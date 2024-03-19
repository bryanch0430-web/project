import yfinance as yf
import ta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import datetime


def df_to_windowed_df_auto_dates(dataframe, n=7):
        
    if len(dataframe) < n + 1:
        raise ValueError(f"DataFrame 至少需要 {n+1} 行数据。")

    X, Y, dates = [], [], []

    for i in range(n, len(dataframe)):
        window = dataframe.iloc[i-n:i+1]['Close']
        date = dataframe.index[i]
        if len(window) != n + 1:
            continue
        X.append(window[:-1].values)  
        Y.append(window[-1])         
        dates.append(date)            

    windowed_df = pd.DataFrame(X, columns=[f'Close_{i}' for i in range(n)])
    windowed_df['Target'] = Y
    windowed_df['Target Date'] = dates  

    return windowed_df

# Fetch the data
BTC_Ticker = yf.Ticker("BTC-USD")
BTC_Data = BTC_Ticker.history(period="max")


del BTC_Data["Dividends"]
del BTC_Data["Stock Splits"]
BTC_Data["TomorrowClose"] = BTC_Data["Close"].shift(-1)

BTC_Data["PriceTrend"] = (BTC_Data["TomorrowClose"]>BTC_Data["Close"]).astype(int)
print(len(BTC_Data))


window=df_to_windowed_df_auto_dates(BTC_Data,7)
print(window)



print(len(BTC_Data))

print(len(window))
