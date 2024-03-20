from matplotlib.dates import datestr2num
import pytz
import yfinance as yf
import ta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import datetime


def calculate_rsi(data, window_size):
    delta = data.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    roll_up1 = up.ewm(span=window_size).mean()
    roll_down1 = down.abs().ewm(span=window_size).mean()

    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    return RSI1

def calculate_macd(data, span1=12, span2=26, signal_span=9):
    ema_fast = data.ewm(span=span1, adjust=False).mean()
    ema_slow = data.ewm(span=span2, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_span, adjust=False).mean()
    return macd, signal





def windowed_df_to_date_X_y(df):
 
    np_df = df.to_numpy()
    dates = np_df[:, 0]
    features_matrix = np_df[:, 1:-1]
    X = features_matrix.reshape((len(dates), features_matrix.shape[1], 1))
    Y = np_df[:, -1]
    print(Y)
    X = X.astype(np.float32)
    Y = Y.astype(np.float32)

    return dates, X, Y


setTicker = "BTC-USD"
# Fetch the data
Ticker = yf.Ticker(setTicker)
df = Ticker.history(period="max")
print(df)

del df["Dividends"]
del df["Stock Splits"]

df["TomorrowClose"] = df["Close"].shift(-1)
window_size = 14  
df['MA_50'] = df['Close'].rolling(window=50).mean()
df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
df['RSI_14'] = calculate_rsi(df['Close'], window_size)
macd, signal = calculate_macd(df['Close'])
df['MACD'] = macd
df['MACDSignal'] = signal
df['BollingerHigh'], df['BollingerLow'] = ta.volatility.bollinger_hband(df['Close']), ta.volatility.bollinger_lband(df['Close'])
df['VWAP'] = ta.volume.volume_weighted_average_price(df['High'], df['Low'], df['Close'], df['Volume'])
df['PivotPoint'] = (df['High'] + df['Low'] + df['Close']) / 3
df['Target'] = df['Close'].shift(-1)

df.dropna(inplace=True)

df.reset_index(inplace=True)

df.rename(columns={'Date': 'Target Date'}, inplace=True)
df = df[['Target Date'] + [col for col in df.columns if col != 'Target Date']]

df = df[[col for col in df.columns if col != 'Target'] + ['Target']]

print(df.head())

dates, X, y = windowed_df_to_date_X_y(df)


set1 = int(len(dates) * .85)
set2 = int(len(dates) * .9)

dates_train, X_train, y_train = dates[:set1], X[:set1], y[:set1]

dates_val, X_val, y_val = dates[set1:set2], X[set1:set2], y[set1:set2]
dates_test, X_test, y_test = dates[set2:], X[set2:], y[set2:]

model = tf.keras.Sequential([tf.keras.layers.Input(X.shape[1:]),
                    tf.keras.layers.LSTM(64),         
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(32, activation='relu'),                  
                    tf.keras.layers.Dense(1)])
print(len(X))
print(X.shape)

model.compile(loss='mse', 
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              metrics=['mean_absolute_error'])

model.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=32)

train_predictions = model.predict(X_train).flatten()

plt.plot(dates_train, train_predictions)
plt.plot(dates_train, y_train)
plt.legend(['Training Predictions', 'Training Observations'])
plt.show()


val_predictions = model.predict(X_val).flatten()

plt.plot(dates_val, val_predictions)
plt.plot(dates_val, y_val)
plt.legend(['Validation Predictions', 'Validation Observations'])
plt.show()

test_predictions = model.predict(X_test).flatten()

plt.plot(dates_test, test_predictions)
plt.plot(dates_test, y_test)
plt.legend(['Testing Predictions', 'Testing Observations'])
plt.show()

from sklearn.metrics import r2_score

r2 = r2_score(y_test, test_predictions)
print(f"Test R²: {r2}")