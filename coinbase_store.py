#To exract Binance Prices
#pip install websocket-client
#pip install websocket-client==1.2.0
#pip install lodash-py
#pip install shared_memory_dict
import pymongo
from datetime import datetime, timedelta
from shared_memory_dict import SharedMemoryDict
import websocket
import json
import time
import time
from time import sleep
import requests
from urllib.request import urlopen
import json
import atexit
import numpy as np

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
productids.append("ETH-USDT")
productids.append("BTC-USDT")
productids.append("ETH-BTC")
productids.append("LTC-USDT")
productids.append("LTC-BTC")
productids.append("LTC-USD")
productids.append("BCH-USDT")
productids.append("BTC-USD")
productids.append("ETH-USD")
productids.append("BCH-BTC")
productids.append("XRP-USDT")
productids.append("BNB-USDT")
productids.append("USDC-USDT")
productids.append("FIL-USDT")
productids.append("SOL-USDT")
productids.append("LDO-USDT")
productids.append("ARB-USDT")
productids.append("UNI-USDT")
productids.append("MATIC-USDT")
productids.append("ATOM-USDT")
productids.append("SHIB-USDT")
productids.append("DOGE-USDT")
productids.append("TRX-USDT")
productids.append("ADA-USDT")
productids.append("GRT-USDT")
productids.append("AVAX-USDT")
productids.append("AAVE-USDT")
productids.append("XLM-USDT")
productids.append("ALGO-USDT")
productids.append("ETC-USDT")
productids.append("LINK-USDT")
productids.append("NEAR-USDT")
productids.append("DOT-USDT")
productids.append("WBTC-USDT")
productids.append("DAI-USDT")
productids.append("UNIQ-USD")
productids.append("BCH-USD")



price_array =[]
rows=37
cols=4
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


np_price_array = np.array(price_array) 

#smd_prices = SharedMemoryDict(name='price_array', size=8192)


Prices_dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
Prices_db = Prices_dbclient["Prices"]
Prices = Prices_db["PricesFromExchanges"]


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

subscribe_msg = {
	'type': 'subscribe',
	'channels': [
		{
			'name': 'ticker',
			'product_ids': productids,
		},
	],
}

# Define callback functions for WebSocket events
def on_open(ws):
	print('Coinbase to db -- do not kill')
	wsapp.send(json.dumps(subscribe_msg))


def on_message(wsapp, message):
	#print(message)
	coinbase_data = json.loads(message)
	if coinbase_data['product_id'] in productids:
		product_id_with_slash = coinbase_data['product_id'].replace('-','/')
		where_in_array = list(zip(*np.where(np_price_array == product_id_with_slash)))
		for value in where_in_array:
			the_row = value[0]
		price_array[the_row][1] = coinbase_data['price']
		price_array[the_row][2] = coinbase_data['best_ask']
		price_array[the_row][3] = coinbase_data['best_bid']
		
		price_timestamp = coinbase_data['time']
		formatted_time = datetime.strptime(price_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
		ist_time = formatted_time + timedelta(seconds=19800)
		ist_time = datetime.strftime(ist_time, "%Y-%m-%dT%H:%M:%S.%fZ")
		ist_time = datetime.strptime(ist_time, "%Y-%m-%dT%H:%M:%S.%fZ")
		
		coinbase_prices = {
						"ExchangeName" : "Coinbase",
						"PriceTimeStamp" : ist_time,
						"Pair" : price_array[the_row][0],
						"Last" : float(coinbase_data['price']),
						"Ask"  : float(coinbase_data['best_ask']),
						"Bid"  : float(coinbase_data['best_bid'])
						}
		new_price_entry = Prices.insert_one(coinbase_prices)
		#print(new_price_entry)
	#print(price_array)
	
	#smd_prices["coinbase_feed"] = price_array
	#print(smd_prices["coinbase_feed"])
   

if __name__ == "__main__":
	#wsapp =  websocket.WebSocketApp('wss://stream.binance.com:9443/ws/'+needed_pair_lower_case+'@ticker', on_message=on_message)
	#wsapp =  websocket.WebSocketApp('wss://stream.binance.com:9443/ws/!ticker@arr', on_message=on_message)
	wsapp =  websocket.WebSocketApp('wss://ws-feed.exchange.coinbase.com', on_open = on_open, on_message=on_message)
	wsapp.run_forever()
	atexit.register(lambda: wsapp.close())
			
'''
{'type': 'ticker', 'sequence': 9015199026, 'product_id': 'BTC-USDT', 'price': '26479.15', 'open_24h': '28621.5', 
'volume_24h': '3525.43370625', 'low_24h': '25122.13', 'high_24h': '28633.94', 'volume_30d': '36903.98242331', 
'best_bid': '26479.15', 'best_bid_size': '0.00000405', 'best_ask': '26479.71', 'best_ask_size': '0.09280000', 
'side': 'sell', 'time': '2023-08-18T07:40:05.768672Z', 'trade_id': 14728449, 'last_size': '0.05666'}
'''

