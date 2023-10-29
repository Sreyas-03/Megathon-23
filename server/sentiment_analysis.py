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



# Reading the dataset with no columns titles and with latin encoding 
df_raw = pd.read_csv('./training.1600000.processed.noemoticon.csv', encoding = "ISO-8859-1", header=None)

 # As the data has no column titles, we will add our own
df_raw.columns = ["sentiment", "time", "date", "query", "username", "tweet"]

# Ommiting every column except for the text and the label, as we won't need any of the other information
df = df_raw[['sentiment', 'tweet']]

# Replacing the label 4 with 1.
df['sentiment'] = df['sentiment'].replace(4,1)
df_pos = df[df['sentiment'] == 1]
df_neg = df[df['sentiment'] == 0] 
df_pos = df_pos.iloc[:int(len(df_pos)/80)]
df_neg = df_neg.iloc[:int(len(df_neg)/80)]
df = pd.concat([df_pos, df_neg])
trim_df = False # prevent running more than once  
is_trimmed = True


ax = df.groupby('sentiment').count().plot(kind='bar', title='Distribution of data',
                                               legend=False)
ax = ax.set_xticklabels(['Negative','Positive'], rotation=0)


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


df['processed_tweet'] = df.tweet.apply(preprocess_apply)

processedtext = list(df['processed_tweet'])
if is_trimmed: 
    data_pos = processedtext[10000:]
    data_neg = processedtext[:10000]
else: 
    data_pos = processedtext[800000:]
    data_neg = processedtext[:800000]



#X_data, y_data = np.array(df['processed_tweet']), np.array(df['sentiment'])

df_train, df_test = train_test_split(df, test_size=0.10, random_state=42)
X_train, y_train = np.array(df_train['processed_tweet']), np.array(df_train['sentiment'])
X_test, y_test = np.array(df_test['processed_tweet']), np.array(df_test['sentiment'])

#X_train, X_test, y_train, y_test = train_test_split(X_data, y_data,test_size = 0.05, random_state = 42)

pos = 0
neg = 0
for val in y_train: 
    if val == 0:
        neg +=1 
    else: pos +=1
# print("pos", pos, "neg", neg)


                
start_time = time()

pipe = Pipeline([('vect', CountVectorizer()),
                     ('clf', MultinomialNB())])


# Parameters of pipelines can be set using ‘__’ separated parameter names:
param_grid = {
    'vect__binary': [True, False], # If True, all non zero counts are set to 1. This is what how interpreted "set of words"
    'vect__ngram_range': [(1,1), (1,2)], # unigram, unigram + bigram
    'clf__alpha': [1, 0.1]
}

search = GridSearchCV(pipe, param_grid, n_jobs=-1) # defaults to 5-fold 
search.fit(df_train['processed_tweet'], df_train['sentiment']) # Pipeline requires pd 


y_pred_mnb = search.predict(df_test['processed_tweet'])


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
    return (pos-neg)*100/pos

post_texts = []
for post in get_posts('MarkZuckerberg', pages=3, credentials=('6352927215', 'sam6561')):
    # print(post['text'])
    post_texts.append(post['text'])


custom_tweets = pd.DataFrame({'tweet': post_texts})
sentiment_value = nb_ratio(custom_tweets)
print("num_posts = ", len(post_texts))
print("sentiment_value : ", sentiment_value)