from bs4 import BeautifulSoup
import requests

source  =  requests.get('http://www.espncricinfo.com/southafrica/content/player/486672.html').text

soup = BeautifulSoup(source , 'html.parser')

table = soup.find_all('table' , class_='engineTable')[1] 
for set in table.find_all('tr' , class_='data1'):
    set1 = set.td.text
    if(set1=='T20s'):
        for set2 in set.find_all('td' , nowrap="nowrap"):
            if(set2.text != 'T20s'):
                print(set2.text)