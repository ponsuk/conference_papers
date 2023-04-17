import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

df = pd.DataFrame(columns=['title', 'author', 'year', 'publication'])

urls_iccv_1 = [
    'https://openaccess.thecvf.com/ICCV2021?day=all'
]

urls_iccv_2 = [
    'https://openaccess.thecvf.com/ICCV2019?day=2019-10-29',
    'https://openaccess.thecvf.com/ICCV2019?day=2019-10-30',
    'https://openaccess.thecvf.com/ICCV2019?day=2019-10-31',
    'https://openaccess.thecvf.com/ICCV2019?day=2019-11-01',
    'https://openaccess.thecvf.com/ICCV2017',
    'https://openaccess.thecvf.com/ICCV2015',
    'https://openaccess.thecvf.com/ICCV2013'
]

for url in urls_iccv_1:
    publication = url.split('.com/')[1].split('?day')[0]
    year = int(publication[4:])
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')

    titles, authors = [], []
    for a in html.select('.link2 .bibref.pre-white-space'):
        b =  str(a).split('author    = {')[1]
        c = b.split('},\n    title     = {')
        author = c[0]
        author = author.replace(', ', ' ')
        author = author.replace('and', ',')
        title = c[1].split('},\n    booktitle')[0]
        titles.append(title)
        authors.append(author)

    df_tmp = pd.DataFrame({'title':titles, 'author':authors})
    df_tmp['year'] = year
    df_tmp['publication'] = publication
    df = pd.concat([df, df_tmp])

df = df.reset_index(drop=True)

for url in urls_iccv_2:
    publication = url.split('.com/')[1][:8]
    year = int(publication[4:])
    
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')

    titles, authors = [], []
    for a in html.select('.link2 .bibref'):
        b =  str(a).split('author = {')[1]
        c = b.split('},<br/>\ntitle = {')
        author = c[0]
        author = author.replace(', ', ' ')
        author = author.replace('and', ',')
        title = c[1].split('},<br/>\nbooktitle')[0]
        titles.append(title)
        authors.append(author)
    
    df_tmp = pd.DataFrame({'title':titles, 'author':authors})
    df_tmp['year'] = year
    df_tmp['publication'] = publication
    df = pd.concat([df, df_tmp])

df = df.reset_index(drop=True)

df.to_csv('./iccv_tmp.csv', index=False)

