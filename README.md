# tripadvisor

web scrapping.
This script it is just a small example of how to scrape a web page using Request, and Beautiful Soup Python Libraries.

To execute the script we need to insert a least one parameter, the url of the place we want to scrape as an example:https://www.tripadvisor.es/Hotels-g187443-Seville_Province_of_Seville_Andalucia-Hotels.html, the second parameter it is the database table were we are going to store the information,
Parameters 3,4,5 are refer to the username, password and Database we are going to use. The last parameter it is optional and it is refer to the number of hotels pages we want to scrape.

To save our data we are going to use Postgresql database. I create a small python class to perform some useful functions.In this case we are going to use a method to execute multiple row insert.

To run this app in your local machine just clone the repo and install all the packages and dependencies via requirements.txt file (sudo pip install -r requirements.txt).

