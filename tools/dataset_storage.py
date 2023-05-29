"""
This module contain all the different helper functions that would
be used within our code but do not fit in any other module.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 20/05/2023
"""

import glob
import os
import random

import cv2


def get_root_dir() -> str:
    """This function finds the root directory's path.

    Returns:
        str: project's root directory path.
    """
    current_dir = os.getcwd()
    root_dir = current_dir

    while not os.path.isfile(os.path.join(root_dir, "README.md")):
        root_dir = os.path.dirname(root_dir)

    return root_dir

###############################################################################
#                                                                             #
#                                 CONSTANTS                                   #
#                                                                             #
###############################################################################


ROOT_DIR = get_root_dir()
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# Dataset
DATASET1_NAME = "UCMerced_LandUse"
READY_DIR = os.path.join(DATA_DIR, DATASET1_NAME+'_ready')

###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################


def create_resample_dir(source_dir: str, resample_scale: float) -> str:
    """This function creates a copy of the source_dir in a
    different path.

    Args:
        source_dir (_type_): directory to be copied
        downsample_dir (_type_): root dir where the copy will be created

    Returns:
        str: path of the new directory
    """
    directory_name = os.path.basename(source_dir)
    new_resolution = int(directory_name.split('_')[-1]) // resample_scale
    parent_dir = os.path.dirname(source_dir)
    target_directory = os.path.join(parent_dir, "lr_{}".format(new_resolution))
    os.makedirs(target_directory, exist_ok=True)
    return target_directory


def copy_imgs_in_place(images: list, destination: str) -> None:
    """This function will take a list of image paths and
    copy them into the given destination.

    Args:
        images (list): list of images
        destination (str): destination directory
    """
    for train_path in images:
        image = cv2.imread(train_path)
        new_path = os.path.join(destination, os.path.basename(train_path))
        cv2.imwrite(new_path, image)


def train_val_test_split(data_dir: str = os.path.join(DATA_DIR, DATASET1_NAME, 'Images'),
                         output_dir: str = READY_DIR, train_percent=.6, val_percent=.2,
                         seed: int = -1) -> None:
    """This function will take a given directory and loop over every subfolder randomly grouping
    the images into three groups (train, val, test) keeping the propotions as told in the
    'train_percent' and 'val_percent' parameters.

    Args:
        data_dir (str, optional): directory containing the images. Defaults to os.path.join(DATA_DIR, DATASET1_NAME).
        output_dir (str, optional): directory where the three groups of images will be stored. Defaults to READY_DIR.
        train_percent (float, optional): percentage of the total images set to train group. Defaults to .6.
        val_percent (float, optional): percentage of the total images set to val group. Defaults to .2.
        seed (int, optional): seed used to replicate the same subdivision. Defaults to -1.
    """

    if seed != -1:
        random.seed(seed)
    
    # train
    train_dir = os.path.join(output_dir, 'train')
    os.makedirs(train_dir, exist_ok=True)

    # val
    val_dir = os.path.join(output_dir, 'val')
    os.makedirs(val_dir, exist_ok=True)

    # test
    test_dir = os.path.join(output_dir, 'test')
    os.makedirs(test_dir, exist_ok=True)

    for image_type in os.listdir(data_dir):
        images_paths = sorted(glob.glob(os.path.join(data_dir, image_type, "*.tif"), recursive=False))
        image_num = len(images_paths)
        train = random.sample(images_paths, int(image_num * train_percent))
        images_paths = [x for x in images_paths if x not in train]
        val = random.sample(images_paths, int(image_num * val_percent))
        test = [x for x in images_paths if x not in val]
        copy_imgs_in_place(train, train_dir)
        copy_imgs_in_place(val, val_dir)
        copy_imgs_in_place(test, test_dir)
        train = []
        val = []
        test = []
