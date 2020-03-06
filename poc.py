#!/usr/bin/env python
# coding: utf-8

# In[14]:


from binance.client import Client
from datetime import datetime
import time
import math
import pandas as pd

class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

client = Client('', '')
tickers = client.get_all_tickers()
BTC_pairs = []
USDT_pairs = []
ETH_pairs = []
for ticker in tickers:
    if ('BTC' in ticker['symbol'][2:]):
        BTC_pairs.append(ticker['symbol'])
    if ('USDT' in ticker['symbol'][2:]):
        USDT_pairs.append(ticker['symbol'])
BTC_pairs.remove('VENBTC')
USDT_pairs.remove('VENUSDT')
BTC_pairs.remove('BCCBTC')
USDT_pairs.remove('BCCUSDT')
BTC_pairs.remove('BCHSVBTC')
USDT_pairs.remove('BCHSVUSDT')
BTC_pairs.remove('BCHABCBTC')
USDT_pairs.remove('BCHABCUSDT')
USDT_pairs.remove('USDSBUSDT')

def get_poc(coin, tf):
    result = []
    result.append(coin)
    if (tf == '1H'):
        tf = str(Client.KLINE_INTERVAL_1HOUR)
        interval = 1
    if (tf == '2H'):
        tf = str(Client.KLINE_INTERVAL_2HOUR)
        interval = 2
    if (tf == '3H'):
        tf = str(Client.KLINE_INTERVAL_3HOUR)
        interval = 3
    if (tf == '4H'):
        tf = str(Client.KLINE_INTERVAL_4HOUR)
        interval = 4
    if (tf == '6H'):
        tf = str(Client.KLINE_INTERVAL_6HOUR)
        interval = 6
    if (tf == '12H'):
        tf = str(Client.KLINE_INTERVAL_12HOUR)
        interval = 12
    if (tf == '1D'):
        tf = str(Client.KLINE_INTERVAL_1DAY)
        interval = 24
    limit = (datetime.utcfromtimestamp((time.time()-(100*interval*60*60))))
    klines = client.get_historical_klines(str(coin), tf, str(limit))
    volumes = {}
    prices = {}
    for i in klines:
        volumes[i[0]] = i[5]
        prices[i[0]] = (float(i[2])+float(i[3]))/2
    max_volume = max(volumes, key=volumes.get)
    poc = prices[max_volume]
    result.append(poc)
    df = pd.DataFrame([result], columns=['Pair', 'Point Of Control'])
    return df
        
    #return result

timeframe = input('timeframe')
pair = input ('pair')
new_list = []
coins_list = ['BTC','ETH','XRP','LTC','BCH','EOS','BNB','XTZ','LINK','ADA','XLM','XMR','DASH','NEO','ETC','TRX','ATOM','ONT','VET','BAT','WRX','ALGO','RVN','REN','KAVA','ONE','ENJ','AION','POLY','POWR','FET','TROY','MANA','DATA','ZEC','XEM','ZRX','RDN','IOST','TOMO','BLZ','LSK','PERL','WAN','ZIL','OMG','BEAM','TNT','DUSK','PPT','GRS','REP','EVX','ARN','ELF','LEND','STRAT','COS','MTH','ARPA','KMD','SNT','FUN','QLC','ONG','LRC','PIVX','VITE','PHB','ZEN','GTO','CND','BRD','AST','WPR','DLT','POE','BTS']
if (pair == 'BTC'):
    for z in coins_list[1:]:
        btc_pair = z + 'BTC'
        new_list.append(btc_pair)
    new_list.append('KNCBTC')
    new_list.append('LOOMBTC')
    new_list.append('BQXBTC')
elif (pair == 'USDT'):
    no_usdt = ['POLY', 'POWR', 'MANA', 'KMD', 'DATA', 'LEND', 'ELF', 'ARN', 'EVX','REP','GRS', 'PPT', 'TNT','BLZ','RDN','XEM', 'POE','DLT', 'WPR','AST','BRD','CND', 'ZEN', 'PHB','PIVX','LRC', 'MTH', 'QLC','SNT']
    for y in coins_list:
        if (y not in no_usdt):
            usd_pair = str(y + 'USDT')
            new_list.append(usd_pair)


df2 = pd.DataFrame()
for coins in new_list[::1]:
    new_result = get_poc(coins, str(timeframe))
    df2 = df2.append(new_result, ignore_index=True)
pd.set_option('display.max_rows', None)
df2


# In[ ]:




