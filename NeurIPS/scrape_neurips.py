import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

df = pd.DataFrame(columns=['title', 'author', 'year', 'publication'])

urls_neurips_1 = [
    'https://papers.nips.cc/paper_files/paper/2022'
]

urls_neurips_2 = [
    'https://papers.nips.cc/paper_files/paper/2021',
    'https://papers.nips.cc/paper_files/paper/2020',
    'https://papers.nips.cc/paper_files/paper/2019',
    'https://papers.nips.cc/paper_files/paper/2018',
    'https://papers.nips.cc/paper_files/paper/2017',
    'https://papers.nips.cc/paper_files/paper/2016',
    'https://papers.nips.cc/paper_files/paper/2015',
    'https://papers.nips.cc/paper_files/paper/2014',
    'https://papers.nips.cc/paper_files/paper/2013'
]

for url in urls_neurips_1:
    year = int(url.split('/')[-1])
    publication = 'NeurIPS' + str(year)
    
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')

    titles, authors = [], []
    for a in html.select('.container-fluid .paper-list .conference'):
        b =  str(a).split('title="paper title">')[1]
        c = b.split('</a> <i>')
        title = c[0]
        author = c[1].split('</i>')[0]
        titles.append(title)
        authors.append(author)
    
    df_tmp = pd.DataFrame({'title':titles, 'author':authors})
    df_tmp['year'] = year
    df_tmp['publication'] = publication
    df = pd.concat([df, df_tmp])

df = df.reset_index(drop=True)

for url in urls_neurips_2:
    year = int(url.split('/')[-1])
    publication = 'NeurIPS' + str(year)

    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')

    titles, authors = [], []
    for a in html.select('.container-fluid .paper-list .none'):
        b =  str(a).split('title="paper title">')[1]
        c = b.split('</a> <i>')
        title = c[0]
        author = c[1].split('</i>')[0]
        titles.append(title)
        authors.append(author)
    
    df_tmp = pd.DataFrame({'title':titles, 'author':authors})
    df_tmp['year'] = year
    df_tmp['publication'] = publication
    df = pd.concat([df, df_tmp])

df = df.reset_index(drop=True)

df.to_csv('./neurips_tmp.csv', index=False)

