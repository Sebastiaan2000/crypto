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

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def get_crossover(coin, tf, mas):
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
    limit = (datetime.utcfromtimestamp((time.time()-(500*interval*60*60))))
    klines = client.get_historical_klines(str(coin), tf, str(limit))
    ma_1_dict = {}
    ma_2_dict = {}
    ma_1_array = []
    ma_2_array = []
    time_ma_1 = []
    time_ma_2 = []
    for ma_s in mas:
        for i in range(len(klines)):
            if (i > ma_s[0]):
                time_ma_1.append(klines[i][0])
            if (i > ma_s[1]):
                time_ma_2.append(klines[i][0])
                ma_1_sum = 0
                ma_2_sum = 0
                for x in klines[i-ma_s[0]:i]:
                    ma_1_sum += float(x[4])
                for x in klines[i-ma_s[1]:i]:
                    ma_2_sum += float(x[4])
                ma_1 = ma_1_sum / ma_s[0]
                ma_2 = ma_2_sum / ma_s[1]
                ma_1_array.append(ma_1)
                ma_2_array.append(ma_2)
                ma_1_dict[int(klines[i][0])] = ma_1
                ma_2_dict[int(klines[i][0])] = ma_2

        intersect(A=Point(0,0), B=Point(1,100), C=Point(0,1), D=Point(1,50))
        # check if the ma_10 crossed the ma_20
        crossovers = []
        for y in range(1, len(ma_1_array)-1):
            A=Point(time_ma_2[y-1], ma_1_array[y-1])
            B=Point(time_ma_2[y], ma_1_array[y])
            C=Point(time_ma_2[y-1], ma_2_array[y-1]) 
            D=Point(time_ma_2[y], ma_2_array[y])
            if (intersect(A,B,C,D)):
                delta_1_ma = (B.y - A.y) / (B.x - A.x)
                delta_2_ma = (D.y - C.y) / (D.x - C.x)
                if (delta_1_ma < delta_2_ma):
                    cross_direction = '-'
                if (delta_1_ma > delta_2_ma):
                    cross_direction = '+'
                #print (delta_10_ma, delta_20_ma)
                #print (A.x, B.x, C.x, D.x)
                #dt_object = datetime.utcfromtimestamp(int(time_ma_20[y-1])/1000)
                crossovers.append([cross_direction, int(time_ma_2[y-1])/1000])
        if (len(crossovers) != 0):
            last_crossover_direction = crossovers[-1][0]
            last_crossover = crossovers[-1][1]
            time_since_cross = (time.time() - (last_crossover))/(interval*60*60)
            result.append(str(last_crossover_direction))
            result.append(str(math.ceil(time_since_cross)))
        else:
            result.append('NONE')
            result.append('NONE')
    klines2 = client.get_historical_klines(str(coin), str(Client.KLINE_INTERVAL_1DAY), '15 days ago utc')
    volume_1_day = float(klines2[-2][5])
    volume_2_day = float(klines2[-3][5])
    volume_3_days = float(klines2[-2][5]) + float(klines2[-3][5]) + float(klines2[-4][5])
    volume_3_6_days = float(klines2[-5][5]) + float(klines2[-6][5]) + float(klines2[-7][5])
    volume_7_days = float(klines2[-2][5]) + float(klines2[-3][5]) + float(klines2[-4][5]) + float(klines2[-5][5]) + float(klines2[-6][5]) + float(klines2[-7][5]) + float(klines2[-8][5])
    volume_7_14_days = float(klines2[-9][5]) + float(klines2[-10][5]) + float(klines2[-11][5]) + float(klines2[-12][5]) + float(klines2[-13][5]) + float(klines2[-14][5]) + float(klines2[-15][5])
    result.append(str("{0:.2f}".format(float(klines[-1][4]))))
    result.append(str("{0:.0f}".format((float(klines[-2][5]) * float(klines[-1][4])))))
    result.append(str("{0:.2f}".format((float(volume_1_day)-float(volume_2_day)) / float(volume_2_day) * 100)) + '%')
    result.append(str("{0:.2f}".format((float(volume_3_days)-float(volume_3_6_days)) / float(volume_3_6_days) * 100)) + '%')
    result.append(str("{0:.2f}".format((float(volume_7_days)-float(volume_7_14_days)) / float(volume_7_14_days) * 100)) + '%')
    
    limit3 = (datetime.utcfromtimestamp((time.time()-(100*interval*60*60))))
    klines3 = client.get_historical_klines(str(coin), tf, str(limit3))
    volumes3 = {}
    prices3 = {}
    for i in klines3:
        volumes3[i[0]] = i[5]
        prices3[i[0]] = (float(i[2])+float(i[3]))/2
    max_volume = max(volumes3, key=volumes3.get)
    poc = prices3[max_volume]
    result.append(poc)
    df = pd.DataFrame([result], columns=['Pair', str(mas[0]), '#', str(mas[1]), '#', str(mas[2]), '#', str(mas[3]), '#', 'Price', '24 HVolume','1D', '3D', '7D', 'POC'])
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

ma_list = [[10,20], [7,20], [20,50], [20,100]]
#print ('PAIR', ma_list[0][0] , '/' , ma_list[0][1] , ' , ' ,ma_list[1][0] , '/' , ma_list[1][1])
df2 = pd.DataFrame()
for coins in new_list[::1]:
    # usage: coins list, timeframe, ma_x, ma_y
    new_result = get_crossover(coins, str(timeframe), ma_list)
    df2 = df2.append(new_result, ignore_index=True)
pd.set_option('display.max_rows', None)
df2
