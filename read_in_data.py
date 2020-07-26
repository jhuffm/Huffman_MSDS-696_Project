import pandas as pd
from glob import glob
import os
import numpy as np

# Select all csv files that have data for this project
stock_files = sorted(glob("C:/Users/huffm/* County.csv"))

# Combine individual twitter pull files into single data frame
dfList = []
for filename in stock_files:
    if os.stat(filename).st_size != 0:
        df = pd.read_csv(filename, header = None).assign(filename = filename)
        dfList.append(df)
combined_twitter_data = pd.concat(dfList, axis = 0).reset_index()

# Add a column for the search term used
a = combined_twitter_data.filename.str[:19]
combined_twitter_data['search_term'] = np.where(a == 'C:/Users/huffm\hand', 'hygiene',
    np.where(a == 'C:/Users/huffm\mask', 'masks',
    np.where(a == 'C:/Users/huffm\soci', 'distancing',
    np.where(a == 'C:/Users/huffm\coro', 'coronavirus', 0))))

# Add a column for the name of the county pulling the information from the filename
county_data = pd.read_csv("C:/Users/huffm/Desktop/MSDS 696/data/colorado_counties.csv")
combine_statement = ""
for county in county_data['county']:
    length = len(county) + 4
    filename_string = "combined_twitter_data.filename.str[-"+str(length)+":]"
    parameter = county + '.csv'
    variable = "np.where("+filename_string+" == '"+parameter+"','"+county+"', "
    combine_statement = combine_statement + variable

paren_number =  ")" * 64
final_combine_statement = combine_statement + " 0" + str(paren_number)
combined_twitter_data['county'] = eval(final_combine_statement)

# Remove unnecessary columns and add appropriate column headers
combined_twitter_data.drop(combined_twitter_data.columns[[0, 4]], axis = 1, inplace = True)
combined_twitter_data.columns = ['id', 'tweet_text', 'filename', 'date_time', 'search_term', 'county']

# Save new dataframe to a csv file
combined_twitter_data.to_csv("C:/Users/huffm/combined_twitter_data.csv")
print(combined_twitter_data.head())