import os

import numpy as np

import paths
import utils

DIGIT_SHAPE = (28, 28)
CAPTCHA_DIGIT_BACKGROUND_THRESHOLD = 0.5
DIGITS_IN_CAPTCHA = 5


def load_captcha(path):
    image_rgba = utils.read_image(path, utils.RGBA)

    image = image_rgba[:, :, 3]

    image = 1 - image
    image[image > CAPTCHA_DIGIT_BACKGROUND_THRESHOLD] = 1
    image[image <= CAPTCHA_DIGIT_BACKGROUND_THRESHOLD] = 0
    return image


def crop_captcha(image):
    black_pixels_indices = np.argwhere(image == 0)

    min_col = np.min(black_pixels_indices[:, 1])
    max_col = np.max(black_pixels_indices[:, 1])

    min_row = np.min(black_pixels_indices[:, 0])
    max_row = np.max(black_pixels_indices[:, 0])

    return image[min_row: max_row + 1, min_col: max_col + 1]


def extract_digits(directory, captchas):
    for captcha in captchas:
        image = load_captcha('{}/{}'.format(directory, captcha))
        cropped_image = crop_captcha(image)

        cols_per_digit = int(cropped_image.shape[1] / DIGITS_IN_CAPTCHA)

        for i in range(DIGITS_IN_CAPTCHA):
            digit = cropped_image[:, i * cols_per_digit: (i + 1) * cols_per_digit]
            resized_digit = utils.resize_image(digit, DIGIT_SHAPE)
            utils.save_image('{dir}{i}_{file_name}'.format(dir=paths.NUM_DUMP_PATH, i=i, file_name=captcha),
                             resized_digit)


if __name__ == '__main__':
    captchas_dir = paths.CAPTCHAS_DUMP_PATH
    captchas = os.listdir(captchas_dir)

    extract_digits(captchas_dir, captchas)
