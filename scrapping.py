from lxml import html
from datetime import datetime as dt
import requests, re, time, schedule, pandas as pd, numpy as np

def extract():
    print('Processing Time: ', dt.fromtimestamp(time.time()).strftime('%H:%M'))
            
    webpage = requests.get('https://www.asx.com.au/asx/statistics/indexInfo.do')
    tree = html.fromstring(webpage.content)

    quote = tree.xpath('//td[@nowrap ="nowrap"]/text()')
    quote = [re.sub(r'[^0-9]', '', x) for x in quote]
    quote = [x for x in quote if x]

    c = [float(a)/10 for a in quote[1::2]]
    close = (list(c))[1::2]
    d = [float(b)/10 for b in quote[0::2]]
    last = (list(d))[0::2]

    chg = [(b-a)/a for a,b in zip(close, last)]
    overall = last + close + chg

    df = (pd.DataFrame(data = [overall]).astype(float))
    df['GMT10'] = dt.today().strftime('%Y-%m-%d-%H:%M')

    with open('ASX3M.csv', 'a') as f:
        df.to_csv(f, header = False)

schedule.every(5).minutes.do(extract)
while True:
    schedule.run_pending()
    time.sleep(5)

