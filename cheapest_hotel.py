###Second part-Find the cheapest hotel and extract its name and price per night 

import requests
import string
import urllib.parse
import re
from bs4 import BeautifulSoup


name=input("Enter your name: ")
city=input("Enter a city: ")
checkin_date=input("Enter the check-in date (YYYY-MM-DD): ")
checkout_date=input("Enter the check-out date (YYYY-MM-DD): ")
nb_adults=int(input("Enter the number of adults: "))
url = f"https://fr.hotels.com/Hotel-Search?adults={nb_adults}&d1={checkin_date}&d2={checkout_date}&destination={urllib.parse.quote(city)}&endDate={checkout_date}&latLong=%2C&selected=&semdtl=&sort=PRICE_LOW_TO_HIGH&startDate={checkin_date}&theme=&useRewards=false&userIntent="

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
