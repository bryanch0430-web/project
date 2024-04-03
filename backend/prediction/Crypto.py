from matplotlib.dates import datestr2num
import pytz
from sklearn.metrics import accuracy_score
import yfinance as yf
import ta
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, UpSampling1D, concatenate, Dense,Flatten, Conv2D, MaxPooling2D,Dropout,BatchNormalization
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
import datetime
from tcn import TCN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau


'''def TCNTimeSeries(input_shape, num_classes):
    inputs = Input(input_shape)

    # TCN layer
    tcn_output = TCN(nb_filters=128,
                     kernel_size=3,
                     nb_stacks=1,
                     dilations=[1, 2, 4, 8, 16, 32],
                     padding='causal',
                     use_skip_connections=True,
                     dropout_rate=0.0,
                     return_sequences=False,
                     activation='relu',
                     kernel_initializer='he_normal',
                     use_batch_norm=False,
                     use_layer_norm=False,
                     use_weight_norm=False)(inputs)

    # Flatten the output or use Global Average Pooling
    flattened = tf.keras.layers.GlobalAveragePooling1D()(tcn_output)

    # Output layer for sequence classification
    outputs = Dense(num_classes, activation='softmax')(flattened)

    model = Model(inputs=[inputs], outputs=[outputs])
    return model

def LSTMTimeSeries(input_shape, num_classes):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(num_classes, activation='sigmoid'))
    return model





def inception_module_1d(x, filters):
    # 1x1 conv
    conv1 = Conv1D(filters=filters[0], kernel_size=1, activation='relu')(x)
    
    # 3x3 conv
    conv3 = Conv1D(filters=filters[1], kernel_size=1, activation='relu')(x)
    conv3 = Conv1D(filters=filters[2], kernel_size=3, padding='same', activation='relu')(conv3)
    
    # 5x5 conv
    conv5 = Conv1D(filters=filters[3], kernel_size=1, activation='relu')(x)
    conv5 = Conv1D(filters=filters[4], kernel_size=5, padding='same', activation='relu')(conv5)
    
    # 3x3 max pooling
    pool = MaxPooling1D(pool_size=3, strides=1, padding='same')(x)
    pool = Conv1D(filters=filters[5], kernel_size=1, activation='relu')(pool)
    
    # Concatenate all
    out = concatenate([conv1, conv3, conv5, pool], axis=-1)
    
    return out

def GoogleNetTimeSeries(input_shape, num_classes):
    input_layer = Input(shape=input_shape)
    
    # First convolution block
    conv1 = Conv1D(filters=64, kernel_size=7, strides=2, padding='same', activation='relu')(input_layer)
    pool1 = MaxPooling1D(pool_size=3, strides=2, padding='same')(conv1)
    norm1 = BatchNormalization()(pool1)

    # Second convolution block
    conv2_reduce = Conv1D(filters=64, kernel_size=1, activation='relu')(norm1)
    conv2 = Conv1D(filters=192, kernel_size=3, padding='same', activation='relu')(conv2_reduce)
    norm2 = BatchNormalization()(conv2)
    pool2 = MaxPooling1D(pool_size=3, strides=2)(norm2)

    # Inception 3a
    inception_3a_output = inception_module_1d(pool2, [64, 96, 128, 16, 32, 32])

    # You can add more inception modules and max pooling layers here

    # Flatten and output layer
    flatten_layer = Flatten()(inception_3a_output)
    output_layer = Dense(num_classes, activation='sigmoid')(flatten_layer)

    model = Model(inputs=input_layer, outputs=output_layer)
    return model

'''



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
    outputs = Dense(num_classes, activation='sigmoid')(flattened)

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

setTicker = "BTC-USD"
setTicker = ['BTC-USD','ETH-USD','BNB-USD','SOL-USD', 'MSTR']
# Fetch the data
# Ticker = yf.Ticker(setTicker)

start_date = '2018-01-01'

df = yf.download(setTicker, start=start_date)
#df = Ticker.history(start=start_date)

print(df)
window_size = 64
classes = ['up','down']
up_label = classes.index('up')
down_label = classes.index('down')

np.random.seed(42)
tf.random.set_seed(42)


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

y_train_onehot = to_categorical(y_train)
y_val_onehot = to_categorical(y_val)
y_test_onehot = to_categorical(y_test)

# Scaling the features
scaler = StandardScaler()
X_train_scaled = np.array([scaler.fit_transform(x) for x in X_train])
X_val_scaled = np.array([scaler.transform(x) for x in X_val])
X_test_scaled = np.array([scaler.transform(x) for x in X_test])

'''
print("Training set shape:", X_train.shape)
print("Validation set shape:", X_val.shape)
print("Balanced test set shape:", X_test.shape)

plot_distribution(y_train, 'training')
plot_distribution(y_val, 'validation')
plot_distribution(y_test, 'test')
])
'''
model = UNetTimeSeries((X_train.shape[1], X_train.shape[2]), 1)

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




tf.keras.models.save_model(model, 'prediction_final.keras')

final_model = tf.keras.models.load_model('prediction_final.keras')
final_predictions = final_model.predict(X_test)
final_predicted_classes = (final_predictions > 0.5).astype(int)
final_accuracy = accuracy_score(y_test, final_predicted_classes)


best_model = tf.keras.models.load_model('prediction_best.keras')
best_predictions = best_model.predict(X_test)
best_predicted_classes = (best_predictions > 0.5).astype(int) 
best_accuracy = accuracy_score(y_test, best_predicted_classes)

print(f"Final model accuracy: {final_accuracy}")
print(f"Best model accuracy: {best_accuracy}")

