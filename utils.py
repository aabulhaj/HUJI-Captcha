import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread, imsave, imresize
from skimage.color import rgb2gray

GRAY_SCALE = 1
RGB = 2
RGBA = 3


def read_image(filename, representation):
    normalized_image = imread(filename).astype(np.float64) / 255

    if representation == RGB or representation == RGBA:
        return normalized_image

    if representation == GRAY_SCALE:
        return rgb2gray(normalized_image)

    raise ValueError("Error: Representation should be 1 for gray scale, 2 for RGB.")


def display_image(image, representation):
    plt.figure()
    if representation == GRAY_SCALE:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(image)
    plt.show()


def save_image(path, image):
    imsave(path, image)


def resize_image(image, size):
    return imresize(image, size)


def normalize_image(image):
    return image.astype(np.float64) / 255
