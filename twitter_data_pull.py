import os
import tweepy as tw
import pandas as pd
import csv
import twitter

# Authenticate with Twitter
consumer_key= "consumer_key"
consumer_secret= "consumer_secret"
access_token= "access_token"
access_token_secret= "access_token_secret"

# Using Tweepy
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Search Terms
search_words = "*"
cnt = 1000
geo = '38.99903,-105.5459,190mi'

# Collect Tweets
# Collect Tweets and write to CSV using Tweepy and CSVWriter
csvFile = open('tweets.csv', 'a')
csvWriter = csv.writer(csvFile)

for tweet in tw.Cursor(api.search,
              q= search_words + "-filter:retweets",
              lang="en",
              geocode= geo).items(cnt):
    csvWriter.writerow([tweet.created_at, tweet.text.encode('ascii', 'ignore'), tweet.user.id, tweet.user.location.encode('utf-8', 'ignore')])
