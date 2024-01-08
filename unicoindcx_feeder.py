#pip install shared_memory_dict
from shared_memory_dict import SharedMemoryDict
import time
from datetime import datetime, timedelta
from time import sleep
import requests
from urllib.request import urlopen
import json
import pymongo
import calendar
import gc
tried = False


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

smd_prices = SharedMemoryDict(name='price_array', size=8192)

api_url = 'https://trade.unicoindcx.com/api/exchange/tickers?limit=100'

Prices_dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
Prices_db = Prices_dbclient["Prices"]
Prices = Prices_db["PricesFromExchanges"]

#price_array[0][5] = ''

if __name__ == "__main__":
	print("Please do not close this window or kill this process - Unicoindcx ticker feed")
	while True:
		gc.collect()
		# Define the URL
		
		for pair in range(0,len(ourpairs)):
			needed_pair = ourpairs[pair].replace('/','')
			try:
			    # Fetch data from the URL
			    response = requests.get(api_url)
			    response.raise_for_status()  # Raise an exception for HTTP errors
			    #print(response.raise_for_status())
			    data = response.json()

			    prices_and_quantities = [
			        {
			            'last_price': item['last_price'],
			            'best_bid_price': item['best_bid_price'],
			            'best_ask_price': item['best_ask_price'],
			            'updated_at': item['updated_at'],
			            'symbol': item['symbol']['symbol']
			        }
			        for item in data['data']
			    ]

			    # Print the extracted data
			    for data in prices_and_quantities:
			        #print("Symbol for Every Data Showing Values:", data['symbol'])
			        if data['symbol'] == needed_pair:
				        #print("Last Price:", data['last_price'])
				        price_array[pair][1] = data['last_price']
				        #print("Best Ask Price:", data['best_ask_price'])
				        price_array[pair][2] = data['best_ask_price']
				        #print("Best Bid Price:", data['best_bid_price'])
				        price_array[pair][3] = data['best_bid_price']
				        #print("Updated Time:", datetime.strptime(data['updated_at']) + timedelta(seconds=19800))
				        time_formatted = datetime.strptime(data['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
				        ist_time = time_formatted + timedelta(seconds=19800)  #convert from GMT to IST
				        ist_epoch = str(calendar.timegm(ist_time.timetuple()))
				        #print(ist_epoch)
				        price_array[pair][4] = ist_epoch
				        #print(needed_pair, price_array[pair][1], price_array[pair][2], price_array[pair][3], price_array[pair][4] )

			except requests.exceptions.RequestException as e:
			    # Handle any errors that occur during the request
			    print('Error:', e)
			    
			    sleep(2)
			    continue
			except ValueError as e:
			    # Handle JSON parsing errors
			    print('Error parsing JSON:', e)
			    continue
		#print(price_array)
		smd_prices["unicoindcx_feed"] = price_array
		#print(smd_prices)

