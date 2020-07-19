import GetOldTweets3 as got
import csv
import pandas as pd
import time

# Variables
max_tweets = 13000

#csvFile = open('tweetscolorado.csv', 'a', newline='')
#csvWriter = csv.writer(csvFile)

def namestr(obj, namespace):
        return [name for name in namespace if namespace[name] is obj]

def get_tweets(date_since, date_until, search_term, max_tweets, near, within):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(search_term)\
                                           .setSince(date_since)\
                                           .setUntil(date_until)\
                                           .setMaxTweets(max_tweets)\
                                           .setNear(near)\
                                           .setWithin(within)\
                                           .setLang('en')
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for tweet in tweets:
        tweet_text = tweet.text.encode('utf-8', 'ignore')
        tweet_date = tweet.date
        tweet_id = tweet.id
        tweet_geo = tweet.geo
        csvWriter.writerow([tweet_id, tweet_text, tweet_date, tweet_geo])

#get_tweets()
# Create Cagegories of search terms
masks = 'masks OR coverings OR face masks OR mask OR facemasks OR facemask OR ppe'
social_distance = 'distance OR apart OR social distance OR isolation OR isolating OR socialdistancing OR stayathome OR lockdown OR stayhome OR staysafe'
hand_washing = 'wash hands OR wash OR washing OR sanitize OR santizing OR washyourhands OR handsanitizer OR disinfect OR santise OR clean'

# Create search grid
search_grid = [masks, social_distance, hand_washing]

# Load county info for centerpoint and radius of each Colorado county
colorado_counties = pd.read_csv("C:/Users/huffm/Desktop/MSDS 696/data/colorado_counties.csv", index_col = "county")

# Dates to pull
# Pulling one day at a time to avoid having to start over if program encounters problems
idx = pd.date_range(start="2020-03-15",end="2020-06-30").date
idx2 = pd.date_range(start="2020-03-16",end="2020-07-01").date
starting_dates = pd.DataFrame({'date_since':idx})
ending_dates = pd.DataFrame({'date_until':idx2})
dates = starting_dates.merge(ending_dates, left_index = True, right_index=True)

# # iterate through each county creating a different .csv file for each county/search term combination
for index, row in dates.iterrows():
        date_since = str(row['date_since'])
        date_until = str(row['date_until'])
        
        for i in search_grid:
                search_term = i
                name = namestr(search_term, globals())[0]
        
                for label, row in colorado_counties.iterrows():
                        near = str(row["latitude"])+', '+ str(row["longitude"])
                        within = str(row["geocode_radius"])+"mi"
                        filename = name + '_' + label + ".csv"
                        csvFile = open(filename, 'a', newline='')
                        csvWriter = csv.writer(csvFile)
                        get_tweets(date_since, date_until, search_term, max_tweets, near, within)
