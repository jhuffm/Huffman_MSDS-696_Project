import pandas as pd

# Import sentiment data
raw_sentiment_data = pd.read_csv("C:/Users/huffm/raw_sentiment_score.csv")
raw_sentiment_data = raw_sentiment_data[['date_time', 'search_term', 'mean_score']]

## Import Denver metro area data
county_covid_data = pd.read_csv("C:/Users/huffm/Desktop/MSDS 696/data/CDPHE_COVID19_County-Level_Open_Data_Repository.csv")

# Keep only lines that pertain to the case rate
county_covid_data = county_covid_data[county_covid_data.values  == "Case Rates Per 100,000 People in Colorado by County"]

# Keep only rows containing case rate and cases for Denver metro area counties
counties = ['Adams County', 'Arapahoe County', 'Boulder County', 'Broomfield County', 'Denver County', 'Douglas County', 'Jefferson County']
county_covid_data_filtered = pd.DataFrame()
for i in counties:
    temp = county_covid_data[county_covid_data.values  == i]
    county_covid_data_filtered = county_covid_data_filtered.append(temp)

# Only keep 'rate' and 'date' columns
county_covid_data_filtered = county_covid_data_filtered[['Rate', 'Date']]
print(county_covid_data_filtered)

# Convert Date field to a datetime object
county_covid_data_filtered['Date']= pd.to_datetime(county_covid_data['Date']).dt.date

# Remove the time element from the date time field
raw_sentiment_data['date_time']= pd.to_datetime(raw_sentiment_data['date_time']).dt.date

# Take the average sentiment score for each day
raw_sentiment_data = raw_sentiment_data.groupby(['date_time', 'search_term'],as_index=False).mean()

# Average the case rate for the metro area for each day
county_covid_data_filtered = county_covid_data_filtered.groupby(['Date'],as_index = False).mean()

# Pivot data to add seperate column for each search term
raw_sentiment_data = raw_sentiment_data.pivot(index = 'date_time', columns = 'search_term', values = 'mean_score')
# print(raw_denver_sentiment.head())

# Merge dataframes
merged_data = pd.merge(county_covid_data_filtered, raw_sentiment_data, left_on='Date',right_on='date_time', how='outer')
print(merged_data.head())

merged_data.to_csv("C:/Users/huffm/merged_data.csv")
