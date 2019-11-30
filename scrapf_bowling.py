from bs4 import BeautifulSoup
import requests
import pandas as pd

columns = ['player' , 'span' , 'matches' , 'innings' , 'overs' , 'maidens_earned' , 'Runs' , 'Wickets' , 'best_inns_bowling' , 'bowling_average' , 'economy_rate' , 'bowling_strike_rate' , '4_wickets_in_an_inns' ,  '5_wickets_in_an_inns' , 'catches_taken' , 'stumpings_made' ]
team_id = [289 , 825, 1026, 1863, 2285, 2461, 2614, 3505, 3672, 3867]
df = pd.DataFrame(columns =[columns])
for id in team_id:
    key = str(id)
    source = requests.get('http://stats.espncricinfo.com/ci/engine/records/averages/bowling.html?class=9;type=team;id='+key).text

    soup = BeautifulSoup(source , 'html.parser')


    table = soup.find('table' , attrs={'class':'engineTable'}).tbody
    trs = table.find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        row = [td.text.replace('\n' , '') for td in tds]
        df = df.append(pd.Series(row, index = [columns]), ignore_index = True)

df.to_csv('female_player_stats_bowling.csv' , index=False)
