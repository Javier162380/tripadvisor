# tripadvisor

web scrapping.
This script it is just a small example of how to scrape a web page using Request, and Beautiful Soup Python Libraries.

To execute the script we need to insert a least one parameter, the url of the place we want to scrape as an example:https://www.tripadvisor.es/Hotels-g187443-Seville_Province_of_Seville_Andalucia-Hotels.html, the second parameter it is optional, and it is the number of pages of hotels we got in the location we want to scrape.

To save our data we are going to use Postgresql database. I create a small python class to perform  a multiple row insert. 

