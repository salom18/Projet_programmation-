import pyowm
import requests
import os
from datetime import datetime, timedelta
import urllib.request
from urllib.request import urlopen
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

#Get user input
name=input("Enter your name: ")
city=input("Enter a city: ")
checkin_date=input("Enter the check-in date (YYYY-MM-DD): ")
checkout_date=input("Enter the check-out date (YYYY-MM-DD): ")


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
