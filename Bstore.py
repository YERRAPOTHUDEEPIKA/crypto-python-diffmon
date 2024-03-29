import pymongo
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

global Prices_dbclient, Prices_db, Prices, Tolerance, Differences
Prices_dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
Prices_db = Prices_dbclient["Prices"]
Prices = Prices_db["PricesFromExchanges"]
Tolerance = Prices_db["Tolerance"]
Differences = Prices_db["Differences"]

rows, cols = (37, 2)
global tolerance_table
tolerance_table =[]
for i in range(0,rows):
	  myrow=[]
	  for j in range(0,cols):
	  	  myrow.append('')
	  tolerance_table.append(myrow)
tolerance_table[0][0] ="ETH/USDT"
tolerance_table[1][0] ="BTC/USDT"
tolerance_table[2][0] ="ETH/BTC"
tolerance_table[3][0] ="LTC/USDT"
tolerance_table[4][0] ="LTC/BTC"
tolerance_table[5][0] ="LTC/USD"
tolerance_table[6][0] ="BCH/USDT"
tolerance_table[7][0] ="BTC/USD"
tolerance_table[8][0] ="ETH/USD"
tolerance_table[9][0] ="BCH/BTC"
tolerance_table[10][0] ="XRP/USDT"
tolerance_table[11][0] ="BNB/USDT"
tolerance_table[12][0] ="USDC/USDT"
tolerance_table[13][0] ="FIL/USDT"
tolerance_table[14][0] ="SOL/USDT"
tolerance_table[15][0] ="LDO/USDT"
tolerance_table[16][0] ="ARB/USDT"
tolerance_table[17][0] ="UNI/USDT"
tolerance_table[18][0] ="MATIC/USDT"
tolerance_table[19][0] ="ATOM/USDT"
tolerance_table[20][0] ="SHIB/USDT"
tolerance_table[21][0] ="DOGE/USDT"
tolerance_table[22][0] ="TRX/USDT"
tolerance_table[23][0] ="ADA/USDT"
tolerance_table[24][0] ="GRT/USDT"
tolerance_table[25][0] ="AVAX/USDT"
tolerance_table[26][0] ="AAVE/USDT"
tolerance_table[27][0] ="XLM/USDT"
tolerance_table[28][0] ="ALGO/USDT"
tolerance_table[29][0] ="ETC/USDT"
tolerance_table[30][0] ="LINK/USDT"
tolerance_table[31][0] ="NEAR/USDT"
tolerance_table[32][0] ="DOT/USDT"
tolerance_table[33][0] ="WBTC/USDT"
tolerance_table[34][0] ="DAI/USDT"
tolerance_table[35][0] ="UNIQ/USD"
tolerance_table[36][0] ="BCH/USD"

# Store the tolerances for each currency
for i in range(0, rows):
    mypair = tolerance_table[i][0]
    findpair = list(Tolerance.find({"Pair": mypair}))

    for rec in findpair:
        tolerance_table[i][1] = float(rec.get("Tolerance"))

def store_differences():
    global Prices_dbclient, Prices_db, Prices, Tolerance, Differences

    before1min = datetime.strftime(datetime.now() - timedelta(seconds=0.5), "%Y-%m-%dT%I:%M:00.000+00:00")

    yyyy = int(before1min[0:4])
    mm = int(before1min[5:7])
    dd = int(before1min[8:10])
    hh = int(before1min[11:13])
    mts = int(before1min[14:16])

    search_from_time = datetime(yyyy, mm, dd, hh, mts, 0)
    search_to_time = datetime(yyyy, mm, dd, hh, mts, 59)

    for pair in range(0, 36):
        thispair = tolerance_table[pair][0]
        tolerance_for_pair = tolerance_table[pair][1]

        unicoindcx_last_price = 0
        unicoindcx_ask_price = 0
        unicoindcx_bid_price = 0

        binance_last_price = 0
        binance_ask_price = 0
        binance_bid_price = 0

        # Sort for the latest UnicoinDCX record
        found_unicoindcx = list(Prices.find({'PriceTimeStamp': {'$gte': search_from_time, '$lte': search_to_time},
                                             'ExchangeName': 'UnicoinDCX', 'Pair': thispair}).sort([('PriceTimeStamp', -1)]).limit(1))
        if len(found_unicoindcx) != 0:
            for unicoindcx_rec in found_unicoindcx:
                unicoindcx_last_price = unicoindcx_rec.get('Last')
                unicoindcx_ask_price = unicoindcx_rec.get('Ask')
                unicoindcx_bid_price = unicoindcx_rec.get('Bid')

        # Binance
        # Sort for the latest Binance record
        found_binance = list(Prices.find({'PriceTimeStamp': {'$gte': search_from_time, '$lte': search_to_time},
                                         'ExchangeName': 'Binance', 'Pair': thispair}).sort([('PriceTimeStamp', -1)]).limit(1))
        if len(found_binance) != 0:
            for binance_rec in found_binance:
                binance_last_price = binance_rec.get('Last')
                binance_ask_price = binance_rec.get('Ask')
                binance_bid_price = binance_rec.get('Bid')

        diff_last_with_binance = abs(binance_last_price - unicoindcx_last_price)
        diff_ask_with_binance = abs(binance_ask_price - unicoindcx_ask_price)
        diff_bid_with_binance = abs(binance_bid_price - unicoindcx_bid_price)
        max_diff_with_binance = max(diff_last_with_binance, diff_ask_with_binance, diff_bid_with_binance)

        # Check if a record with the same values already exists
        existing_record = Differences.find_one({
            'DifferenceTimeStamp': search_to_time,
            'Pair': thispair,
            'DifferenceWithExchange': 'Binance',
            'DifferenceAboveTolerance': max_diff_with_binance
        })

        if existing_record is None:
            newdiffrecord = {
                'DifferenceTimeStamp': search_to_time,
                'Pair': thispair,
                'DifferenceWithExchange': 'Binance',
                'DifferenceAboveTolerance': max_diff_with_binance
            }
            newdiffentry = Differences.insert_one(newdiffrecord)
        else:
            print('Duplicate record found and not added to the database.')

if __name__ == '__main__':
    while True:
        store_differences()
        print('Stored differences:', str(datetime.now()))
        sleep(0.5)