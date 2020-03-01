#!/usr/bin/env python
# coding: utf-8

# In[4]:


from binance.client import Client
from datetime import datetime
import time

class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

client = Client('', '')
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
    
def get_crossover(coin, tf, ma_x, ma_y):
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
        
    klines = client.get_historical_klines(str(coin), tf, "1 Jan 2020")
    ma_10_dict = {}
    ma_20_dict = {}
    ma_10_array = []
    ma_20_array = []
    time_ma_10 = []
    time_ma_20 = []

    for i in range(len(klines)):
        if (i > ma_x):
            time_ma_10.append(klines[i][0])
        if (i > ma_y):
            time_ma_20.append(klines[i][0])
            ma_10_sum = 0
            ma_20_sum = 0
            for x in klines[i-ma_x:i]:
                ma_10_sum += float(x[4])
            for x in klines[i-ma_y:i]:
                ma_20_sum += float(x[4])
            ma_10 = ma_10_sum / ma_x
            ma_20 = ma_20_sum / ma_y
            ma_10_array.append(ma_10)
            ma_20_array.append(ma_20)
            ma_10_dict[int(klines[i][0])] = ma_10
            ma_20_dict[int(klines[i][0])] = ma_20

    intersect(A=Point(0,0), B=Point(1,100), C=Point(0,1), D=Point(1,50))
    # check if the ma_10 crossed the ma_20
    crossovers = []
    for y in range(1, len(ma_10_array)-1):
        A=Point(time_ma_20[y-1], ma_10_array[y-1])
        B=Point(time_ma_20[y], ma_10_array[y])
        C=Point(time_ma_20[y-1], ma_20_array[y-1]) 
        D=Point(time_ma_20[y], ma_20_array[y])
        if (intersect(A,B,C,D)):
            delta_10_ma = (B.y - A.y) / (B.x - A.x)
            delta_20_ma = (D.y - C.y) / (D.x - C.x)
            if (delta_10_ma < delta_20_ma):
                cross_direction = '-'
            if (delta_10_ma > delta_20_ma):
                cross_direction = '+'
            #print (delta_10_ma, delta_20_ma)
            #print (A.x, B.x, C.x, D.x)
            #dt_object = datetime.utcfromtimestamp(int(time_ma_20[y-1])/1000)
            crossovers.append([cross_direction, int(time_ma_20[y-1])/1000])
    if (len(crossovers) != 0):
        last_crossover_direction = crossovers[-1][0]
        last_crossover = crossovers[-1][1]
        time_since_cross = (time.time() - (last_crossover))/(interval*60*60)
        print (coin + ':', last_crossover_direction, time_since_cross)
    else:
        print ('NO CROSS IN SPECIFIED RANGE')
coins_list = ['BTCUSDT','ETHUSDT', 'LTCUSDT', 'BNBUSDT', 'ICXUSDT', 'VETUSDT', 'NANOUSDT', 'XRPUSDT', 'ALGOUSDT', 'EOSUSDT', 'NEOUSDT', 'ETHBTC', 'VETBTC']

for coins in coins_list:
    # usage: coins list, timeframe, ma_x, ma_y
    get_crossover(coins, '1H', 10, 20)


# In[ ]:




