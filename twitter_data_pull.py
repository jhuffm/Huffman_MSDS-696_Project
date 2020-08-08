import GetOldTweets3 as got
import csv
import pandas as pd
import time

# Variables
max_tweets = 15000
# Colorado radius
# near = '38.99903,-105.5459'
# within = '190mi'

# Greater Denver area radius
near = '39.747469,-104.872391'
within = '45mi'

# Function to pull variable name for search terms to append to filename later
def namestr(obj, namespace):
        return [name for name in namespace if namespace[name] is obj]

# Function to scrape Twitter data
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

# Create lists of words grouped into categories to search for
masks = 'masks OR coverings OR face masks OR mask OR facemasks OR facemask OR ppe OR breathe'
social_distance = 'distance OR apart OR social distance OR isolation OR isolating OR socialdistancing OR stayathome OR lockdown OR stayhome OR staysafe'
hand_washing = 'wash hands OR wash OR washing OR sanitize OR santizing OR washyourhands OR handsanitizer OR disinfect OR santise OR clean'
coronavirus = 'coronavirus OR covid19 OR covid-19 OR covid OR pandemic OR virus'

# Create search grid
search_grid = [masks, social_distance, hand_washing, coronavirus]

# Create list of dates to pull Dates to pull
# Pulling one day at a time to avoid having to start over if program encounters problems
idx = pd.date_range(start="2020-03-17",end="2020-07-31").date
idx2 = pd.date_range(start="2020-03-18",end="2020-08-01").date
starting_dates = pd.DataFrame({'date_since':idx})
ending_dates = pd.DataFrame({'date_until':idx2})
dates = starting_dates.merge(ending_dates, left_index = True, right_index=True)

# iterate through each county creating a different .csv file for each county/search term combination
# Iterating through each day
for index, row in dates.iterrows():
        date_since = str(row['date_since'])
        date_until = str(row['date_until'])
       
        # Iterate through each parameter in the search grid
        for i in search_grid:
                search_term = i
                name = namestr(search_term, globals())[0]

                filename = name + "_" +'Greater Denver Area County.csv'
                csvFile = open(filename, 'a', newline='')
                csvWriter = csv.writer(csvFile)
                get_tweets(date_since, date_until, search_term, max_tweets, near, within)
