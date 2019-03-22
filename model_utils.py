import os
import time

import tensorflow as tf
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
from keras.models import Sequential
from keras.models import model_from_json

import paths


def get_model():
    model = Sequential()
    model.add(Conv2D(28, kernel_size=(3, 3), activation=tf.nn.relu, input_shape=(28, 28, 1)))
    model.add(Conv2D(64, kernel_size=(3, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation=tf.nn.softmax))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def get_last_model(models_dir=paths.MODEL_DUMP):
    """Loads last dumped model if exists, otherwise builds a new one."""
    model_paths = os.listdir(models_dir)

    if len(model_paths) == 0:
        return get_model()

    model_dir = models_dir + max(model_paths)
    json_file = open('{dir}/model.json'.format(dir=model_dir), 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('{dir}/model.h5'.format(dir=model_dir))

    loaded_model.compile(optimizer='adam',
                         loss='sparse_categorical_crossentropy',
                         metrics=['accuracy'])

    return loaded_model


def dump_model(model, models_dir=paths.MODEL_DUMP):
    """Dumps the learnt model."""
    timestamp = time.time()
    output_dir = models_dir + str(timestamp)

    os.mkdir(output_dir)

    model_json = model.to_json()
    with open('{dir}/model.json'.format(dir=output_dir), 'w') as json_file:
        json_file.write(model_json)
    model.save_weights('{dir}/model.h5'.format(dir=output_dir))
