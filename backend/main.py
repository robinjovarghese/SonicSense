import os
from pathlib import Path
import numpy as np
import tensorflow as tf  # Import TensorFlow
from extract_features import get_audio_features
from gender_model import lstm_gender_model
from age_model import lstm_age_model
from language_model import lstm_lang_model
from utils import norm_multiple
from file_io import get_data_files
import json

# Define custom metrics
def precision(y_true, y_pred):
    true_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true * y_pred, 0, 1)))
    predicted_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + tf.keras.backend.epsilon())
    return precision

def recall(y_true, y_pred):
    true_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true * y_pred, 0, 1)))
    possible_positives = tf.keras.backend.sum(tf.keras.backend.round(tf.keras.backend.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + tf.keras.backend.epsilon())
    return recall

def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    f1_score = 2 * ((p * r) / (p + r + tf.keras.backend.epsilon()))
    return f1_score

gender_labels = {
    0: "female",
    1: "male"
}

age_labels = {
    0: "fifties",
    1: "fourties",
    2: "sixties",
    3: "teens",
    4: "thirties",
    5: "twenties"
}

lang_labels = {
    0: "english",
    1: "french",
    2: "german"
}

data_path = "audio/"
models_path = "model/"

def get_gender(out_data):
    out_data = out_data[0]
    return gender_labels[int(np.argmax(out_data))]

def get_age(out_data):
    out_data = out_data[0]
    return age_labels[int(np.argmax(out_data))]

def get_lang(out_data):
    out_data = out_data[0]
    return lang_labels[int(np.argmax(out_data))]

def main_program():

    gender_weights, gender_means, gender_stddev = get_data_files(models_path, "gender", 10)
    age_weights, age_means, age_stddev = get_data_files(models_path, "age", 30)
    lang_weights, lang_means, lang_stddev = get_data_files(models_path, "lang", 20)
    np.set_printoptions(precision=3)

    num_gender_labels = len(gender_labels)
    num_age_labels = len(age_labels)
    num_lang_labels = len(lang_labels)

    # declare the models
    gender_model = lstm_gender_model(num_gender_labels)
    age_model = lstm_age_model(num_age_labels)
    lang_model = lstm_lang_model(num_lang_labels)

    # load models
    gender_model.load_weights(gender_weights)
    age_model.load_weights(age_weights)
    lang_model.load_weights(lang_weights)

    mean_paths = [gender_means, age_means, lang_means]
    stddev_paths = [gender_stddev, age_stddev, lang_stddev]

    data_files = os.listdir(data_path)

    results = []

    for data_file in data_files:
        data = get_audio_features(Path(data_path + data_file),
                                  extra_features=["delta", "delta2", "pitch"])
        data = np.array([data.T])

        data = norm_multiple(data, mean_paths, stddev_paths)

        gender_predict = gender_model.predict(data[0])
        age_predict = age_model.predict(data[1])
        lang_predict = lang_model.predict(data[2])
        
        result = {'age': get_age(age_predict).upper(), 'gender': get_gender(gender_predict).upper(), 'language': get_lang(lang_predict).upper()}
        
        results.append(result)

    return results

if __name__ == '__main__':
    results = main_program()
    print(json.dumps(results))
