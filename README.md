 ## HOTELS BOOKING HELPER 
 <a name="hdp"></a> 
 
 ## Summary
 
- General description
- Structure
- Utilisation
- Description of each file 
- Main difficulties

<a name="General description"></a> 
## General description
This program is intended to facilitate the booking of hotels on the Hotels.com site. You select a city and dates and this program sends you an email with the name of the cheapest hotel, its price, the weather during the stay and the different opinions based on tweets about the city.

<a name="Structure"></a>
## Structure
- In "name_file " you will find the whole script of our program. 
- In "name_file" you will find all the packages we used. 
- In "name_file" you will find all the functions we used. 
- In "name_file" you will find the code which allows to extract the cheapest hotel from the Hotels.com website 
- In "name_file" you will find the code which allows to obtain the meteo of a specific city at specific dates.
- In "name_file" you will find the code which allows to obtain the tweets about a specific city. 

<a name="Utilisation"></a>
## Utilisation
The user must follow the following steps : 
1. Download the file hotels_booking_helper
2. Open a terminal and copy and paste the following packages : 
- pip install pyowm
- pip install urllib.request
- pip install json
- pip install ssl
- pip install schedule
- pip install smtplib
- pip install numpy 
- pip install pandas 
- pip install re
- pip install textblob 
- pip install sys
- pip install selenium
3. 
<a name="Description of each file"></a> 
## Description of each file 
There are several files and each of these files is a module containing a function to allow the extraction of the different desired information.
#### Cheapest_hotel
This module contains the function to extract the cheapest hotel for a given destination, dates and number of adults, on the Hotels.com website. 
#### Meteo 
This module contains the function to determine the meteo for a given city and dates. We used the API OpenWeatherMap. 
#### Twitter 
This module contains the function to detect the number of tweets about a specific city and the sentiments expressed in the tweets about this city. 
