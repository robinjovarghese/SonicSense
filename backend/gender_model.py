from keras import Sequential
from keras.layers import LSTM, Dense
import tensorflow as tf
from models import train_multi_epoch, train_deepnn

NUM_FEATURES = 41  # 20, 41, 39

def precision(y_true, y_pred):
    true_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + tf.keras.backend.epsilon())
    return precision

def lstm_gender_model(num_labels):
    model = Sequential()
    model.add(LSTM(100, input_shape=(35, NUM_FEATURES), dropout=0.3, return_sequences=True))
    model.add(LSTM(100, dropout=0.2))
    model.add(Dense(num_labels, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy', precision])
    return model
