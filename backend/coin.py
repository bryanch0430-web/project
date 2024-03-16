import pandas as pd
from pycoingecko import CoinGeckoAPI
import time
import requests
# Create a CoinGeckoAPI client
cg = CoinGeckoAPI()

coins = ['bitcoin', 'ethereum', 'dopex', 'ftx-token', 'optimism',
         'jasmycoin', 'ethereum-name-service', 'solana', 'the-sandbox','Tether','dYdX']

vsCurrencies = ['usd', 'eur', 'link']

def get_coins_prices(): 
        cg = CoinGeckoAPI()
        simple_price_request = cg.get_price(ids=coins, vs_currencies='usd')
        print(simple_price_request)
        return simple_price_request 
    
