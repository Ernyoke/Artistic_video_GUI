import os.path

IMAGE = "image"
VIDEO = "video"

SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".bmp"]
SUPPORTED_VIDEO_TYPES = [".gif", ".mp4", ".avi"]


class UnsupportedExtension(Exception):
    pass


def input_type(path):
    _, file_extension = os.path.splitext(path)
    if file_extension in SUPPORTED_IMAGE_TYPES:
        return IMAGE
    elif file_extension in SUPPORTED_VIDEO_TYPES:
        return VIDEO
    else:
        raise UnsupportedExtension
