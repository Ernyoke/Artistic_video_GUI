import numpy as np
import scipy.misc


MEAN_PIXEL = np.array([123.68,  116.779,  103.939])


def imread(path):
    try:
        img = scipy.misc.imread(path).astype(np.float)
        if len(img.shape) == 2:
            # grayscale
            img = np.dstack((img,img,img))
        return __preprocess(img)
    except FileNotFoundError as err:
        raise err


def imsave(path, img):
    if not (img is None):
        img = np.clip(img, 0, 255).astype(np.uint8)
        scipy.misc.imsave(path, __unprocess(img))


def __preprocess(image):
    return image - MEAN_PIXEL


def __unprocess(image):
    return image + MEAN_PIXEL