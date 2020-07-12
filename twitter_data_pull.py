import os
import tweepy as tw
import pandas as pd
import csv
import twitter

# Authenticate with Twitter
consumer_key= "66l8nfYqZIshVFitg1YvIILN5"
consumer_secret= "Ja5U1G3uQWt5YpP1Au32zCF28JwghzLxglU0oPyHMHINKSyZim"
access_token= "1015836533360750592-Z7o7AOKszVDs3FZCpObRJwfveh6Ojl"
access_token_secret= "KT8Nusyyvbp5eI57uDPd1CGu8JYr9KOENpO9laSYL9tvX"

# Using Tweepy
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Using Twitter
#api2 = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret)


# Search Terms
search_words = "*"
#date_since = "2016-05-01"
cnt = 500000
geo = '38.99903,-105.5459,190mi'

# Collect Tweets
# Collect Tweets and write to CSV using Tweepy
csvFile = open('tweets.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tw.Cursor(api.search,
              q= search_words + "-filter:retweets",
              lang="en",
              geocode= geo).items(cnt):
    #print([tweet.created_at, tweet.text.encode('utf-8'), tweet.user.id, tweet.geo])
    #csvWriter.writerow([tweet.created_at, tweet.text, tweet.user.id, tweet.user.location])
    csvWriter.writerow([tweet.created_at, tweet.text.encode('ascii', 'ignore'), tweet.user.id, tweet.user.location.encode('utf-8', 'ignore')])

# Collect Tweets and write to CSV using twitter
#csvFile2 = open('tweets2.csv', 'a')
#csvWriter2 = csv.writer(csvFile2)
#for tweet in api2.GetSearch(geocode=geo, lang='en', count=cnt):
#    csvWriter2.writerow([tweet.created_at, tweet.text.encode('utf-8', 'ignore'), tweet.user.id, tweet.user.location.encode('utf-8', 'ignore')])

# Iterate and print tweets
#for tweet in tweets:
#    print(tweet.text)

# Create Pandas Dataframe
#tweet_text = pd.DataFrame(data=users_locs, 
#                    columns=['user', "location"])
#tweet_text


##References
#https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/twitter-data-in-python/
#https://www.researchgate.net/post/Is_it_possible_to_retrieve_locations_of_tweets_even_though_the_location_of_users_were_turned_off
#https://medium.com/@shsu14/introduction-to-data-science-custom-twitter-word-clouds-704ec5538f46
#https://www.bmc.com/blogs/track-tweets-location/
#https://www.techtrek.io/generating-word-cloud-from-twitter-feed-with-python/
#https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed
#http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html
#http://docs.tweepy.org/en/v3.5.0/api.html
#https://readthedocs.org/projects/tweepy/downloads/pdf/latest/
#https://stackoverflow.com/questions/58152326/using-bounding-box-for-collecting-twitter-stream
#https://towardsdatascience.com/almost-real-time-twitter-sentiment-analysis-with-tweep-vader-f88ed5b93b1c
#https://www.reddit.com/r/learnpython/comments/e7ukpr/tweepy_cursor_geocode_how_does_it_work/