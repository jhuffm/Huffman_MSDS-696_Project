import re
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import matplotlib.pyplot as plt

# Import pulled Tweets
data_pull = pd.read_csv('C:/Users/huffm/tweets.csv', header=None)
raw_tweets = data_pull.iloc[:,1]

badwords = ['fuck', 'fucking', 'shit', 'bitch', 'ass', 'damn', 'bullshit', 'fucked']

# eliminate special characters, links, short words, and stopwords
raw_string = ''.join(raw_tweets)
no_links = re.sub(r'http\S+', '', raw_string)
no_unicode = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
no_special_characters = re.sub('[^A-Za-z ]+', '', no_unicode)

words = no_special_characters.split(" ")
words = [w for w in words if len(w) > 2]
words = [w.lower() for w in words]
words = [w for w in words if w not in STOPWORDS]
words = [w for w in words if w not in badwords]
 
#print(words)

wc = WordCloud(background_color='white',
        width=1600,
        height=800,
        random_state=21,
        colormap='jet',
        max_words=2000,
        max_font_size=200)

clean_string = ','.join(words)
wc.generate(clean_string)

plt.figure(figsize=(12, 10))
plt.axis('off')
plt.imshow(wc, interpolation="bilinear")
plt.title("Colorado Twitter Word Cloud")
plt.show()


#https://medium.com/@shsu14/introduction-to-data-science-custom-twitter-word-clouds-704ec5538f46
#https://towardsdatascience.com/almost-real-time-twitter-sentiment-analysis-with-tweep-vader-f88ed5b93b1c

