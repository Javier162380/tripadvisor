# -*- coding: utf-8 -*-
from requests import get
from bs4 import BeautifulSoup
import re
from time import sleep
from sys import argv
from postgre import postgre

# we get all the different pages were we can see a list of all the hotels.
def internallinks(url, n):

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
def gethotelsinfo(hotelsList):

    hotelsinformation = []

    for i in hotelsList:
        sleep(5)
        request = get(i)
        parser = BeautifulSoup(request.text, 'lxml')
        hotelreview = []
        # name
        try:
            name = parser.find(class_="heading_title").get_text()
            title = re.sub('\n', '', name)
        except:
            title = None
        hotelreview.append(title)
        # direction
        try:
            direction = parser.find(class_="content hidden").get_text('')
        except:
            direction = None
        hotelreview.append(direction)
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
            city = raw_city.split(' ')[1].replace(',','')
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


# We need to insert the url compulsory and the database table were we are going to save the information,
# the number of pages we want to retrieve it is optional.  
def main():
    if len(argv) == 4:
        # parameters
        url = argv[1]
        table = argv[2]
        numberofpages = int(argv[3])
        # functions
        listlinks = internallinks(url, numberofpages)
        hotelslinks = gethotelslinks(listlinks)
        information = gethotelsinfo(hotelslinks)
        # insert
        # we create an instance of our class postgre.
        database = postgre()
        # execute multiple inserts
        database.execute_multiple_inserts(data=information, table=table, chunksize=1000)

    elif len(argv) == 3:
        # parameters
        url = argv[1]
        table = argv[2]
        # functions
        hotelslinks = gethotelslinknopages(url)
        information = gethotelsinfo(hotelslinks)
        # insert
        # we create an instance of our class postgre.
        database = postgre()
        # execute multiple inserts
        database.execute_multiple_inserts(data=information, table=table, chunksize=1000)

    else:
        print("Estas introduciendo mal los parametros")


if __name__ == "__main__":
    main()