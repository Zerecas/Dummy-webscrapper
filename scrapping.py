from lxml import html
import requests, re, time, schedule
import pandas as pd
import numpy as np
from datetime import datetime as dt

def job():
    print('Processing Time: ', dt.fromtimestamp(time.time()).strftime('%H:%M'))
    
    webpage = requests.get('https://www.asx.com.au/asx/statistics/indexInfo.do')
    tree = html.fromstring(webpage.content)

    quote = tree.xpath('//td[@nowrap="nowrap"]/text()')
    quote = [re.sub(r'[^0-9]', '', x) for x in quote]
    quote = [x for x in quote if x]

    dft = pd.DataFrame({'ASX': quote}).astype(float)
    dft['ASX'] = dft.ASX/10
    dft = dft.loc[~(dft.ASX < 100)].reset_index().drop(columns = ['index']).iloc[0:8, :]

    df0 = dft.iloc[3:4, :].rename(columns = {'ASX' : 'ASX50_Open'}).dropna().reset_index()
    df1 = dft.iloc[2:3, :].rename(columns = {'ASX' : 'ASX50_Last'}).dropna().reset_index()
    df2 = dft.iloc[7:8, :].rename(columns = {'ASX': 'ASX200_Open'}).dropna().reset_index()
    df3 = dft.iloc[6:7, :].rename(columns = {'ASX' : 'ASX200_Last'}).dropna().reset_index()
    df = pd.concat([df0, df1, df2, df3], axis = 1).drop(columns = ['index'])

    df['ASX200_DGrowth'] = (df.ASX200_Last - df.ASX200_Open)/df.ASX200_Last
    df['ASX50_DGrowth'] =  (df.ASX50_Last - df.ASX50_Open)/df.ASX50_Last
    df['Date'] = dt.today().strftime('%Y-%m-%d-%H:%M')

    with open('ASX_Minute.csv', 'a') as f:
        df.to_csv(f, header = False)

schedule.every(1).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
