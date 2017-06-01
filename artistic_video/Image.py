import numpy as np
import cv2
import scipy.misc


MEAN_PIXEL = np.array([123.68, 116.779, 103.939])


def imread(path):
    """
    :param path: a string which has the path to the image
    :return: a numpy array containing the image
    """

    # read image as bgr
    img = cv2.imread(path, cv2.IMREAD_COLOR)

    # raise error if image was not found
    if img is None:
        raise FileNotFoundError

    img = img.astype(np.float)

    # convert bgr to rgb
    img = img[..., ::-1]

    img = _preprocess(img)
    return img


def imsave(path, img):
    """
    :param path: a string with the path where the image will be saved
    :param img: a numpy array with the image
    :return: has no return value
    """
    if not (img is None):
        img = np.clip(img, 0, 255).astype(np.uint8)
        img = _postprocess(img)

        # convert rgb to bgr
        # img = img[..., ::-1]

        # save the image
        scipy.misc.imsave(path, img)
        # cv2.imwrite(path, img)


def _preprocess(image):
    return image - MEAN_PIXEL


def _postprocess(image):
    return image + MEAN_PIXEL