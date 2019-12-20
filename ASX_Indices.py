import requests, time, schedule, pandas as pd, numpy as np
from lxml import html
from datetime import datetime as dt
import re

def extract():
    webpage = requests.get('https://www.asx.com.au/asx/statistics/indexInfo.do')
    tree = html.fromstring(webpage.content)

    quote = tree.xpath('//td[@nowrap = "nowrap"]/text()')

    quote = [_.replace('\r', '') for _ in quote]
    quote = [_.replace('\n', '') for _ in quote]
    quote = [_.replace('\t', '') for _ in quote]
    quote = [_.replace('%', '') for _ in quote]
    quote = [_.replace(',', '') for _ in quote]
    quote = [_.replace(' ', '') for _ in quote]

    A = quote[2 : -1 : 3] + [quote[-1]]
    A = A[0: -1 : 2]

    data = pd.DataFrame([A])
    data['GMT10'] = dt.today().strftime('%Y-%m-%d-%H:%M:%S')

    with open('ASX_INIT15M_190701.csv', 'a', newline = '') as info:
            data.to_csv(info, header = False, index = False)
            
schedule.every(12).minutes.do(extract)
while True:
    schedule.run_pending()
    time.sleep(12)
