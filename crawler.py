import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://poneyxpress.com/'
home_path = 'poney_club_centre_equestre.php'
home_attribute = '?p=FR'
url = base_url + home_path + home_attribute
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
page_id_reg = re.compile(r'.*\?id\=(\d+)')
filename = 'data.csv'

def get_response(url, header=header):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

soup = get_response(url)
finds = soup.find_all('tr')
with open(filename, 'w') as file:
    for f in finds:
        try:
            if 'poney_club_centre_equestre.php?id' in f.a['href']:
                soup = get_response(base_url + f.a['href'])
                data_list = soup.find_all('p',attrs={'class':'mb5'})
                address = [data_list[0].find('span', attrs={'itemprop':'streetAddress'}).text,data_list[0].find('span', attrs={'itemprop':'postalCode'}).text,data_list[0].find('span', attrs={'itemprop':'addressLocality'}).text,data_list[0].find('span', attrs={'itemprop':'addressCountry'}).text]
                address = (' ').join(address)

                file.write(f.td.text + ',' + f.find_all('td',attrs={'class':'l'})[1].text + ',' + f.find('td',attrs={'class':'s hideonmobileportrait'}).text + ',' + address + '\n')
                print('*',end='')
        except:
            print('--------Error----------')