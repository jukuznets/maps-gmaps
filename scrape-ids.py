from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

quote_pages = ['https://realt.by/rent/flat-for-long/']

for num in range(1, 215):
    url = f'https://realt.by/rent/flat-for-long/?page={num}'
    quote_pages.append(url)

data = []

for pg in quote_pages:
    req = Request(url = pg, headers = headers)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    id_list = soup.find_all(class_='flex-grow-1 justify-content-md-end')
    for id_num in id_list:
        id_num = id_num.get_text()
        data.append((id_num[3:]))

filename = 'realt-ids'
with open(filename + '.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for val in data:
        writer.writerow([val])
