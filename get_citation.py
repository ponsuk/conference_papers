import requests
import pandas as pd
import os
import numpy as np

def get_citation(title):
    cnt = len(title.split(' '))
    while True:
        title_list = title.split(' ')[:cnt]
        url = ' '.join(title_list)
        re = requests.get('http://api.semanticscholar.org/graph/v1/paper/search?query=' + url)
        try:
            if re.json()['total']==0:
                cnt -= 1
                if cnt == 0:
                    print(0)
                    return 0
                continue
            else:
                cnt -= 1
                paper_id = re.json()['data'][0]['paperId']
                break
        except KeyError:
            return 0

    offset = 0
    ci_num = 0
    while True:
        re = requests.get('https://api.semanticscholar.org/graph/v1/paper/' + paper_id + f'/citations?offset={offset}&limit=1000')
        try:
            ci_num += len(re.json()['data'])
        except KeyError:
            break

        try:
            next = re.json()['next']
        except KeyError:
            break

        offset = next
    print(url, ci_num)
    return ci_num

pub = input('Please enter publication in lower letter (e.g. cvpr) :')
if not os.path.isfile('./{}/{}_list.csv'.format(pub.upper(), pub)):
    df_tmp = pd.read_csv('./{}/{}_tmp.csv'.format(pub.upper(), pub))
    df_tmp['citation'] = -999
    df_tmp.to_csv('./{}/{}_list.csv'.format(pub.upper(), pub), index=False)
    del df_tmp

df = pd.read_csv('./{}/{}_list.csv'.format(pub.upper(), pub))
for i in range(len(df)):
    if (i+1)%50==0:
        print('==========================================')
        print(f'[{i+1}/{len(df)}]')
        print('==========================================')
        df.to_csv('./{}/{}_list.csv'.format(pub.upper(), pub), index=False)
    title = df['title'][i]
    if df['citation'][i] != -999:
        continue
    ci_num = get_citation(title)
    df.at[i, 'citation'] = ci_num

