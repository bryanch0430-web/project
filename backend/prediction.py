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

def UNetTimeSeries(input_shape, num_classes):
    inputs = Input(input_shape)

    # Encoder (Downsampling)
    # 1st downsample block
    c1 = Conv1D(64, 3, activation='relu', padding='same')(inputs)
    c1 = Conv1D(64, 3, activation='relu', padding='same')(c1)
    p1 = MaxPooling1D(pool_size=2)(c1)

    # 2nd downsample block
    c2 = Conv1D(128, 3, activation='relu', padding='same')(p1)
    c2 = Conv1D(128, 3, activation='relu', padding='same')(c2)
    p2 = MaxPooling1D(pool_size=2)(c2)

    # Bottleneck (no pooling)
    b = Conv1D(256, 3, activation='relu', padding='same')(p2)
    b = Conv1D(256, 3, activation='relu', padding='same')(b)

    # Decoder (Upsampling)
    # 1st upsample block
    u1 = UpSampling1D(size=2)(b)
    u1 = concatenate([u1, c2])
    c3 = Conv1D(128, 3, activation='relu', padding='same')(u1)
    c3 = Conv1D(128, 3, activation='relu', padding='same')(c3)

    # 2nd upsample block
    u2 = UpSampling1D(size=2)(c3)
    u2 = concatenate([u2, c1])
    c4 = Conv1D(64, 3, activation='relu', padding='same')(u2)
    c4 = Conv1D(64, 3, activation='relu', padding='same')(c4)

    # Output layer
    # Flatten the features or use Global Average Pooling
    flattened = tf.keras.layers.GlobalAveragePooling1D()(c4)

    # Output layer for sequence classification
    outputs = Dense(num_classes, activation='softmax')(flattened)

    model = Model(inputs=[inputs], outputs=[outputs])
    return model

def plot_distribution(y, dataset_name):
    unique, counts = np.unique(y, return_counts=True)
    print(unique, counts)
    plt.bar(unique, counts)
    plt.title(f'Distribution of classes in the {dataset_name} set')
    plt.xlabel('Class')
    plt.ylabel('Frequency')
    plt.xticks(unique, classes) 
    plt.show()

setTicker = "AAPL"
# Fetch the data
Ticker = yf.Ticker(setTicker)

start_date = '2010-01-01'

df = Ticker.history(start=start_date)
del df["Dividends"]
del df["Stock Splits"]

print(df)
window_size = 100
classes = ['up','down']
up_label = classes.index('up')
down_label = classes.index('down')




X,y=[],[]

for i in range(len(df)):
    past = df[:i+1]
    future = df[i+1:]
    
    if(len(past) < window_size or len(future) < 1):
        continue
    
    past_window = past[-window_size:]

    
    future_window = future[:1]
    today_price = past_window.iloc[-1]["Close"]
    target = future_window.iloc[0]["Close"]
    
    if target > today_price:
        label = up_label  
    else:
        label = down_label
    
    X.append(past_window.values)  
    y.append(label)
    
X, y = np.array(X), np.array(y)
print(X[:1])

#split set
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42, stratify=y_temp)


# Balance the testset
X_test_up = X_test[y_test==up_label]
X_test_down = X_test[y_test==down_label]
minlen=min(len(X_test_up),len(X_test_down))

X_test_up = X_test_up[np.random.choice(len(X_test_up), minlen, replace=False), :]
X_test_down = X_test_down[np.random.choice(len(X_test_down), minlen, replace=False), :]

X_test = np.vstack([X_test_up,X_test_down])
y_test = np.array([up_label]*minlen+[down_label]*minlen)


'''
print("Training set shape:", X_train.shape)
print("Validation set shape:", X_val.shape)
print("Balanced test set shape:", X_test.shape)


plot_distribution(y_train, 'training')
plot_distribution(y_val, 'validation')
plot_distribution(y_test, 'test')

'''
'''
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1], X_train.shape[2])),
    tf.keras.layers.LSTM(256),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(len(classes), activation='softmax')  
])

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1], X_train.shape[2])),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(len(classes), activation='softmax')
])
'''
model = UNetTimeSeries((X_train.shape[1], X_train.shape[2]), len(classes))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',  
              metrics=['accuracy'])


early_stopping_callback = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=100,  
    restore_best_weights=True
)


model.fit(X_train,tf.keras.utils.to_categorical(y_train),
          validation_data = (X_val,tf.keras.utils.to_categorical(y_val)), 
          callbacks=[early_stopping_callback],
          batch_size =2048,
          epochs=1000)


predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)  
accuracy = accuracy_score(y_test, predicted_classes)  

print(f"Model accuracy: {accuracy}")


# Save the model in the native Keras format
tf.keras.models.save_model(model, 'AAPLprediction.keras')
'''

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