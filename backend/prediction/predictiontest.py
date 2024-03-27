import yfinance as yf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Flatten
from sklearn.model_selection import train_test_split


start_date = '2010-01-01'

Ticker = yf.Ticker('AAPL')

df = Ticker.history( start=start_date, interval='1m')

window_size_minutes = 390*100  

X, y = [], []

for i in range(window_size_minutes, len(df)):
    window = df.iloc[i - window_size_minutes:i] 
    future_price = df.iloc[i]['Close']
    past_price = window.iloc[-1]['Close']

    label = 1 if future_price > past_price else 0
    X.append(window.values.flatten())
    y.append(label)

X = np.array(X)
y = np.array(y)

print(X[:5])




# Reshape X_train and X_test to fit the model's input shape
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42, stratify=y_temp)


# Balance the testset
X_test_up = X_test[y_test==1]
X_test_down = X_test[y_test==0]
minlen=min(len(X_test_up),len(X_test_down))

X_test_up = X_test_up[np.random.choice(len(X_test_up), minlen, replace=False), :]
X_test_down = X_test_down[np.random.choice(len(X_test_down), minlen, replace=False), :]

X_test = np.vstack([X_test_up,X_test_down])
y_test = np.array([1]*minlen+[0]*minlen)


# Define the model architecture
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1, activation='sigmoid'))



# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))



# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {loss}, Test accuracy: {accuracy}")