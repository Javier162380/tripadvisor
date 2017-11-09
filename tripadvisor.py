# -*- coding: utf-8 -*-
from requests import get
from bs4 import BeautifulSoup
import re
import googlemaps
from time import sleep
from sys import argv
from postgre import postgre

# we get all the different pages were we can see a list of all the hotels.
def internallinks(url, n):
    """This function it is perform to return a set with all the list pages of the site."""
    linkslist = set()
    request = get(url)
    parser = BeautifulSoup(request.text, 'lxml')
    for link in parser.find(class_="pageNumbers").findAll("a", href=re.compile("^(/|.*)")):
        if link.attrs['href'] is not None:
            listurl = link.attrs['href']
            link = 'https://www.tripadvisor.es' + str(listurl)
            linkslist.add(link)
        else:
            pass
    urllist = set()
    while n > 0:
        pageslinks = set()
        for i in linkslist:
            request = get(i)
            sleep(1)
            parser = BeautifulSoup(request.text, 'lxml')
            for link in parser.find(class_="pageNumbers").findAll("a", href=re.compile("^(/|.*)")):
                if link.attrs['href'] is not None:
                    listurl = link.attrs['href']
                    link = 'https://www.tripadvisor.es' + str(listurl)
                    if link not in urllist:
                        urllist.add(link)
                        pageslinks.add(link)
                    elif link not in pageslinks:
                        pass
                    else:
                        pageslinks.remove(link)
                else:
                    pass
        linkslist = set(pageslinks)
        n = n - 1
    return set(urllist)


# we get all the individual links of all the hotels
def gethotelslinks(urllist):
    """This function it is perform to retrieve a set with all the hotels pages."""
    hotelslist = set()
    for i in urllist:
        sleep(1)
        request = get(i)
        parser = BeautifulSoup(request.text, 'lxml')
        for link in parser.findAll("a", href=re.compile("^(/|.*)(?=REVIEWS)")):
            if link.attrs['href'] is not None:
                hotelurl = link.attrs['href']
                url = 'https://www.tripadvisor.es' + str(hotelurl)
                hotelslist.add(url)
            else:
                pass
    return hotelslist


def gethotelslinknopages(url):
    """This function it is perform to retrieve a set with all the hotels pages."""
    hotelslist = set()
    request = get(url)
    sleep(1)
    parser = BeautifulSoup(request.text, 'lxml')
    for link in parser.findAll("a", href=re.compile("^(/|.*)(?=REVIEWS)")):
        if link.attrs['href'] is not None:
            hotelurl = link.attrs['href']
            url = 'https://www.tripadvisor.es' + str(hotelurl)
            hotelslist.add(url)
        else:
            pass
    return hotelslist


# we extract the data we want from the hotels.
def gethotelsinfo(hotelsList,key):
    """This function it is perform to retrieve a list with all the information of the hotels"""
    #we create a google maps object.
    gmaps = googlemaps.Client(key=key)
    hotelsinformation = []
    for i in hotelsList:
        sleep(3)
        request = get(i)
        parser = BeautifulSoup(request.text, 'lxml')
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
    return hotelsinformation


# We need to insert the url compulsory , the database table were we are going to save the information,
#username, password and dbname of our PostgreSQL, and the gmaps key.
# the number of pages we want to retrieve it is optional.  
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
        # functions
        listlinks = internallinks(url, numberofpages)
        hotelslinks = gethotelslinks(listlinks)
        information = gethotelsinfo(hotelslinks,gmapskey)
        # insert
        # we create an instance of our class postgre.
        database = postgre(username, password, dbname)
        # execute multiple inserts
        database.execute_multiple_inserts(data=information, table=table, chunksize=1000)

    elif len(argv) == 7:
        # parameters
        url = argv[1]
        table = argv[2]
        username=argv[3]
        password = argv[4]
        dbname=argv[5]
        gmapskey=argv[6]
        # functions
        hotelslinks = gethotelslinknopages(url)
        information = gethotelsinfo(hotelslinks,gmapskey)
        # insert
        # we create an instance of our class postgre.
        database = postgre(username,password,dbname)
        # execute multiple inserts
        database.execute_multiple_inserts(data=information, table=table, chunksize=1000)

    else:
        print("Estas introduciendo mal los parametros")


if __name__ == "__main__":
    main()