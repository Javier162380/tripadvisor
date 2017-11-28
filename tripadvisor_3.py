
# -*- coding: utf-8 -*-
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import googlemaps
from requests import get
from time import  sleep
from sys import argv
from postgre import postgre


def internallinks(url,number_of_pages):
    """This method is perform to extract all the pages of the site """
    hotelslist = set()
    request = get(url)
    parser = BeautifulSoup(request.text, 'html.parser')
    page_load = 5
    for link in parser.findAll("a", href=re.compile("^(/|.*)(?=REVIEWS)")):
        if link.attrs['href'] is not None:
            hotelurl = link.attrs['href']
            url = 'https://www.tripadvisor.es' + str(hotelurl)
            hotelslist.add(url)
        else:
            pass
    next_page = parser.find(class_="prw_rup prw_common_standard_pagination_resp").find("a", href=re.compile("^(/|.*)"))
    next_page_url = next_page.attrs['href']
    while number_of_pages > 1:
        url = 'https://www.tripadvisor.es' + str(next_page_url)
        request = get(url)
        parser = BeautifulSoup(request.text, 'html.parser')
        for link in parser.findAll("a", href=re.compile("^(/|.*)(?=REVIEWS)")):
            if link.attrs['href'] is not None:
                hotelurl = link.attrs['href']
                url = 'https://www.tripadvisor.es' + str(hotelurl)
                hotelslist.add(url)
            else:
                pass
        try:
            next_page = parser.find(class_="prw_rup prw_common_standard_pagination_resp").find("a", href=re.compile(
                "^(/|.*)"))
            next_page_url = next_page.attrs['href']
            print(next_page_url)
            number_of_pages = number_of_pages - 1
            if page_load < 5:
                page_load = page_load + (5 - page_load)
            else:
                pass
        except:
            print(
                "IndexError(Encontramos un error al extraer la  {0} página volvemos a ejecutar el contenido de esa "
                "pagina)".format(str(number_of_pages)))
            sleep(1)
            if page_load > 0:
                page_load = page_load - 1
                pass
            else:
                raise IndexError("Encontramos un error al extraer la  {0} multiples fallos "
                                 "salimos ").format(str(number_of_pages))
    return hotelslist

def gethotelsinfo(url,key):
    """This methos it is perform to retrieve a list with all the information of the hotels.Asynchronous Request."""
    response = yield from aiohttp.request('GET', url)
    text = yield from  response.read()
    hotelsinformation=[]
    #we create a google maps object.
    gmaps = googlemaps.Client(key=key)
    parser = BeautifulSoup(text, 'html.parser')
    hotelreview = []
    #name
    try:
        name = parser.find(class_="heading_title").get_text()
        title = re.sub('\n', '', name)
    except:
        title = None
    hotelreview.append(title)
    # address
    try:
        address = parser.find(class_="content hidden").get_text('')
    except:
        address = None
    hotelreview.append(address)
    #latitude and longitude
    if address is None:
        latitude=None
        longitude=None
    else:
        try:
            #we make the request to the google maps API.
            geocode_result = gmaps.geocode(address)
            latitude=geocode_result[0]['geometry']['location']['lat']
            longitude=geocode_result[0]['geometry']['location']['lng']
        except:
            latitude=None
            longitude=None
    hotelreview.append(latitude)
    hotelreview.append(longitude)
    # zipcode.
    try:
        raw_zipcode = parser.find(class_="content hidden").find(class_="locality").get_text('')
        zipcode = int(raw_zipcode.split(' ')[0])
    except:
        zipcode=None
    hotelreview.append(zipcode)
    #city
    try:
        raw_city = parser.find(class_="content hidden").find(class_="locality").get_text('')
        city = raw_city.split(' ')[1].replace(',', '')
    except:
        city=None
    hotelreview.append(city)
    # rooms
    try:
        numberofrooms = int(parser.find(class_="list number_of_rooms").get_text(';').split(';')[1])
    except:
        numberofrooms = None
    hotelreview.append(numberofrooms)
    # stars
    try:
        stars = parser.find(class_="starRating detailListItem").get_text(';').split(';')[1]
    except:
        stars = None
    hotelreview.append(stars)
    # services
    try:
        service = str([i.get_text(';') for i in parser.find(class_="detailsMid").
                      findAll(class_="highlightedAmenity detailListItem")]).replace("'", "")
    except:
        service = None
    hotelreview.append(service)
    # price
    try:
        prices = parser.find(class_="list price_range").get_text(';').replace('\xa0', '')
        minprice = int(prices.split(';')[1].split('€')[0])
        maxprice = int(prices.split(';')[1].split('-')[1].split("€")[0])
    except:
        minprice = None
        maxprice = None
    hotelreview.append(minprice)
    hotelreview.append(maxprice)
    # phonenumber
    try:
        phone = parser.find(class_="blEntry phone").get_text()
        parse_phone = "".join(phone.split())
    except:
        parse_phone = None
    hotelreview.append(parse_phone)
    # hotel information.
    hotelsinformation.append(hotelreview)
    print(hotelreview)
    return hotelsinformation

def main():
    if len(argv) == 8:
        # parameters
        url = argv[1]
        table = argv[2]
        username=argv[3]
        password = argv[4]
        dbname=argv[5]
        gmapskey=argv[6]
        numberofpages=int(argv[7])
        #tripadvisorcrwaler
        listlinks = internallinks(url, numberofpages)
        coroutine = []
        for url in listlinks:
            coroutine.append(asyncio.Task(gethotelsinfo(url,gmapskey)))
        yield from asyncio.gather(*coroutine)
        database = postgre(username, password, dbname)
        # insert
        # execute multiple inserts
        database.execute_multiple_inserts(data=coroutine, table=table, chunksize=1000)

    else:
        print("Los parametros se estan introduciendo mal los parammetros")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())