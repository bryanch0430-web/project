import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense,Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error

class BayesianLSTM(Sequential):
    def __init__(self, units, output_size, features, dropout_rate=0.5):
        super().__init__()
        self.add(LSTM(units, input_shape=(None, features), return_sequences=False))
        self.add(Dense(units, activation='relu'))
        self.dropout_rate = dropout_rate
        self.add(Dropout(dropout_rate))
        self.add(Dense(output_size))

    def predict_with_dropout(self, x, n_samples=100):
        predictions = [self(x, training=True) for _ in range(n_samples)]
        return np.array(predictions)

setTicker = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'MSTR']

# Define the function to plot results for a single ticker
def plot_ticker_results(y_test, predictions, ticker):
    mean_predictions = predictions.mean(axis=0)
    std_predictions = predictions.std(axis=0)
    
    lower_bound = (mean_predictions - std_predictions).squeeze()
    upper_bound = (mean_predictions + std_predictions).squeeze()

    plt.figure(figsize=(14, 7))
    plt.plot(y_test, label='Actual')
    plt.plot(mean_predictions.squeeze(), label='Predicted')
    plt.fill_between(range(len(y_test)), lower_bound, upper_bound, color='orange', alpha=0.3, label='Uncertainty')
    plt.title(f'Actual vs Predicted Values with Uncertainty for {ticker}')
    plt.xlabel('Time Step')
    plt.ylabel('Target Variable')
    plt.legend()
    plt.show()


dataframes = [] 

for ticker in setTicker:
    df = yf.download(ticker, start="2020-01-01", end="2023-12-31")
    df = df.dropna()
    df['RSI'] = RSIIndicator(df['Close']).rsi()
    indicator_bb = BollingerBands(df['Close'])
    df['BB_MAVG'] = indicator_bb.bollinger_mavg()
    df['BB_HBAND'] = indicator_bb.bollinger_hband()
    df['BB_LBAND'] = indicator_bb.bollinger_lband()
    df['MACD'] = MACD(df['Close']).macd()
    df['Prev Close'] = df['Close'].shift(1)
    df = df.dropna()
    df['Ticker'] = ticker
    dataframes.append(df)


for ticker_df in dataframes:
    ticker = ticker_df['Ticker'].iloc[0]
    print(f"Processing {ticker}")


    feature_names = ['Prev Close', 'Open', 'High', 'Low', 'RSI', 'BB_MAVG', 'BB_HBAND', 'BB_LBAND', 'MACD']
    X = ticker_df[feature_names].values
    y = ticker_df['Close'].values  

    timesteps = 10
    
    X_lstm = np.array([X[i - timesteps:i, :] for i in range(timesteps, len(X))])
    y_lstm = y[timesteps:]

    X_train, X_test, y_train, y_test = train_test_split(X_lstm, y_lstm, test_size=0.2, random_state=42)
    
    
    print("Length of y_test:", len(y_test))

    units = 50
    output_size = 1
    features = len(feature_names)
    model = BayesianLSTM(units=units, output_size=output_size, features=features)

    model.compile(optimizer=Adam(), loss='mse')


    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)
    
    predictions = model.predict_with_dropout(X_test, n_samples=10)

 
    mean_predictions = predictions.mean(axis=0)
    std_predictions = predictions.std(axis=0)


    if len(y_test) > len(mean_predictions):
        y_test = y_test[-len(mean_predictions):]

    assert len(y_test) == len(mean_predictions), "The length of y_test and mean_predictions must be the same"

    lower_bound = mean_predictions - std_predictions
    upper_bound = mean_predictions + std_predictions

    plot_ticker_results(y_test, predictions, ticker)