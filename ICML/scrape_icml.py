import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

df = pd.DataFrame(columns=['title', 'author', 'year', 'publication'])

urls_icml_1 = [
    ['https://proceedings.mlr.press/v162/', 2022],
    ['https://proceedings.mlr.press/v139/', 2021],
    ['https://proceedings.mlr.press/v119/', 2020],
    ['https://proceedings.mlr.press/v97/', 2019],
    ['https://proceedings.mlr.press/v80/', 2018],
    ['https://proceedings.mlr.press/v70/', 2017],
    ['https://proceedings.mlr.press/v48/', 2016],
    ['https://proceedings.mlr.press/v37/', 2015],
    ['https://proceedings.mlr.press/v32/', 2014],
    ['https://proceedings.mlr.press/v28/', 2013]
]

for tmp in urls_icml_1:
    url = tmp[0]
    year = tmp[1]
    publication = 'ICML' + str(year)
    
    response = requests.get(url)
    html = BeautifulSoup(response.content, 'html.parser')

    titles = []
    for a in html.select('.page-content .wrapper .paper .title'):
        title = str(a).replace('<p class="title">', '').replace('</p>', '')
        titles.append(title)

    authors = []
    for a in html.select('.page-content .wrapper .paper .details .authors'):
        author = str(a).replace('<span class="authors">', '').replace('</span>', '')
        authors.append(author)
    
    df_tmp = pd.DataFrame({'title':titles, 'author':authors})
    df_tmp['year'] = year
    df_tmp['publication'] = publication
    df = pd.concat([df, df_tmp])

df = df.reset_index(drop=True)

df.to_csv('./icml_tmp.csv', index=False)

