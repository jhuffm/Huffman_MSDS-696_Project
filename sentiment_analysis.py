import pandas as pd
import string
from nltk.tokenize import word_tokenize
import numpy as np

# Read in Tweets
text = pd.read_csv("C:/Users/huffm/combined_twitter_data.csv", index_col = 0)

## Process text prior to sentiment analysis
# Convert to lower case
text['tweet_text'] = text['tweet_text'].str.lower()

# Remove punctuation
text['tweet_text'] = text['tweet_text'].str.translate(str.maketrans('','', string.punctuation))

# Remove first character since every tweet shows 'b' as the first character
text['tweet_text'] = text['tweet_text'].str[1:]

# Split tweets into individual words
text['tokenized_tweets'] = text.apply(lambda row: word_tokenize(row['tweet_text']), axis=1)

## Sentiment Analysis
scores_file = "C:/Users/huffm/Desktop/MSDS 696/AFINN-165.txt"

# Loop through words in scores_file and store in dictionary
def readSentimentData(sentimentDataFile):
    sentimentfile = open(sentimentDataFile, "r")
    scores = {} 	
    for line in sentimentfile:
        word, score = line.split("\t")
        scores[word] = int(score) 
    sentimentfile.close()
    return scores	

scores = readSentimentData(scores_file)

text['mean_score'] = ""
i=0
# Loop through words in individual tweets to see if they contain words from the scores_file, produce the mean score for each tweet
for line in text['tokenized_tweets']:
    sentiments = {"-5": 0, "-4": 0, "-3": 0, "-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    n=0
    for word in line:
        if word in scores.keys():
            score = scores[word]
            sentiments[str(score)] += 1
            n+=1
    if n > 0:
        text['mean_score'].loc[i] = 1/n*(sentiments["-5"]*-5+sentiments["-4"]*-4+sentiments["-3"]*-3+sentiments["-2"]*-2+sentiments["-1"]*-1+sentiments["0"]*0+sentiments["1"]*1+sentiments["2"]*2+sentiments["3"]*3+sentiments["4"]*4+sentiments["5"]*5)
    else:
        text['mean_score'].loc[i]=0
    i+=1

text.to_csv("C:/Users/huffm/raw_sentiment_score.csv")
print(text.head(10))
