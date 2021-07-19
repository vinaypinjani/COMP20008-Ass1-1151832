#Vinay Pinjani | 1151832

import requests
import json
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import unicodedata
import re
import matplotlib.pyplot as plt


# Task 1
# Some of the code is inspired from the workshops
page_limit = 200

base_url = 'http://comp20008-jh.eng.unimelb.edu.au:9889/main/'
seed_item = 'index.html'

seed_url = base_url + seed_item
page = requests.get(seed_url)
soup = BeautifulSoup(page.text, 'html.parser')

visited = {}
visited[seed_item] = True
pages_visited = 1

links = soup.findAll('a')
seed_link = soup.findAll('a', href=re.compile("^index,html"))
to_visit_relative = list(set(links) - set(seed_link))



with open('task1.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["url", "headline"])


to_visit = []
for link in to_visit_relative:
    to_visit.append(urljoin(seed_url, link['href']))

while (to_visit):
    if pages_visited == page_limit:
        break

    link = to_visit.pop(0)


    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')

    headline = soup.find('h1').text

    with open('task1.csv', mode='a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow([link, headline])

    visited[link] = True
    to_visit
    new_links = soup.findAll('a')
    for new_link in new_links:
        new_item = new_link['href']
        new_url = urljoin(link, new_item)
        if new_url not in visited and new_url not in to_visit:
            to_visit.append(new_url)
        
    pages_visited = pages_visited + 1

#************************************************************************************

# Task 2
with open("rugby.json", "r") as f:
    data = json.load(f)
names = []
for team in data['teams']:
    names.append(team["name"])

def get_page_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    page_text = soup.find('body').text
    return page_text


def find_team(url, name_list):
    page_text = get_page_text(url)
    match = re.search(r'(?:% s)' % '|'.join(name_list), page_text)
    if (match is not None):
        return match.group(0)
    return False

def find_score(url):
    page_text = get_page_text(url)
    match = re.findall(r' (100|[1-9]?[0-9])-(100|[1-9]?[0-9])', page_text)
    highest = 0
    i = 0
    high_i = 0
    if match:
        for score in match:
            
            sum_score = int(score[0]) + int(score[1])
            if sum_score > highest:
                high_i = i
                highest = sum_score
            i += 1
        return (match[high_i][0] + "-" + match[high_i][1])
    return False

web_data = csv.DictReader(open('task1.csv'))
with open('task2.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['url','headline','team','score'])

for row in web_data:
    if(find_team(row['url'], names) and find_score(row['url'])):
        with open('task2.csv', 'a', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow([row['url'], row['headline'], find_team(row['url'], names), find_score(row['url'])])

#**************************************************************************************************

# Task 3

def get_scorediff(score_str):
    scores = score_str.split("-")
    return abs(int(scores[0]) - int(scores[1]))


with open('task2.csv','r') as f:
    score_data = csv.DictReader(f)
    team_dict = {}
    for row in score_data:
         team_dict[row['team']] = []
    
with open('task2.csv','r') as f:
    score_data = csv.DictReader(f)
    for row in score_data:
        score_diff = get_scorediff(row['score'])
        team_dict[row['team']].append(score_diff)
        
with open('task2.csv') as f:
    reader = csv.DictReader(f)
    article_count = {}
    for row in reader:
        article_count[row['team']] = 0

#************************************************************

# Task 4
with open('task2.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        article_count[row['team']] += 1

article_freq = pd.Series(data=article_count)

article_freq.nlargest().plot(kind='bar')
article_freq.nlargest().plot(color='pink')
plt.ylabel("Article Count")
plt.xlabel("Team")
plt.savefig('task4.png')
     

#***********************************************************************************

# Task 5

with open('task3.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['team', 'avg_game_difference'])

for (team, scores) in team_dict.items():
    avg_score = sum(scores) / len(scores)
    with open('task3.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([team, avg_score])


game_diff = {}
with open('task3.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        game_diff[row['team']] = float(row['avg_game_difference'])





comb_data = pd.DataFrame({'game_diff': game_diff, 'article_freq': article_freq})


comb_data.plot(kind='scatter', x='game_diff', y='article_freq', color='purple')
plt.savefig('task5.png')