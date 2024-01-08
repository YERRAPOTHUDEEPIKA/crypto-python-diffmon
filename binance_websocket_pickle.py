#for Unix changed to file
#To exract Binance Prices
#pip install websocket-client
#pip install websocket-client==1.2.0
#pip install lodash-py
#pip install shared_memory_dict
import pymongo
from datetime import datetime

import websocket
import json
import time
import time
from time import sleep
import requests
from urllib.request import urlopen
import json
import atexit
import sys
import warnings
#warnings.filterwarnings("ignore")

import pickle

ourpairs = []

ourpairs.append("ETH/USDT")
ourpairs.append("BTC/USDT")
ourpairs.append("ETH/BTC")
ourpairs.append("LTC/USDT")
ourpairs.append("LTC/BTC")
ourpairs.append("LTC/USD")
ourpairs.append("BCH/USDT")
ourpairs.append("BTC/USD")
ourpairs.append("ETH/USD")
ourpairs.append("BCH/BTC")
ourpairs.append("XRP/USDT")
ourpairs.append("BNB/USDT")
ourpairs.append("USDC/USDT")
ourpairs.append("FIL/USDT")
ourpairs.append("SOL/USDT")
ourpairs.append("LDO/USDT")
ourpairs.append("ARB/USDT")
ourpairs.append("UNI/USDT")
ourpairs.append("MATIC/USDT")
ourpairs.append("ATOM/USDT")
ourpairs.append("SHIB/USDT")
ourpairs.append("DOGE/USDT")
ourpairs.append("TRX/USDT")
ourpairs.append("ADA/USDT")
ourpairs.append("GRT/USDT")
ourpairs.append("AVAX/USDT")
ourpairs.append("AAVE/USDT")
ourpairs.append("XLM/USDT")
ourpairs.append("ALGO/USDT")
ourpairs.append("ETC/USDT")
ourpairs.append("LINK/USDT")
ourpairs.append("NEAR/USDT")
ourpairs.append("DOT/USDT")
ourpairs.append("WBTC/USDT")
ourpairs.append("DAI/USDT")
ourpairs.append("UNIQ/USD")
ourpairs.append("BCH/USD")

price_array =[]
rows=37
cols=5
for i in range(0,rows):
    row=[]
    for j in range(0,cols):
        row.append('nil')
    price_array.append(row)
price_array[0][0] ="ETH/USDT"
price_array[1][0] ="BTC/USDT"
price_array[2][0] ="ETH/BTC"
price_array[3][0] ="LTC/USDT"
price_array[4][0] ="LTC/BTC"
price_array[5][0] ="LTC/USD"
price_array[6][0] ="BCH/USDT"
price_array[7][0] ="BTC/USD"
price_array[8][0] ="ETH/USD"
price_array[9][0] ="BCH/BTC"
price_array[10][0] ="XRP/USDT"
price_array[11][0] ="BNB/USDT"
price_array[12][0] ="USDC/USDT"
price_array[13][0] ="FIL/USDT"
price_array[14][0] ="SOL/USDT"
price_array[15][0] ="LDO/USDT"
price_array[16][0] ="ARB/USDT"
price_array[17][0] ="UNI/USDT"
price_array[18][0] ="MATIC/USDT"
price_array[19][0] ="ATOM/USDT"
price_array[20][0] ="SHIB/USDT"
price_array[21][0] ="DOGE/USDT"
price_array[22][0] ="TRX/USDT"
price_array[23][0] ="ADA/USDT"
price_array[24][0] ="GRT/USDT"
price_array[25][0] ="AVAX/USDT"
price_array[26][0] ="AAVE/USDT"
price_array[27][0] ="XLM/USDT"
price_array[28][0] ="ALGO/USDT"
price_array[29][0] ="ETC/USDT"
price_array[30][0] ="LINK/USDT"
price_array[31][0] ="NEAR/USDT"
price_array[32][0] ="DOT/USDT"
price_array[33][0] ="WBTC/USDT"
price_array[34][0] ="DAI/USDT"
price_array[35][0] ="UNIQ/USD"
price_array[36][0] ="BCH/USD"



def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)

def on_message(wsapp, message):
    #print(message)
    message_data = json.loads(message)
    #message_data.encode('utf-8').strip()
    #print(message_data)
    #wsapp.close()
    #print(list(message_data))
    for rec in list(message_data):
        for pair in range(0,len(ourpairs)):
            needed_pair = ourpairs[pair].replace('/','')
            for i in item_generator(rec, "s"):
                if i == needed_pair:
                    #print(i,rec['c'], rec['a'], rec['b'])
                    price_array[pair][1] = rec['c']
                    price_array[pair][2] = rec['a']
                    price_array[pair][3] = rec['b']
                    epoch_time = rec['E']
                    epoch_10 = str(epoch_time)[0: 10]
                    millisec = str(epoch_time)[-3:]
                    #price_timestamp=datetime.fromtimestamp(float(epoch_10))
 
                    price_timestamp=datetime.strptime(datetime.fromtimestamp(float(epoch_10)).strftime('%Y-%m-%dT%H:%M:%S.') + ('%s' % int(millisec)),'%Y-%m-%dT%H:%M:%S.%f')
                    #print(price_timestamp)
                    price_array[pair][4] = price_timestamp
                    binance_prices = {
                        "ExchangeName" : "Binance",
                        "PriceTimeStamp" : price_timestamp,
                        "Pair" : ourpairs[pair],
                        "Last" : rec['c'],
                        "Ask"  : rec['a'],
                        "Bid"  : rec['b']
                    }
                    #new_price_entry = Prices.insert_one(binance_prices)
                    
                #else:
                    #print("not available ", needed_pair)
    
    pickle.dump(price_array, open("binance.pickle", "wb"))
    print('price_array')
    s=input('...?')
    #myinfo = pickle.load(open("binance.pickle", "rb"))
    #print(myinfo[1][1])
    #s=input('...?')

   

if __name__ == "__main__":
    #atexit.register(lambda: wsapp.close())
    print('Binance Socket - Please do not close this cmd window or kill the process')
    #wsapp =  websocket.WebSocketApp('wss://stream.binance.com:9443/ws/'+needed_pair_lower_case+'@ticker', on_message=on_message)
    wsapp =  websocket.WebSocketApp('wss://stream.binance.com:9443/ws/!ticker@arr', on_message=on_message)
    #print('Binance Socket - Please do not close this cmd window or kill the process')
    #atexit.register(lambda: wsapp.close())
    print('before wsapp run')
    wsapp.run_forever()
    
            

#2023-08-18T12:00:17.000+00:00
