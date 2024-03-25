from matplotlib.dates import datestr2num
import pytz
from sklearn.metrics import accuracy_score
import yfinance as yf
import ta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, UpSampling1D, concatenate,Dense
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
import datetime
from tcn import TCN

setTicker = "AAPL"
# Fetch the data
Ticker = yf.Ticker(setTicker)

start_date = '2010-01-01'

df = Ticker.history(start=start_date,interval="1m")
del df["Dividends"]
del df["Stock Splits"]

print(df)
window_size = 100
classes = ['up','down']
up_label = classes.index('up')
down_label = classes.index('down')
