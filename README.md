 ## TRIP INFORMATION PROVIDER
 <a name="hdp"></a> 
 
 ## Summary
 
- General description
- Structure
- Utilisation
- Description of each file 
- Main difficulties

<a name="General description"></a> 
## General description
This program is intended to facilitate your trips by giving you information about the weather, the cheapest hotel (its name and price) of the city you're traveling to and also some opinions of what people think about the city based on the last 30 day tweets. The user selects the city, the check-in and the check-out date as well as the number of adults and the program sends an email with all the details.

<a name="Structure"></a>
## Structure
- In "trip_information_provider.py" you will find the whole script of our program. 
- In "packages.ipynb" you will find all the packages we used. 
- In "cheapest_hotel.ipynb" you will find the code which allows to extract the cheapest hotel from the Hotels.com website 
- In "avg_temp.py" you will find the code which allows to obtain the average temperature of a specific city in specific dates.
- In "tweetsentiment" you will find the code which allows to obtain the tweets about a specific city. 
- In "sendmail.ipynb" you will find the function which allows to send an email with trip information from the functions created above
- In "codeRmarkdown.Rmd" you will find our code for the project presentation 
- In "presentation.html" you will find our slides for the project presentation
<a name="Utilisation"></a>
## Utilisation
The user must follow the following steps : 
1. Download the file trip_information_provider
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
- pip install requests
- pip install beautifulsoup4
- pip install urllib
3. Execute the program by entering information the user is asked about and waiting for the result in your email address.

<a name="Description of each file"></a> 
## Description of each file 
There are several files and each of these files is a module containing a function to allow the extraction of the different desired elements.
#### Cheapest_hotel
This module contains the function to extract the cheapest hotel (its name and price) for a given destination, date and number of adults. Information is found on the Hotels.com website. 
#### Avg_temp 
This module contains the function to determine the average temperature for a given city and dates. We used the OpenWeatherMap API. 
#### Tweetsentiment 
This module contains the function to detect the number of tweets for the last 30 days about a specific city and the sentiments expressed. We used Snscrape to get the tweets and the package TextBlob to analyze the sentiments in these tweets. 
#### Sendmail
This module contains the mail function which asks the user for his email address and sends him an email with all the details : average temperature, cheapest hotel and tweets. 

<a name="Main difficulties"></a> 
## Main difficulties 
#### API 
We first wanted to use the Hotels.com's API but it did not display a clear and precise list of hotels so we finally chose Web scraping.
#### Web scraping 
Extracting hotel price and hotel name from the Hotels.com website : the Xpaths were too difficult to exploit. 
#### Weather function 
There were some problems with the attributes, and also with the Openweathermap API so we used import pyowm and then entered the API key.
