from matplotlib.dates import datestr2num
import pytz
import yfinance as yf
import ta
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import datetime


setTicker = "BTC-USD"
# Fetch the data
Ticker = yf.Ticker(setTicker)
df = Ticker.history(period="max")




print(df)

df=df.filter(['Close'])  

scalar=MinMaxScaler(feature_range=(0,1))
scalared_price = scalar.fit_transform(df.values)

print(scalared_price)


X,Y=[],[]
window_size = 30
for i in range(len(scalared_price)-window_size):
    x=scalared_price[i:i+window_size]
    y=scalared_price[i+window_size]
    X.append(x)
    Y.append(y)
    
X,Y=np.array(X), np.array(Y)

print('x=',X.shape)
print('y=',Y.shape)

DS_SPILT = 0.8
size=round(X.shape[0]*DS_SPILT)
X_train, Y_train =  X[:size], Y[:size]
X_test, Y_test =  X[size:], Y[size:]



model = tf.keras.Sequential([tf.keras.layers.Input((X.shape[1],1)),
                    tf.keras.layers.LSTM(64),         
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(32, activation='relu'),                  
                    tf.keras.layers.Dense(1)])

model.compile(loss='mean_squared_error', 
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              metrics=['mean_absolute_error'])



callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss',patience=10,restore_best_weights=True)
model.fit(X_train,Y_train, validation_split=0.2, callbacks=[callback],epochs=100)

preds = model.predict(X_test)
preds = scalar.inverse_transform(preds)

train_df = df[:size+window_size]
test_df = df[size+window_size:]
test_df = test_df.assign(Pedict=preds)

plt.xlabel("Date")
plt.ylabel("Price")
plt.plot(train_df["Close"],linewidth=2)
plt.plot(test_df["Close"],linewidth=2)
plt.plot(test_df["Pedict"],linewidth=1)
plt.legend(["Train","Close","Predict"])
plt.show()

'''
def calculate_rsi(data, window_size):
    delta = data.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = up.ewm(span=window_size).mean()
    roll_down1 = down.abs().ewm(span=window_size).mean()
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    return RSI1

def calculate_macd(data, span1=12, span2=26, signal_span=9):
    ema_fast = data.ewm(span=span1, adjust=False).mean()
    ema_slow = data.ewm(span=span2, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal = macd.ewm(span=signal_span, adjust=False).mean()
    return macd, signal
'''

'''
del df["Dividends"]
del df["Stock Splits"]
df['MA_50'] = df['Close'].rolling(window=50).mean()
df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
df['RSI_14'] = calculate_rsi(df['Close'], 14)
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
 
'''