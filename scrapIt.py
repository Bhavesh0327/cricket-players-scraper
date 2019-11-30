from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
import re

home_page = 'http://www.espncricinfo.com/newzealand/content/player/index.html?'

Name = []
Country_Name = []
Age = []
Batting_style = []
Matches = []
Innings = []
Not_outs = []
Runs = []
Highest_score = []
Average = []
Balls_faced = []
Strike_rate = []
Hundreds = []
Fifty = []
Fours = []
Sixes = []
Catches_taken = []
Stumpings_made = []

table = {'Name': Name , 
         'Country-Name' : Country_Name , 
         'Age' : Age , 
         'Batting-style' : Batting_style , 
         'Matches' : Matches , 
         'Innings' : Innings , 
         'Not-outs' : Not_outs , 
         'Runs':Runs, 
         'Highest-score' : Highest_score , 
         'Average' :Average , 
         'Balls-faced' :Balls_faced , 
         'Strike-Rate' :Strike_rate , 
         '100s':Hundreds , 
         '50s':Fifty , 
         '4s' :Fours , 
         '6s':Sixes , 
         'Catches-taken' :Catches_taken , 
         'Stumpings-made' :Stumpings_made}

source = requests.get(home_page).text
country_links = []
soup = BeautifulSoup(source , 'html.parser')
country = soup.find('div' , class_="ciPlayersHomeCtryList")
for cn in country.find_all('li'):
    count = cn.find('a' , attrs={'href': re.compile("^index.html")} )
    if count is not None:
        count = count.get('href')
        country_links.append(count)

player_index = []
for i in country_links:
    source = requests.get('http://www.espncricinfo.com/newzealand/content/player/'+i).text
    
    soup = BeautifulSoup(source , 'html.parser')

    for main in soup.table.find_all('td' , class_='divider'):
        link = main.find('a' , attrs={'href': re.compile("^/ci/content/")} )
        link = link.get('href')
        player_index.append(link)


for player_link in player_index:
    source = requests.get('http://www.espncricinfo.com'+player_link).text
    soup = BeautifulSoup(source , 'html.parser')

    stat=[]
    name = soup.find('div', class_='ciPlayernametxt').h1.text.replace("\xa0" , '').replace("\n" ,'')
    stat.append(name)
    country = soup.find('div', class_='ciPlayernametxt').h3.text.replace("\n" , '')
    stat.append(country)
    for data in soup.find_all('p' , class_="ciPlayerinformationtxt"):
        column = data.b.text
        if(column=='Current age'):
            age = data.span.text[:2]
            stat.append(age)

        if(column=='Batting style'):
            bat_style = data.span.text.replace("\n" , '')
            stat.append(bat_style)


    for set in soup.tbody.find_all('tr' , class_='data1'):
        set1 = set.td.text
        if(set1 =='T20s'):
            for set2 in set.find_all('td' , nowrap="nowrap"):
                if(set2.text != 'T20s'):
                    stat.append(set2.text)
    if (len(stat)==18):
        Name.append(stat[0])
        Country_Name.append(stat[1])
        Age.append(stat[2])
        Batting_style.append(stat[3])
        Matches.append(stat[4])
        Innings.append(stat[5])
        Not_outs.append(stat[6])
        Runs.append(stat[7])
        Highest_score.append(stat[8])
        Average.append(stat[9])
        Balls_faced.append(stat[10])
        Strike_rate.append(stat[11])
        Hundreds.append(stat[12])
        Fifty.append(stat[13])
        Fours.append(stat[14])
        Sixes.append(stat[15])
        Catches_taken.append(stat[16])
        Stumpings_made.append(stat[17])


df = DataFrame(table, columns= ['Name' , 
                                'Country-Name'  , 
                                'Age'  , 
                                'Batting-style'  , 
                                'Matches' , 
                                'Innings' , 
                                'Not-outs'  , 
                                'Runs', 
                                'Highest-score' , 
                                'Average', 
                                'Balls-faced' , 
                                'Strike-Rate' , 
                                '100s', 
                                '50s', 
                                '4s', 
                                '6s', 
                                'Catches-taken',
                                'Stumpings-made'])

export_csv = df.to_csv (r'batting-fielding.csv', index = None, header=True) 
