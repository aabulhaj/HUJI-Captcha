import os

import PIL
import PIL.Image
import PIL.ImageTk
import numpy as np

import model_utils
import utils
from online_learning import gui_helper
from online_learning import learning_gui
from paths import CLASSIFIED_IM_PATH, NUM_DUMP_PATH

BATCH_SIZE = 32
EPOCHS = 10


def classify_image(src_path, label):
    """Moves image to the correct folder."""
    file_name = src_path.rsplit('/', 1)[1]
    os.rename(src_path, '{dir}{label}/{filename}'.format(dir=CLASSIFIED_IM_PATH, label=label, filename=file_name))


def load_digits(directory):
    files = os.listdir(directory)
    for file in files:
        digit_obj = PIL.Image.open(directory + file)
        digit = PIL.ImageTk.PhotoImage(digit_obj)
        digit_arr = utils.read_image(directory + file, utils.RGBA)

        yield digit, digit_arr, directory + file


def main():
    model = model_utils.get_last_model()

    digits_loader = load_digits(NUM_DUMP_PATH)

    batch = []
    batch_labels = []
    i = 0
    for digit, digit_arr, path in digits_loader:
        # Get CNN prediction.
        prediction = np.argmax(model.predict(digit_arr.reshape(1, 28, 28, 1)))

        # Update GUI.
        gui_helper.update_gui(digit, str(prediction), str(i))

        # Get user action and input.
        input_action, input_num = gui_helper.get_input()

        if input_action == learning_gui.USER_LABEL:
            if input_num == '':
                # Correct CNN prediction.
                classify_image(path, prediction)
                continue
            classify_image(path, input_num)
            i = (i + 1) % BATCH_SIZE

            # Add to learning batch.
            batch.append(digit_arr)
            batch_labels.append(int(input_num))

        if i == 0:
            # Send learning batch to CNN.
            X_train = np.array(batch).reshape(BATCH_SIZE, 28, 28, 1)
            y_train = np.array(batch_labels)
            model.fit(x=X_train, y=y_train, epochs=EPOCHS)
            model_utils.dump_model(model)

            # Start a new batch.
            batch = []
            batch_labels = []
            continue


if __name__ == '__main__':
    gui_helper.start_gui()
    main()
    gui_helper.close_gui()
