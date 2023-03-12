import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import re
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import snscrape.modules.twitter as sntwitter
import nltk
import sys

city=input("Enter a city: ")
###Find 100 tweets for the last 30 days###

def analyze_sentiment(city):
    noOfTweet=100
    noOfDays=30
    if city != '':
        #Creating list to append tweet data
        tweets_list = []
        now = dt.date.today()
        now = now.strftime('%Y-%m-%d')
        yesterday = dt.date.today() - dt.timedelta(days = int(noOfDays))
        yesterday = yesterday.strftime('%Y-%m-%d')
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(city + ' lang:en since:' +  yesterday + ' until:' + now + ' -filter:links -filter:replies').get_items()):
            if i > int(noOfTweet):
                break
            tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username])
        if not tweets_list:
            return (f"If you wonder what people think about {city}, we are really sorry to say that there are no tweets found for '{city}' in the past 30 days.")
        #Creating a dataframe from the tweets list above 
        df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
    # Create a function to clean the tweets
    def cleanTxt(text):
        text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
        text = re.sub('#', '', text) # Removing '#' hash tag
        text = re.sub('RT[\s]+', '', text) # Removing RT
        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
        return text

    #applying this function to Text column of our dataframe
    df["Text"] = df["Text"].apply(cleanTxt)

    #Sentiment Analysis
    def percentage(part,whole):
        return 100 * float(part)/float(whole)

    #Assigning Initial Values
    positive = 0
    negative = 0
    neutral = 0
    #Creating empty lists
    tweet_list1 = []
    neutral_list = []
    negative_list = []
    positive_list = []

    #Iterating over the tweets in the dataframe
    for tweet in df['Text']:
        tweet_list1.append(tweet)
        blob = TextBlob(tweet)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            positive_list.append(tweet) #appending the tweet that satisfies this condition
            positive += 1 #increasing the count by 1
        elif polarity < 0:
            negative_list.append(tweet) #appending the tweet that satisfies this condition
            negative += 1 #increasing the count by 1
        else:
            neutral_list.append(tweet) #appending the tweet that satisfies this condition
            neutral += 1 #increasing the count by 1 

    positive = percentage(positive, len(df)) #percentage is the function defined above
    negative = percentage(negative, len(df))
    neutral = percentage(neutral, len(df))

    #Converting lists to pandas dataframe
    tweet_list1 = pd.DataFrame(tweet_list1)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    #using len(length) function for counting
    return(f"..And last but not least, do you wonder what people recently think about {city}? Don't worry ! We collected and sorted some tweets for you. There have been {len(tweet_list1)} tweets on '{city}' for the last 30 days. There are {len(positive_list)} tweet(s) with a positive Sentiment, {len(neutral_list)} tweet(s) with Neutral Sentiment and {len(negative_list)} tweet(s) with Negative Sentiment. Now it's all up to you! Enjoy your trip! ")

def get_sent():
    sent=analyze_sentiment(city)
    return(sent)
