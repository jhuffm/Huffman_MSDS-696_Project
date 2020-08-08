import pandas as pd
import matplotlib.pyplot as plt

## Import and organize sentiment data
raw_sentiment_data = pd.read_csv("raw_sentiment_score.csv")
# Keep only the date, search term, and sentiment score columns
raw_sentiment_data = raw_sentiment_data[['date_time', 'search_term', 'mean_score']]
# Remove the time element from the date time field
raw_sentiment_data['date_time']= pd.to_datetime(raw_sentiment_data['date_time']).dt.date
# Take the average sentiment score for each day
raw_sentiment_data = raw_sentiment_data.groupby(['date_time', 'search_term'],as_index=False).mean()
# Pivot data to add seperate column for each search term
raw_sentiment_data = raw_sentiment_data.pivot(index = 'date_time', columns = 'search_term', values = 'mean_score')

## Import and organize County Data
county_covid_data = pd.read_csv("https://raw.githubusercontent.com/jhuffm/Huffman_MSDS-696_Project/master/data/CDPHE_COVID19_County-Level_Open_Data_Repository.csv")
# Keep only rows containing case rate and cases for Denver metro area counties
counties = ['Adams County', 'Arapahoe County', 'Boulder County', 'Broomfield County', 'Denver County', 'Douglas County', 'Jefferson County']
county_covid_data = county_covid_data[county_covid_data.values  == "Case Rates Per 100,000 People in Colorado by County"]
county_covid_data_filtered = pd.DataFrame()
for i in counties:
    temp = county_covid_data[county_covid_data.values  == i]
    county_covid_data_filtered = county_covid_data_filtered.append(temp)
# Keep only the date and case rate columns
county_covid_data_filtered = county_covid_data_filtered[['Rate', 'Date']]
# Convert Date field to a datetime object
county_covid_data_filtered['Date']= pd.to_datetime(county_covid_data['Date']).dt.date
# Take the mean case rate across the 7 counties for each day
county_covid_data_filtered = county_covid_data_filtered.groupby(['Date'],as_index = False).mean()

## Merge dataframes
merged_data = pd.merge(county_covid_data_filtered, raw_sentiment_data, left_on='Date',right_on='date_time', how='inner')

# Create a moving average of the twitter data using an exponential moving average
merged_data['coronavirus_EMA'] = merged_data['coronavirus'].ewm(span = 3, adjust=False).mean()
merged_data['distancing_EMA'] = merged_data['distancing'].ewm(span = 3, adjust=False).mean()
merged_data['hygiene_EMA'] = merged_data['hygiene'].ewm(span = 3, adjust=False).mean()
merged_data['masks_EMA'] = merged_data['masks'].ewm(span = 3, adjust=False).mean()

# Plot the original data against the moving average
f, ax = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
ax[0,0].plot(merged_data['coronavirus'],label='coronavirus')
ax[0,0].plot(merged_data['coronavirus_EMA'],label='EMA')
ax[0,0].grid(True)
ax[0,0].legend(loc=2)
ax[0,1].plot(merged_data['distancing'],label='distancing')
ax[0,1].plot(merged_data['distancing_EMA'],label='EMA')
ax[0,1].grid(True)
ax[0,1].legend(loc=2)
ax[1,0].plot(merged_data['hygiene'],label='hygiene')
ax[1,0].plot(merged_data['hygiene_EMA'],label='EMA')
ax[1,0].grid(True)
ax[1,0].legend(loc=2)
ax[1,1].plot(merged_data['masks'],label='masks')
ax[1,1].plot(merged_data['masks_EMA'],label='EMA')
ax[1,1].grid(True)
ax[1,1].legend(loc=2)

plt.show()

# Drop the original columns and keep the moving average
merged_data.drop(merged_data.columns[[2,3,4,5]], axis = 1, inplace = True)

merged_data.to_csv("merged_data.csv")
