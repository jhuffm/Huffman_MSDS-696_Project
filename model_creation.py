import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import acf
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

merged_data = pd.read_csv("merged_data.csv", index_col = 0)

merged_data['Date'] = pd.to_datetime(merged_data.Date , format = '%Y-%m-%d')
data = merged_data.drop(['Date'], axis=1)
data.index = merged_data.Date

# Plotting Infection Rate
merged_data = merged_data.drop(['Date', 'coronavirus_EMA', 'distancing_EMA', 'hygiene_EMA', 'masks_EMA'], axis = 1)
sb.set_style('darkgrid')
merged_data.plot(kind = 'line', legend = 'reverse', title = 'Infection Rate Time-Series')
plt.legend(loc = 2, shadow = True)
plt.tight_layout()
plt.show()

# check for missing values
print(data.isnull().sum())
print(data.shape)

# Test for Causality using Granger causality test
maxlag=12
test = 'ssr_chi2test'
def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False):    
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            min_p_value = np.min(p_values)
            df.loc[r, c] = min_p_value
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    return df

print(grangers_causation_matrix(data, variables = data.columns))

# Split Data into training and validation dataset
# For time series we want to use continuous portions of the dataset rather than pulling a random 80% for training
nobs = 28
training_data = data[:int(0.8*(len(data)))]
validation_data = data[int(0.8*(len(data))):]
print(validation_data.shape)

# Check for Stationarity using the Augmented Dickey-Fuller Test
def adf_test(series, signif=0.05, name = ''):
    dftest = adfuller(series, autolag='AIC')
    adf = pd.Series(dftest[0:4], index=['test_statistic','pvalue','n_Lags','n_obs'])
    for key,value in dftest[4].items():
       adf['Critical Value (%s)'%key] = value
    print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n   ", '-'*47)
    print (adf)
    p = adf['pvalue']
    if p <= signif:
        print(f" Series is Stationary")
    else:
        print(f" Series is Non-Stationary")

# Apply adf test on the series
for name, column in training_data.iteritems():
    adf_test(column, name = column.name)
    print('\n')

# Make all series stationary if necessary by taking first difference
df_differenced = training_data.diff().dropna()
for name, column in df_differenced.iteritems():
    adf_test(column, name = column.name)
    print('\n')

# If still not stationary, take second difference
df_differenced = df_differenced.diff().dropna()
for name, column in df_differenced.iteritems():
    adf_test(column, name = column.name)
    print('\n')

# create and fit a model
model = VAR(df_differenced)
results = model.fit(maxlags=15, ic='aic')
print(results.summary())

# Forecast using model
# Get the lag order
lag_order = results.k_ar
print(lag_order)

# Input data for forecasting
fc = results.forecast(df_differenced.values[-lag_order:], steps=nobs)
df_forecast = pd.DataFrame(fc, index=data.index[-nobs:], columns=data.columns + '_2d')
print(df_forecast)

# Invert model to undo effect of differencing earlier
def invert_transformation(df_train, df_forecast, second_diff=False):
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:        
        # Roll back 2nd Diff
        if second_diff:
            df_fc[str(col)+'_1d'] = (df_train[col].iloc[-1]-df_train[col].iloc[-2]) + df_fc[str(col)+'_2d'].cumsum()
        # Roll back 1st Diff
        df_fc[str(col)+'_forecast'] = df_train[col].iloc[-1] + df_fc[str(col)+'_1d'].cumsum()
    return df_fc

# Display non-inverted predictions
df_results = invert_transformation(training_data, df_forecast, second_diff=True)
print(df_results.loc[:, ['Rate_forecast']])

# Plot predictions vs actuals
sb.set_style('darkgrid')
df_results['Rate_forecast'].plot()
data["Rate"].plot()
plt.title(label = 'Rate Forecast vs Actuals')
plt.legend(loc = 2, shadow = True)
plt.tight_layout()
plt.show()

# Evaluate Accuracy of Model
expected = validation_data['Rate']
predicted = df_results['Rate_forecast'].values

mae = mean_absolute_error(expected, predicted)
mse = mean_squared_error(expected, predicted)
rmse = sqrt(mse)
print('Forecast Accuracy')
print('MAE = %f'% mae)
print('MSE = %f'% mse)
print('RMSE = %f'% rmse)
