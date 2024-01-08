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

import gc
import subprocess
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


productids = []
productids.append("ETHUSDT")
productids.append("BTCUSDT")
productids.append("ETHBTC")
productids.append("LTCUSDT")
productids.append("LTCBTC")
productids.append("LTCUSD")
productids.append("BCHUSDT")
productids.append("BTCUSD")
productids.append("ETHUSD")
productids.append("BCHBTC")
productids.append("XRPUSDT")
productids.append("BNBUSDT")
productids.append("USDCUSDT")
productids.append("FILUSDT")
productids.append("SOLUSDT")
productids.append("LDOUSDT")
productids.append("ARBUSDT")
productids.append("UNIUSDT")
productids.append("MATICUSDT")
productids.append("ATOMUSDT")
productids.append("SHIBUSDT")
productids.append("DOGEUSDT")
productids.append("TRXUSDT")
productids.append("ADAUSDT")
productids.append("GRTUSDT")
productids.append("AVAXUSDT")
productids.append("AAVEUSDT")
productids.append("XLMUSDT")
productids.append("ALGOUSDT")
productids.append("ETCUSDT")
productids.append("LINKUSDT")
productids.append("NEARUSDT")
productids.append("DOTUSDT")
productids.append("WBTCUSDT")
productids.append("DAIUSDT")
productids.append("UNIQUSD")
productids.append("BCHUSD")



price_array =[]
rows=37
cols=5
for i in range(0,rows):
    row=[]
    for j in range(0,cols):
        row.append('')
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




print('UnicoinDCX Websocket feed - do not kill')

# Initialize the price array
# (Note: This initialization is redundant as you've already done it above)
# price_array = [[pair, '', '', '', ''] for pair in ourpairs]

# Create a mapping from product ID to row index
productid_to_row = {productids[i]: i for i in range(len(productids))}

# Run the JavaScript program
result = subprocess.Popen('node pixuno.js', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
lc=0
while True:
    gc.collect()
    line = result.stdout.readline().decode('utf-8').strip()
    #print(line)
    parts = line.split(' ')

    #print(parts[0],'---',parts[1])
    if parts[0] == 'Symbol:':
        givensymbol = parts[1]
        lc = 1
    if parts[0] == 'LastPrice:':
        givenlastprice = parts[1]
        lc = 2
    if parts[0] == 'BestAskPrice:':
        givenaskprice = parts[1]
        lc = 3
    if parts[0] == 'BestBidPrice:':
        givenbidprice = parts[1]
        lc = 4
    if parts[0] == 'LastUpdate:':
        lastupdate= parts[1]
        lc = 5
    if lc == 5:
        setdata = givensymbol+'~'+givenlastprice+'~'+givenaskprice+'~'+givenbidprice+'~'+lastupdate
        #print(setdata)
        row_index = productid_to_row.get(givensymbol)
        price_array[row_index][0] = givensymbol
        price_array[row_index][1] = givenlastprice
        price_array[row_index][2] = givenaskprice
        price_array[row_index][3] = givenbidprice
        price_array[row_index][4] = lastupdate
        print(lastupdate)
        print(price_array)
        print('-----------------------')
        pickle.dump(price_array, open("unicoindcx.pickle", "wb"))
      
        s=input('?')
   