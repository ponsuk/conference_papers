import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

df = pd.DataFrame(columns=['title', 'author', 'year', 'publication'])

urls_cvpr_1 = [
    'https://openaccess.thecvf.com/CVPR2022?day=all',
    'https://openaccess.thecvf.com/CVPR2021?day=all'
]

urls_cvpr_2 = [
    'https://openaccess.thecvf.com/CVPR2020?day=2020-06-16',
    'https://openaccess.thecvf.com/CVPR2020?day=2020-06-17',
    'https://openaccess.thecvf.com/CVPR2020?day=2020-06-18',
    'https://openaccess.thecvf.com/CVPR2019?day=2019-06-18',
    'https://openaccess.thecvf.com/CVPR2019?day=2019-06-19',
    'https://openaccess.thecvf.com/CVPR2019?day=2019-06-20',
    'https://openaccess.thecvf.com/CVPR2018?day=2018-06-19',
    'https://openaccess.thecvf.com/CVPR2018?day=2018-06-20',
    'https://openaccess.thecvf.com/CVPR2018?day=2018-06-21',
    'https://openaccess.thecvf.com/CVPR2017',
    'https://openaccess.thecvf.com/CVPR2016',
    'https://openaccess.thecvf.com/CVPR2015',
    'https://openaccess.thecvf.com/CVPR2014',
    'https://openaccess.thecvf.com/CVPR2013'
]

for url in urls_cvpr_1:
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

for url in urls_cvpr_2:
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

df.to_csv('./cvpr_tmp.csv', index=False)

