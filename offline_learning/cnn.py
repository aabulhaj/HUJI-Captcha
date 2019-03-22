import os

import numpy as np

import model_utils
import paths
import utils

BATCH_SIZE = 32
EPOCHS = 10


def load_data():
    captchas = []
    labels = []
    for i in range(10):
        digits_path = paths.CLASSIFIED_IM_PATH + str(i) + '/'
        digits = os.listdir(digits_path)
        for digit in digits:
            captcha = utils.read_image(digits_path + digit, utils.RGBA)
            captchas.append(captcha)
            labels.append(i)
    return np.array(captchas), np.array(labels)


def main():
    # Load data.
    captchas, labels = load_data()

    # Generate 70% random indices.
    samples_count = len(labels)
    indices = np.random.randint(0, samples_count, int(0.7 * samples_count))

    # Mask for the rest 30% of the indices.
    mask = np.ones(samples_count, dtype=bool)
    mask[indices] = False

    X_train = captchas[indices].reshape(-1, 28, 28, 1)
    y_train = labels[indices]

    X_eval = captchas[mask].reshape(-1, 28, 28, 1)
    y_eval = labels[mask]

    model = model_utils.get_model()

    model.fit(x=X_train, y=y_train, validation_data=(X_eval, y_eval), epochs=20)

    # Dumps the model, notice that by default it is dumped with the online CNN models.
    model_utils.dump_model(model)


if __name__ == '__main__':
    main()
