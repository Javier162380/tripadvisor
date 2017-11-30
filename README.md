# Tripadvisor
 web scrapping.
This script is just a small example of how to scrape a web page using Request, aiohttp, and Beautiful Soup Python Libraries.

To execute the script we need to insert at least one parameter, the url of the place we want to scrape as an example: https://www.tripadvisor.es/Hotels-g187443-Seville_Province_of_Seville_Andalucia-Hotels. html, the second parameter is the database table where we will store the information,
Parameters 3,4,5 refer to the username, password and database that we are going to use and the sixth parameter refers to the google maps API key that we will use to obtain the latitude and longitude of the hotels. The last parameter is optional and refers to the number of hotel pages we want to scrape.

The frist script (tripadvisor. py) uses synchronized requests to make each call. It is the slowest of all, because until one request is finished, the next one is not launched. The second script makes parallel calls and improves efficiency over the first script. The latter is the most efficient of all uses asynchronous coroutines since the same session, relying on asyncio, aiohttp having a behavior similar to that of scrapy.

To store our data we will use the Postgresql database. I created a small class of python to perform some useful functions, in this case we will use a method to run the insertion of several rows.

To run this application on your local machine, simply clone the repo and install all packages and dependencies through the requirements file. txt (sudo pip install -r requisites. txt).

In addition, I have carried out a small analysis of maps and clustering.

