## The purpose of this scraper is solely created for educational testing only and it is by no mean for commercial activities.

from lxml import html
from datetime import datetime as dt
import requests, re, time, schedule, pandas as pd, numpy as np

def extract():
    ## Script Processing Timestamp
    print('Processing Time: ', dt.fromtimestamp(time.time()).strftime('%H:%M'))
    
    ## Web Request to extract HTML format
    webpage = requests.get('https://www.asx.com.au/asx/statistics/indexInfo.do')
    tree = html.fromstring(webpage.content)
    
    ## HTML transformation in filtering unneeded texts
    quote = tree.xpath('//td[@nowrap ="nowrap"]/text()')
    quote = [re.sub(r'[^0-9]', '', x) for x in quote]
    quote = [x for x in quote if x]
    
    ## Further Data Preprocessing
    c = [float(a)/10 for a in quote[1::2]]
    close = (list(c))[1::2]
    d = [float(b)/10 for b in quote[0::2]]
    last = (list(d))[0::2]
    
    ## Data Engineering (Changes)
    chg = [(b-a)/a for a,b in zip(close, last)]
    
    ## Lists Merging
    overall = last + close + chg
    
    ## Dataframe Creation
    df = (pd.DataFrame(data = [overall]).astype(float))
    df['GMT10'] = dt.today().strftime('%Y-%m-%d-%H:%M')
    
    ## Loading new data every 5 minutes in csv format
    with open('ASX.csv', 'a') as f:
        df.to_csv(f, header = False)

schedule.every(5).minutes.do(extract)
while True:
    schedule.run_pending()
    time.sleep(5)

