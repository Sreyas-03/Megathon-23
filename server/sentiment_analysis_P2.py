import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
import re
import pickle
from collections import Counter

# Plots
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# For naive bayes
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split

from time import time
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report

from facebook_scraper import get_posts, get_profile


filename = 'finalized_model.sav'
search = pickle.load(open(filename, 'rb'))










# Reading the dataset with no columns titles and with latin encoding 
# df_raw = pd.read_csv('./training.1600000.processed.noemoticon.csv', encoding = "ISO-8859-1", header=None)

 # As the data has no column titles, we will add our own
# df_raw.columns = ["sentiment", "time", "date", "query", "username", "tweet"]

# # Ommiting every column except for the text and the label, as we won't need any of the other information
# df = df_raw[['sentiment', 'tweet']]

# Replacing the label 4 with 1.
# df['sentiment'] = df['sentiment'].replace(4,1)
# df_pos = df[df['sentiment'] == 1]
# df_neg = df[df['sentiment'] == 0] 
# df_pos = df_pos.iloc[:int(len(df_pos)/80)]
# df_neg = df_neg.iloc[:int(len(df_neg)/80)]
# df = pd.concat([df_pos, df_neg])
# trim_df = False # prevent running more than once  
# is_trimmed = True


# ax = df.groupby('sentiment').count().plot(kind='bar', title='Distribution of data',
#                                                legend=False)
# ax = ax.set_xticklabels(['Negative','Positive'], rotation=0)


contractions = pd.read_csv('./contractions.csv', index_col='Contraction')
contractions.index = contractions.index.str.lower()
contractions.Meaning = contractions.Meaning.str.lower()
contractions_dict = contractions.to_dict()['Meaning']

# Defining regex patterns.
urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|(www\.)[^ ]*)"
userPattern       = '@[^\s]+'
hashtagPattern    = '#[^\s]+'
alphaPattern      = "[^a-z0-9<>]"
sequencePattern   = r"(.)\1\1+"
seqReplacePattern = r"\1\1"

# Defining regex for emojis
smileemoji        = r"[8:=;]['`\-]?[)d]+"
sademoji          = r"[8:=;]['`\-]?\(+"
neutralemoji      = r"[8:=;]['`\-]?[\/|l*]"
lolemoji          = r"[8:=;]['`\-]?p+"

def preprocess_apply(tweet):

    tweet = tweet.lower()

    # Replace all URls with '<url>'
    tweet = re.sub(urlPattern,'<url>',tweet)
    # Replace @USERNAME to '<user>'.
    tweet = re.sub(userPattern,'<user>', tweet)
    
    # Replace 3 or more consecutive letters by 2 letter.
    tweet = re.sub(sequencePattern, seqReplacePattern, tweet)

    # Replace all emojis.
    tweet = re.sub(r'<3', '<heart>', tweet)
    tweet = re.sub(smileemoji, '<smile>', tweet)
    tweet = re.sub(sademoji, '<sadface>', tweet)
    tweet = re.sub(neutralemoji, '<neutralface>', tweet)
    tweet = re.sub(lolemoji, '<lolface>', tweet)

    for contraction, replacement in contractions_dict.items():
        tweet = tweet.replace(contraction, replacement)

    # Remove non-alphanumeric and symbols
    tweet = re.sub(alphaPattern, ' ', tweet)

    # Adding space on either side of '/' to seperate words (After replacing URLS).
    tweet = re.sub(r'/', ' / ', tweet)
    return tweet


# df['processed_tweet'] = df.tweet.apply(preprocess_apply)

# processedtext = list(df['processed_tweet'])
# if is_trimmed: 
#     data_pos = processedtext[10000:]
#     data_neg = processedtext[:10000]
# else: 
#     data_pos = processedtext[800000:]
#     data_neg = processedtext[:800000]














def label_to_str(label):
    if label == 0: return "Negative :"
    return "Positive :"

def nb_predict(df_custom_tweets):
    df_custom_tweets['tweet_processed'] = df_custom_tweets.tweet.apply(preprocess_apply)
    sentiments = search.predict(df_custom_tweets['tweet_processed'])
    for index, row in enumerate(df_custom_tweets['tweet']):
        print(label_to_str(sentiments[index]), row)

def nb_ratio(df_custom_tweets):
    neg = 0
    pos = 0
    df_custom_tweets['tweet_processed'] = df_custom_tweets.tweet.apply(preprocess_apply)
    sentiments = search.predict(df_custom_tweets['tweet_processed'])
    for index, row in enumerate(df_custom_tweets['tweet']):
        if sentiments[index] == 0:
            neg += 1
        else: 
            pos += 1
    # print("pos", pos, "neg", neg)
    if pos == 0:
        return -20.0
    return ((pos-neg)*100/pos) * 0.5 + 50

if __name__ == "__main__":
    post_texts = []
    # user = input("Enter username: ")
    # password = input("Enter password: ")

    USER = "vaibhavagrawal1510"
    PASSWORD = "guliya999208"

    for post in get_posts('shubhankar.kamthankar', pages=3, credentials=(USER, PASSWORD)):
        post_texts.append(post['text'])


    custom_tweets = pd.DataFrame({'tweet': post_texts})
    sentiment_value = nb_ratio(custom_tweets)
    print("num_posts = ", len(post_texts))
    print("sentiment_value : ", sentiment_value)