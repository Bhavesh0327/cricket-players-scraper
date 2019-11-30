from bs4 import BeautifulSoup
import requests
from pandas import DataFrame
import re

home_page = 'http://www.espncricinfo.com/newzealand/content/player/index.html?'
Name = []
Country_Name = []
Age = []
Bowling_style = []
Matches = []
Innings = []
Balls_bowled = []
Runs_conceded = []
Wickets_taken = []
Best_innings_bowling = []
Best_match_bowling = []
Bowling_Average = []
Economy_rate = []
Bowling_Strike_rate = []
Four_wickets_in_an_innings = []
Five_wickets_in_an_innings = []
Ten_wickets_in_a_match = []

table = {'Name': Name ,
         'Country-Name' : Country_Name ,
         'Age' : Age , 
         'Bowling-style' : Bowling_style , 
         'Matches' : Matches , 
         'Innings' : Innings , 
         'Balls-bowled' : Balls_bowled , 
         'Runs-conceded':Runs_conceded, 
         'Wickets-taken' : Wickets_taken ,
         'Best-innings-bowling' :Best_innings_bowling , 
         'Best-match-bowling' :Best_match_bowling ,
         'Bowling-average': Bowling_Average,
         'Economy-rate': Economy_rate,
         'Bowling_Strike-Rate' :Bowling_Strike_rate , 
         'Four-wickets-in-an-innings':Four_wickets_in_an_innings,
         'Five-wickets-in-an-innings': Five_wickets_in_an_innings,
         'Ten-wickets-in-a-match': Ten_wickets_in_a_match}

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

        if(column=='Bowling style'):
            ball_style = data.span.text.replace("\n" , '')
            stat.append(ball_style)

    tab = soup.find_all('table' , class_='engineTable')[1] 
    for set in tab.find_all('tr' , class_='data1'):
        set1 = set.td.text
        if(set1 =='T20s'):
            for set2 in set.find_all('td' , nowrap="nowrap"):
                if(set2.text != 'T20s'):
                    stat.append(set2.text)
    if (len(stat)==17):
        Name.append(stat[0])
        Country_Name.append(stat[1])
        Age.append(stat[2])
        Bowling_style.append(stat[3])
        Matches.append(stat[4])
        Innings.append(stat[5])
        Balls_bowled.append(stat[6])
        Runs_conceded.append(stat[7])
        Wickets_taken.append(stat[8])
        Best_innings_bowling.append(stat[9])
        Best_match_bowling.append(stat[10])
        Bowling_Average.append(stat[11])
        Economy_rate.append(stat[12])
        Bowling_Strike_rate.append(stat[13])
        Four_wickets_in_an_innings.append(stat[14])
        Five_wickets_in_an_innings.append(stat[15])
        Ten_wickets_in_a_match.append(stat[16])


df = DataFrame(table, columns= ['Name',
         'Country-Name'  ,
         'Age' , 
         'Bowling-style' , 
         'Matches', 
         'Innings' , 
         'Balls-bowled', 
         'Runs-conceded', 
         'Wickets-taken' ,
         'Best-innings-bowling'  , 
         'Best-match-bowling',
         'Bowling-average',
         'Economy-rate',
         'Bowling_Strike-Rate' , 
         'Four-wickets-in-an-innings',
         'Five-wickets-in-an-innings',
         'Ten-wickets-in-a-match'])

export_csv = df.to_csv (r'bowling.csv', index = None, header=True) 