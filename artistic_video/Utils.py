import sys
from enum import Enum
from os import listdir, system, getcwd
from os.path import isfile, join, basename, splitext


class NotSupportedOS(Exception):
    pass


class NotSupportedInput(Exception):
    pass


class OS(Enum):
    WIN = 'WIN'
    LINUX = 'LINUX'


class InputType(Enum):
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'


class Default:
    CONTENT_WEIGHT = 5e0
    STYLE_WEIGHT = 1e2
    TV_WEIGHT = 1e2
    TEMPORAL_WEIGHT = 1e0
    LEARNING_RATE = 1e1
    STYLE_SCALE = 1.0
    ITERATIONS = 500
    VGG_PATH = 'imagenet-vgg-verydeep-19.mat'
    OUTPUT_FOLDER = 'output/'


SUPPORTED_IMAGE_TYPES = [".jpeg", ".jpg", ".png", ".bmp", ".tiff"]
SUPPORTED_VIDEO_TYPES = [".gif", ".mp4", ".avi"]


def get_os_type():
    """
    Decide on which OS are we running the script
    raise NotSupportedOS exception if the current OS is not supported.
    :return: OS enum type which denotes on which platform is the script running
    """
    if sys.platform.startswith("win32"):
        platform = OS.WIN
    elif sys.platform.startswith("linux"):
        platform = OS.LINUX
    else:
        raise NotSupportedOS(sys.platform + " is currently not supported!")
    return platform


def get_separator():
    return "\\" if get_os_type() == OS.WIN else "/"


def get_file_extension(path):
    _, file_extension = splitext(path)
    return file_extension


def get_input_type(path):
    """
    Decide weather the input type is IMAGE or VIDEO. Raise NotSupportedInput exception if the input type is neither
    IMAGE or VIDEO
    :param path: A string which contains a path to the input file
    :return: an InputType which can be IMAGE or VIDEO
    """
    file_extension = get_file_extension(path)
    if file_extension in SUPPORTED_IMAGE_TYPES:
        return InputType.IMAGE
    elif file_extension in SUPPORTED_VIDEO_TYPES:
        return InputType.VIDEO
    else:
        raise NotSupportedInput


def get_main_path():
    """
    Returns the working directory.
    :return: A string containing the working directory path.
    """
    return getcwd()


def get_files_from_folder(folder):
    """
    Returns a list of strings with file names from a folder.
    :param folder: A string which contains a path to a folder.
    :return: a list with the files in the folder.
    """
    return [f for f in listdir(folder) if isfile(join(folder, f))]


def get_base_name(path):
    """
    Return the file name without extension.
    :param path: A string containing the path to a file.
    :return: A string with the filename
    """
    return basename(path).split('.')[0]


def file_exists(path):
    """
    Return True if the file from the path exists.
    :param path: A string containing the path to a file.
    :return: a boolean - True if the file exists, otherwise False
    """
    return isfile(path)


def run_binary(bin_path, arguments):
    """
    Executes a binary or command line script file with arguments.
    :param bin_path: A string which contains the path of the binary/script
    :param arguments: A list of strings with the input arguments.
    :return: An integer which is the return code af the script. Usually the return code of 0 means that the
    binary/script did execute successfully.
    """
    command = bin_path
    for arg in arguments:
        command += " " + arg
    return system(command)
