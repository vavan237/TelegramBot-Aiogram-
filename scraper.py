
import requests
from bs4 import BeautifulSoup
import re
url = ''
HOST = ''




def get_html(url, params = None):
	r = requests.get(url)
	
	return r

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_ = 'iva-item-content-m2FiN')	
	cars = []
	for item in items:
		cars.append({
			"title": item.find('div', class_ = 'iva-item-titleStep-2bjuh').get_text(),
			"link": HOST + item.find('a', class_ = 'iva-item-sliderLink-2hFV_').get('href'),
			"price": item.find('span', class_ = 'price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').get_text().replace("\xa0"," "),
			"city": item.find('div', class_ = 'geo-georeferences-3or5Q text-text-1PdBw text-size-s-1PUdo').get_text(),
			
			})
		
	return cars

def add_car_id():
	html = get_html(url)
	auto_id = 'auto_id.txt'            
	cars_list = get_content(html.text)

	
	for car in cars_list: 
		
		with open(auto_id, 'r+') as f:	
			if car['link'] in f.read():
				#print ("already in")

				pass
			else:
				with open (auto_id, "a") as autoid:
					
					autoid.write(car['link'] + "\n")
					#print (car['title'], car["price"], car["city"], car["link"])	
					return car['title'], car["price"], car["city"], car["link"]		
		



		
def parse():
	
	html = get_html(url)
	if html.status_code == 200:
		cars = get_content(html.text)
		for car in cars:
			
			#print (car["title"], car["car_id"])
			return car["title"], car["price"], car["city"], car["link"]
			
	else:
		print("Error")	



add_car_id()





		
	


