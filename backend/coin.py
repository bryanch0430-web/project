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

def create_windowed_dataframe(df, start_date_str=None, window_size=3):
    # Calculate statistical features
    df['MA'] = df['Close'].rolling(window=window_size).mean()
    df['EMA'] = df['Close'].ewm(span=window_size, adjust=False).mean()
    df['Volatility'] = df['Close'].rolling(window=window_size).std()
    df['RSI'] = calculate_rsi(df['Close'], window_size)
    df['MACD'], df['Signal'] = calculate_macd(df['Close'])

    # Calculate the percentage change for the target variable
    df['Pct_Change'] = df['Close'].pct_change() * 100

    # Set the start date
    if start_date_str is None:
        start_date = df.index[window_size]
    else:
        start_date = pd.to_datetime(start_date_str)
        if start_date not in df.index:
            print(f'Error: The start date {start_date} is not in the DataFrame index.')
            return None

    # Trim the DataFrame to the start_date and drop rows with NaN values
    df = df.loc[start_date:].dropna()

    # Create lists to store the windowed data
    windowed_dates, features, labels = [], [], []
    for current_date in df.index:
        subset = df.loc[:current_date].tail(window_size + 1)
        
        if len(subset) < window_size + 1:
            continue

        windowed_dates.append(current_date)
        # Flatten the subset excluding the last 'Close' which is the label
        feature_set = subset.iloc[:-1].drop(columns=['Close', 'Pct_Change']).values.flatten()
        # Include 'Open' and 'Volume' for the current day
        feature_set = np.append(feature_set, [subset.iloc[-2]['Open'], subset.iloc[-2]['Volume']])
        # The label is the percentage change between yesterday's and today's closing prices
        label = subset.iloc[-1]['Pct_Change']

        features.append(feature_set)
        labels.append(label)

    # Create the new DataFrame
    windowed_df = pd.DataFrame(features, index=windowed_dates)
    windowed_df.insert(0, 'Target Date', windowed_dates)
    windowed_df['Target'] = labels

    # Format dates in 'Target Date' column
    windowed_df['Target Date'] = windowed_df['Target Date'].dt.strftime('%Y-%m-%d')

    return windowed_df

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

#df["PriceTrend"] = (df["TomorrowClose"]>df["Close"]).astype(int)
#print(len(df))

start_date = None #datetime.datetime(2020, 1, 1, 0, 0, tzinfo=pytz.UTC)

window_size = 2
window = create_windowed_dataframe(df,start_date,window_size)
print(window)
dates, X, y = windowed_df_to_date_X_y(window)


set1 = int(len(dates) * .85)
set2 = int(len(dates) * .9)

dates_train, X_train, y_train = dates[:set1], X[:set1], y[:set1]

dates_val, X_val, y_val = dates[set1:set2], X[set1:set2], y[set1:set2]
dates_test, X_test, y_test = dates[set2:], X[set2:], y[set2:]

model = tf.keras.Sequential([tf.keras.layers.Input((len(X), 1)),
                    tf.keras.layers.LSTM(64),         
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(32, activation='relu'),                  
                    tf.keras.layers.Dense(1)])


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