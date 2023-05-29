"""
This module contain all the different helper functions that would
be used within our code but do not fit in any other module.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 23/04/2023
"""

import os
import subprocess
from models_storage import SR3_REPO_NAME, LIIF_REPO_NAME

###############################################################################
#                                                                             #
#                                 CONSTANTS                                   #
#                                                                             #
###############################################################################

# SR3 CONFIG CONSTANTS
SR3_TRAIN_SCRIPT = "sr.py"
SR3_TEST_SCRIPT = "infer.py"
SR3_TRAIN_CONFIG = os.path.join('.', 'config', 'sr_sr3_64_256.json')
SR3_TEST_CONFIG = os.path.join('.', 'config', 'sr_sr3_64_256_test.json')

# LIIF CONFIG CONSTANTS
LIIF_TRAIN_SCRIPT = "train_liif.py"
LIIF_VAL_SCRIPT = "test.py"
LIIF_TEST_SCRIPT = "infer.py"
LIIF_TRAIN_CONFIG = os.path.join('.', 'configs', 'train-UCMerced_LandUse',
                                 'train_UCMerced_LandUse-64-256.yaml')
LIIF_OUTPUT_DIR = os.path.join('.', 'output')


###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

def train_sr3() -> None:
    """This function is meant to start SR3 training process
    """
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.join(current_dir, "models", SR3_REPO_NAME))
        subprocess.run(["python", SR3_TRAIN_SCRIPT, "-p", "train", "-c", SR3_TRAIN_CONFIG], check=True)
    finally:
        os.chdir(current_dir)


def val_sr3() -> None:
    """This function will start the SR3 model validation
    """
    current_dir = os.getcwd() 
    try:
        os.chdir(os.path.join(current_dir, "models", SR3_REPO_NAME))
        subprocess.run(["python", SR3_TRAIN_SCRIPT, "-p", "val", "-c", SR3_TRAIN_CONFIG], check=True)
    finally:
        os.chdir(current_dir)


def test_sr3() -> None:
    """This function is meant to start the SR3 infering process
    """
    current_dir = os.getcwd()                                                                                                                                                       
    try:
        os.chdir(os.path.join(current_dir, "models", SR3_REPO_NAME))
        subprocess.run(["python", SR3_TEST_SCRIPT, "-c", SR3_TEST_CONFIG], check=True)
    finally:
        os.chdir(current_dir)


def train_liif() -> None:
    """This function is meant to start liif training
    """
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.join(current_dir, "models", LIIF_REPO_NAME))
        subprocess.run(["python", LIIF_TRAIN_SCRIPT, "--config", LIIF_TRAIN_CONFIG], check=True)
    finally:
        os.chdir(current_dir)


def val_liif(model_path:str) -> None:
    """This function will start the validation process of a given trained liif model.

    Args:
        model_path (str): the path to the trained model to be used
    """
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.join(current_dir, "models", LIIF_REPO_NAME))
        full_model_path = os.path.abspath(model_path)
        if os.path.isfile(full_model_path):
            subprocess.run(["python", LIIF_VAL_SCRIPT, "--config", LIIF_TRAIN_CONFIG, '--model', model_path], check=True)
    finally:
        os.chdir(current_dir)


def test_liif(input_dir:str, model_path:str) -> None:
    """This function is meant to infer images using a given trained liif model.

    Args:
        input_dir (str): the directory containing the images to use for the inference
        model_path (str): path to the trained model to use
    """
    current_dir = os.getcwd()                                                                     
    try:
        os.chdir(os.path.join(current_dir, "models", LIIF_REPO_NAME))
        full_model_path = os.path.abspath(model_path)
        full_input_path = os.path.abspath(input_dir)
        full_output_path = os.path.abspath(LIIF_OUTPUT_DIR)
        if os.path.isfile(full_model_path) and os.path.isdir(full_input_path):
            os.makedirs(full_output_path, exist_ok=True)
            subprocess.run(["python", LIIF_TEST_SCRIPT, "--input", input_dir, '--model', model_path, '--output', LIIF_OUTPUT_DIR], check=True)
    finally:
        os.chdir(current_dir)
