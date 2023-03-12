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
import requests
import urllib.parse
import string
from bs4 import BeautifulSoup
import smtplib
import time
import pyowm
from datetime import datetime, timedelta
import urllib.request
from urllib.request import urlopen
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime, timedelta
import urllib.request
from urllib.request import urlopen
import os
import json
import ssl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unicodedata
from lxml import html

#Get user input

name=input("Enter your name: ")
city=input("Enter a city: ")
checkin_date=input("Enter the check-in date (YYYY-MM-DD): ")
checkout_date=input("Enter the check-out date (YYYY-MM-DD): ")
nb_adults=int(input("Enter the number of adults: "))
url = f"https://fr.hotels.com/Hotel-Search?adults={nb_adults}&d1={checkin_date}&d2={checkout_date}&destination={urllib.parse.quote(city)}&endDate={checkout_date}&latLong=%2C&selected=&semdtl=&sort=PRICE_LOW_TO_HIGH&startDate={checkin_date}&theme=&useRewards=false&userIntent="


####PART 1 - Find the average temperature of a city between the departure date and the arrival date###

def get_avg_weather(city, checkin_date, checkout_date):
    #get the API
    owm = pyowm.OWM("5ebbddc757117fab77a6c7785688f4a1")
    #date de depart et date d'arrive
    start_date = datetime.strptime(checkin_date, '%Y-%m-%d')
    end_date = datetime.strptime(checkout_date, '%Y-%m-%d') + timedelta(days=1)
    # check if start date is greater than end date
    if start_date >= end_date:
        return -1
    daily_forecasts = []
    while start_date < end_date:
        try:
            observation = owm.weather_manager().weather_at_place(city)
            weather = observation.weather
            daily_forecasts.append(weather)
        except pyowm.exceptions.api_response_error.NotFoundError:
            print(f"Invalid city name: {city}")
            return -1
        start_date += timedelta(days=1)
    total_temp = sum([f.temperature('celsius')['temp'] for f in daily_forecasts])
    avg_temp = total_temp / len(daily_forecasts)
    return avg_temp

def get_weather():
    avg_temp=get_avg_weather(city, checkin_date, checkout_date)
    result=f'Hello {name}! I hope you are doing well! We just found out that you are visiting {city} soon. The first thing you should know is certainly the weather! The average temperature in {city} between {checkin_date} and {checkout_date} will be {avg_temp:.1f} degrees Celsius, so be careful while packing your clothes!'
    return(result)


###PART 2 - Find the cheapest hotel 

def get_hrefs(url):
    response = requests.get(url)
    result = response.content
    soup = BeautifulSoup(result, 'html.parser')
    result_container=soup.find("div", class_="uitk-card uitk-card-roundcorner-all uitk-card-has-primary-theme")
    hotel_link=result_container.find("a", class_="uitk-card-link")
    if hotel_link:
        href=hotel_link.get("href")
    else:
        print("No hotel links found")
                       
    pattern = r'top_dp=(\d+)&top_cur=([A-Z]{3})'
    match = re.search(pattern, href)
    if match:
        top_dp = match.group(1)
        top_cur = match.group(2)
    pattern1 = r'/([^/]+)/\?'
    match1 = re.search(pattern1, href)
    if match1:
        hotel_name = match1.group(1)
        hotel_name = re.sub(r'-', ' ', hotel_name)
        Hotel=string.capwords(hotel_name)
    result2=f" If you are on a budget, we suggest for your staying to book '{Hotel}' as it is the cheapest hotel in town. You will only have to pay {top_dp}{top_cur} per night! That is cool, right?"
    return(result2)

def find_hotels():
    hotel_cheap=get_hrefs(url)
    return(hotel_cheap)


####PART 3 - Find tweets and nature of 100 tweets for the last 30 days for a given word###

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

    #Applying this function to Text column of our dataframe
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

####PART 4 ----Send email with all information###

def send_email():
    message1 = get_weather()
    if message1 is not None:
        message1 = str(message1)

    message2 = find_hotels()
    if message2 is not None:
        message2 = str(message2)

    message3 = get_sent()
    if message3 is not None:
        message3 = str(message3)

    message_final = (message1 or "") + (message2 or "") + (message3 or "")
    s=smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("projectpythonse@gmail.com", "bapffljplqnfvgxs")
    SUBJECT="Informations"
    TEXT=message_final.encode('utf-8')
    message="Subject:{}\n\n{}".format(SUBJECT,TEXT.decode('utf-8'))
    while True:
        destinateur=input("Enter your email:")
        if not destinateur:
            print("Email address cannot be empty. Please try again.")
        elif "@" not in destinateur:
            print("Invalid email address. Please try again.")
        else:
            break
    s.sendmail("projectpythonse@gmail.com", destinateur,message.encode('utf-8'))
    s.quit()
    print("Formuler le mail.")
    time.sleep(2)
    print("En train d'envoyer le mail...")
    time.sleep(1)
    print("Email envoyé! ")

send_email()
