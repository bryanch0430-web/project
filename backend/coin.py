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


setTicker = "BTC-USD"
# Fetch the data
Ticker = yf.Ticker(setTicker)
df = Ticker.history(period="max")


del df["Dividends"]
del df["Stock Splits"]
df["TomorrowClose"] = df["Close"].shift(-1)

df["PriceTrend"] = (df["TomorrowClose"]>df["Close"]).astype(int)
print(len(df))


window=df_to_windowed_df_auto_dates(df,7)
print(window)



print(len(df))

print(len(window))
