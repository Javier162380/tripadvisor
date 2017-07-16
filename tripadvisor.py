

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 
from time import sleep
from sys import argv

#we get all the different pages were we can see a list of hotels.
def internallinks(url, n):

	linkslist=[]
	request=urlopen(url)
	parser=BeautifulSoup(request,'lxml')
	for link in parser.find(class_="pageNumbers").findAll("a", href=re.compile("^(/|.*)")):
		if link.attrs['href'] is not None:
			listurl=link.attrs['href']
			link='https://www.tripadvisor.es'+str(listurl)
			linkslist.append(link)
		else:
			pass
	urllist=[]
	while n>0:
		for i in linkslist:
			request=urlopen(i)
			parser=BeautifulSoup(request,'lxml')
			for link in parser.find(class_="pageNumbers").findAll("a", href=re.compile("^(/|.*)")):
				if link.attrs['href'] is not None:
					listurl=link.attrs['href']
					link='https://www.tripadvisor.es'+str(listurl)
					urllist.append(link)
				else:
					pass
		linkslist=set(urllist)
		n=n-1
	return set(urllist)

#we get all the individual links of all the hotels
def gethotelslinks(urllist):

	hotelsList=[]
	for i in urllist:
		sleep(1)
		request=urlopen(i)
		parser=BeautifulSoup(request,'lxml')
		for link in parser.findAll("a", href=re.compile("^(/|.*)")):
			if link.attrs['href'] is not None:
				hotelurl=link.attrs['href']
				if 'Hotel_Review' in hotelurl and '#REVIEWS' not in hotelurl:
					url='https://www.tripadvisor.es'+str(hotelurl)
					hotelsList.append(url)
				else:
					pass
			else:
				pass
	return set(hotelsList)

def gethotelslinknopages(url):

	hotelsList=[]
	request=urlopen(url)
	parser=BeautifulSoup(request,'lxml')
	for link in parser.findAll("a", href=re.compile("^(/|.*)")):
		if link.attrs['href'] is not None:
			hotelurl=link.attrs['href']
			if 'Hotel_Review' in hotelurl and '#REVIEWS' not in hotelurl:
				url='https://www.tripadvisor.es'+str(hotelurl)
				hotelsList.append(url)
			else:
				pass
		else:
			pass
	return set(hotelsList)

#we extract the date we want from the hotels in this case the number of rooms and name of  the hotel .
def gethotelsinfo(hotelsList):

	hotelsinformation=[]
	
	for i in hotelsList:
		info={}
		sleep(1)
		request=urlopen(i)
		parser=BeautifulSoup(request,'lxml')
		
		if str(type(parser.find(class_="list number_of_rooms")))!="<class 'NoneType'>":
			numberofrooms=parser.find(class_="list number_of_rooms").get_text().split('s')[1].split(' ')[0]
			
		else:
			pass
		if type(parser.find(class_="heading_title"))!=None:
			name=parser.find(class_="heading_title").get_text()
			title=re.sub('\n','',name)
		else:
			pass 
		info[title]=numberofrooms
		hotelsinformation.append(info)
	return hotelsinformation
#We need to insert the url complusory, the number of pages we want to retrieve it is optional.	

def main():

	
	if len(argv)==3:
		url=argv[1]
		numberofpages=int(argv[2])
		listlinks=internallinks(url,numberofpages)
		hotelslinks=gethotelslinks(listlinks)
		information=gethotelsinfo(hotelslinks)

	elif len(argv)==2:
		url=argv[1]
		hotelslinks=gethotelslinknopages(url)
		information=gethotelsinfo(hotelslinks)

	else:
		print("Estas introduciendo mal los parametros")

	print(hotelslinks)
	print(information)
if __name__=="__main__":
	main()
