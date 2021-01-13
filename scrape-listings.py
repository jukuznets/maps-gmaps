from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

id_list = pd.read_csv('realt-ids.csv')
quote_pages = []

for num in id_list.values:
    url = f'https://realt.by/rent/flat-for-long/object/{str(num)[1:-1]}'
    quote_pages.append(url)

data = []

for pg in quote_pages:
    req = Request(url = pg, headers = headers)
    try:
        page = urlopen(req)
    except:
        continue
    soup = BeautifulSoup(page, 'html.parser')

    try:
        data_center = json.loads(soup.select_one('div#map-center')['data-center'])
        x_coord = data_center['position.']['x']
        y_coord = data_center['position.']['y']
    except AttributeError:
        continue

    try:
        price_block = soup.find(class_='price-block')
        price = price_block.find(class_='d-flex align-items-center fs-giant').get_text()[:-12].replace(' ', '')
    except AttributeError:
        continue
    
    try:
        address_block = soup.find(class_='d-flex align-items-center col-auto mr-sm mb-6')
        address = address_block.find(class_='color-black').get_text()
    except AttributeError:
        address = ''

    try:
        district = soup.find('a',{'class':'color-graydark'}).get_text()
    except AttributeError:
        district = ''

    try:
        metro = soup.find(class_='metro-blue').find('a').get_text()
    except AttributeError:
        try:
            metro = soup.find(class_='metro-red').find('a').get_text()
        except AttributeError:
            metro = ''
    
    data_block = soup.find_all(class_ = 'row scrolling-x-md')[0]
    try:
        rooms_num = data_block.find_all(class_='col-auto')[0].find(class_='fs-giant').find('strong').get_text()
    except IndexError or AttributeError:
        rooms_num = ''
    try:
        tot_area = data_block.find_all(class_='col-auto')[1].find(class_='fs-giant').find('strong').get_text()
    except IndexError:
        tot_area = ''
    try:
        liv_area = data_block.find_all(class_='col-auto')[2].find(class_='fs-giant').find('strong').get_text()
    except IndexError:
        liv_area = ''

    data.append((pg, price, x_coord, y_coord, address, district, metro, rooms_num, tot_area, liv_area))

filename = 'realt-listings'
columns = ['URL', 'Price, BYN', 'Lat', 'Long', 'Address', 'District', 'Metro', 'Rooms', 'Total area, sqm', 'Living area, sqm']

with open(filename + '.csv', 'w', encoding='utf-16') as csv_file:
    writer = csv.writer(csv_file, lineterminator='\n', delimiter ='\t')
    writer.writerow((columns))
    writer.writerows(data)