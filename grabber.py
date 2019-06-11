#!/usr/bin/python3

##
## run the code for about 2/3 days
##

import requests
import time
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

f_name = input("dataset name: ")
f = open(f_name, "a")
keys = [
    "price_usd", "24h_volume_usd", "market_cap_usd", "available_supply", "total_supply",
    "percent_change_1h", "percent_change_24h", "percent_change_7d"
]
vals = [0] * len(keys)

while True:
    done_iteration = False
    while not done_iteration:
        try:
            data = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/").json()[0]
            bstamp = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json()
            bkc = requests.get("https://blockchain.info/ticker").json()

            for d in data.keys():
                if d in keys:
                    indx = keys.index(d)
                    vals[indx] = data[d]

            for val in vals:
                f.write(val + ",")

            f.write("{},{},".format(bstamp["volume"], bstamp["vwap"]))
            f.write("{},{},{}".format(bkc["USD"]["sell"], bkc["USD"]["buy"], bkc["USD"]["15m"]))
            f.write("\n")
            f.flush()

            done_iteration = True
            time.sleep(9 * 60)

        except Exception:
            logging.exception()
            time.sleep(3)
