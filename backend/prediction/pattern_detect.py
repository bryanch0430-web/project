import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, UpSampling1D, concatenate, Dense,Flatten, Conv2D, MaxPooling2D,Dropout,BatchNormalization
from tensorflow.keras.models import Model
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout



'''
def find_double_tops_and_bottoms(data, min_distance=5, threshold=0.05, volume=None):
    peaks = []
    troughs = []
    
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            if volume is None or volume[i] > volume[i-1]:
                peaks.append((i, data[i]))
        elif data[i] < data[i-1] and data[i] < data[i+1]:
            if volume is None or volume[i] > volume[i+1]:
                troughs.append((i, data[i]))
    
    categorized_patterns = {
        'double_top_and_down': [],
        'double_bottom_and_up': []
    }

    for i in range(1, len(peaks)):
        if peaks[i][0] - peaks[i-1][0] >= min_distance and abs(peaks[i][1] - peaks[i-1][1]) / peaks[i-1][1] < threshold:
            peak_index = peaks[i][0]
            following_prices = data[peak_index+1:peak_index+1+min_distance]
            if len(following_prices) > 0:
                min_following_price = min(following_prices)
                drop_occurred = (peaks[i][1] - min_following_price) / peaks[i][1] >= threshold
                if drop_occurred:
                    categorized_patterns['double_top_and_down'].append((peaks[i-1][0], peaks[i][0]))

    for i in range(1, len(troughs)):
        if troughs[i][0] - troughs[i-1][0] >= min_distance and abs(troughs[i][1] - troughs[i-1][1]) / troughs[i-1][1] < threshold:
            trough_index = troughs[i][0]
            following_prices = data[trough_index+1:trough_index+1+min_distance]
            if len(following_prices) > 0:
                max_following_price = max(following_prices)
                rise_occurred = (max_following_price - troughs[i][1]) / troughs[i][1] >= threshold
                if rise_occurred:
                    categorized_patterns['double_bottom_and_up'].append((troughs[i-1][0], troughs[i][0]))

    return categorized_patterns

def find_double_tops_and_check_drops(data, min_distance=5, threshold=0.05):
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            peaks.append((i, data[i]))
    
    categorized_double_tops = {
        'double_top_and_down': [],
        'double_top_and_not_down': [],
        'no_double_top': []
    }

    for i in range(1, len(peaks)):
        if peaks[i][0] - peaks[i-1][0] >= min_distance and abs(peaks[i][1] - peaks[i-1][1]) / peaks[i-1][1] < threshold:
            peak_index = peaks[i][0]
            following_prices = data[peak_index+1:peak_index+1+min_distance]
            if not following_prices.empty:
                min_following_price = following_prices.min()
                drop_occurred = (peaks[i][1] - min_following_price) / peaks[i][1] >= threshold
                double_top_type = 'double_top_and_down' if drop_occurred else 'double_top_and_not_down'
                categorized_double_tops[double_top_type].append((peaks[i-1][0], peaks[i][0]))
    
    return categorized_double_tops


def calculate_significant_drop_opportunity(double_tops_and_drops):
    if not double_tops_and_drops:
        return 0  
    
    significant_drops_count = sum(1 for _, _, drop_occurred in double_tops_and_drops if drop_occurred)
    
    opportunity = significant_drops_count / len(double_tops_and_drops)
    
    return opportunity

def plot_double_tops(data, categorized_double_tops):
    plt.figure(figsize=(14,7))
    plt.plot(data.index, data.values, label='Price')

    for category, double_tops in categorized_double_tops.items():
        if category == 'double_top_and_down':
            color = 'red'
        elif category == 'double_top_and_not_down':
            color = 'green'
        else:
            continue

        for first_peak, second_peak in double_tops:
            plt.scatter(data.index[first_peak], data.values[first_peak], color=color)
            plt.scatter(data.index[second_peak], data.values[second_peak], color=color)

    plt.title('Double Tops Categorized')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


setTicker = ["AAPL", "MSFT", "GOOGL", "AMZN", "V", "MA", "TSLA", "NVDA", "PYPL", "ADBE", "INTC", "NFLX", "CSCO", "CMCSA", "PEP", "AVGO", "TMUS", "COST", "QCOM", "AMGN", "TXN", "SBUX", "INTU", "AMD", "ISRG", "GILD", "BKNG", "MDLZ", "MU", "ADP", "FISV", "REGN", "ATVI", "BTC-USD", "ETH-USD", "XRP-USD", "LTC-USD", "BCH-USD", "LINK-USD", "BNB-USD", "ADA-USD", "XLM-USD", "USDT-USD", "EOS-USD", "TRX-USD", "XMR-USD", "XTZ-USD", "NEO-USD", "MIOTA-USD", "DASH-USD", "ETC-USD", "VET-USD", "DOGE-USD", "ZEC-USD", "LSK-USD", "OMG-USD", "QTUM-USD", "ZRX-USD", "BCN-USD", "BTG-USD", "DCR-USD", "ICX-USD", "SC-USD", "STEEM-USD", "REP-USD", "GNT-USD", "WAVES-USD", "MKR-USD", "DGB-USD", "BTM-USD", "ETN-USD", "BCD-USD", "HC-USD", "KCS-USD", "ETP-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", " RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD", "KIN-USD", "RDD-USD", "XVG-USD", "NANO-USD", "BTS-USD", "XIN-USD", "XZC-USD",]
start_date = '2012-01-01'

df = yf.download(setTicker, start=start_date)



double_tops_results = {}

for ticker in setTicker:
    close_prices = df['Close'][ticker]
    categorized_double_tops = find_double_tops_and_check_drops(close_prices)
    double_tops_results[ticker] = categorized_double_tops
    
    #for category, double_tops in categorized_double_tops.items():
    #   print(f"{ticker} {category}: {len(double_tops)} occurrences")
     

X = []
y = []

max_length = max(len(df['Close'][ticker][first_peak:second_peak+1]) for ticker, categorized_double_tops in double_tops_results.items() for category, double_tops in categorized_double_tops.items() for first_peak, second_peak in double_tops)

for ticker, categorized_double_tops in double_tops_results.items():
    for category, double_tops in categorized_double_tops.items():
        for first_peak, second_peak in double_tops:
            pattern = df['Close'][ticker][first_peak:second_peak+1].values
            pattern_padded = np.pad(pattern, (0, max_length - len(pattern)), 'constant', constant_values=0)
            X.append(pattern_padded)
            y.append(category)
            
X = np.array(X)
y = np.array(y)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)


#split set
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42, stratify=y_temp)


# Balance the testset
X_test_up = X_test[y_test=='double_top_and_down']
X_test_down = X_test[y_test=='double_top_and_not_down']
#X_test_nothing = X_test[y_test=='no_double_top']
minlen=min(len(X_test_up),len(X_test_down))

X_test_up = X_test_up[np.random.choice(len(X_test_up), minlen, replace=False), :]
X_test_down = X_test_down[np.random.choice(len(X_test_down), minlen, replace=False), :]
#X_test_nothing = X_test_down[np.random.choice(len(X_test_nothing), minlen, replace=False), :]

X_test = np.vstack([X_test_up,X_test_down])#,X_test_nothing])
y_test = np.array(['double_top_and_down']*minlen+['double_top_and_not_down']*minlen+['no_double_top']*minlen)

# Reshape X_train, X_val, and X_test
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
# Do the same for X_val and X_test, assuming they were split from X and have the same feature dimension
X_val = X_val.reshape(X_val.shape[0], X_val.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

model =Sequential([
    LSTM(64, input_shape=((X_train.shape[1], X_train.shape[2])), return_sequences=True),
    Dropout(0.5),
    LSTM(32),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

early_stopping_callback = EarlyStopping(
    monitor='val_loss',
    patience=100,  
    restore_best_weights=True
)

model_checkpoint_callback = ModelCheckpoint(
    filepath='prediction_best.keras',
    save_best_only=True,
    monitor='val_loss',
    verbose=1
)

reduce_lr_callback = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    patience=10,
    verbose=1,
    mode='auto',
    min_delta=0.0001,
    cooldown=0,
    min_lr=0
)

# Fit the model
history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val), 
    callbacks=[early_stopping_callback, model_checkpoint_callback, reduce_lr_callback],
    batch_size=2048,
    epochs=1000
)


best_model = tf.keras.models.load_model('prediction_best.keras')
best_predictions = best_model.predict(X_test)
best_predicted_classes = (best_predictions > 0.5).astype(int) 
best_accuracy = accuracy_score(y_test, best_predicted_classes)

print(f"Best model accuracy: {best_accuracy}")
'''