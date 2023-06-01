"""
This module contains all the functions related with the
automated process of training, validating and testing the models.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 31/05/2023
"""

import os
import subprocess

from models_storage import LIIF_REPO_NAME, SR3_REPO_NAME

###############################################################################
#                                                                             #
#                                 CONSTANTS                                   #
#                                                                             #
###############################################################################

# SR3 CONFIG CONSTANTS
SR3_TRAIN_SCRIPT = "sr.py"
SR3_TEST_SCRIPT = "infer.py"
SR3_CONFIG_DIR = os.path.join('.', 'config')

# LIIF CONFIG CONSTANTS
LIIF_TRAIN_SCRIPT = "train_liif.py"
LIIF_VAL_SCRIPT = "test.py"
LIIF_TEST_SCRIPT = "infer.py"
LIIF_CONFIG_DIR = os.path.join('.', 'configs', 'train-UCMerced_LandUse')
LIIF_OUTPUT_DIR = os.path.join('.', 'output')


###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

def select_file_from_config_dir(config_dir:str) -> str:
    """This function is meant to let the user choose the config file
    is going to be used in the train/val/test process.

    Args:
        config_dir (str): The configuration directory containing the config files.

    Returns:
        str: The selected config file
    """

    files = [f for f in os.listdir(config_dir) if os.path.isfile(os.path.join(config_dir, f))]

    if not files:
        print(f"There are no config files in {config_dir}")
        return

    print("You can chose between the following config files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            selection = int(input("Please, insert the number related to the config you want to use: "))
            if 1 <= selection <= len(files):
                return files[selection - 1]
            else:
                print(f"Please, select a number between 1 and {len(files)}.")
        except ValueError:
            print("Please, select a valid number or press Ctrl+c to leave.")


def train_sr3(config_file:str) -> None:
    """This function is meant to start SR3 training process
    """
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.join(current_dir, "models", SR3_REPO_NAME))
        subprocess.run(["python", SR3_TRAIN_SCRIPT, "-p", "train", "-c", os.path.join(SR3_CONFIG_DIR, config_file)], check=True)
    finally:
        os.chdir(current_dir)


def val_sr3(config_file:str) -> None:
    """This function will start the SR3 model validation
    """
    current_dir = os.getcwd() 
    try:
        os.chdir(os.path.join(current_dir, "models", SR3_REPO_NAME))
        subprocess.run(["python", SR3_TRAIN_SCRIPT, "-p", "val", "-c", os.path.join(SR3_CONFIG_DIR, config_file)], check=True)
    finally:
        os.chdir(current_dir)


def test_sr3(config_file:str) -> None:
    """This function is meant to start the SR3 infering process
    """
    current_dir = os.getcwd()                                                                                                                                                       
    try:
        os.chdir(os.path.join(current_dir, "models", SR3_REPO_NAME))
        subprocess.run(["python", SR3_TEST_SCRIPT, "-c",  os.path.join(SR3_CONFIG_DIR, config_file)], check=True)
    finally:
        os.chdir(current_dir)


def train_liif(config_file) -> None:
    """This function is meant to start liif training
    """
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.join(current_dir, "models", LIIF_REPO_NAME))
        subprocess.run(["python", LIIF_TRAIN_SCRIPT, "--config", os.path.join(LIIF_CONFIG_DIR, config_file)], check=True)
    finally:
        os.chdir(current_dir)


def val_liif(config_file: str, model_path:str) -> None:
    """This function will start the validation process of a given trained liif model.

    Args:
        model_path (str): the path to the trained model to be used
    """
    current_dir = os.getcwd()
    try:
        os.chdir(os.path.join(current_dir, "models", LIIF_REPO_NAME))
        full_model_path = os.path.abspath(model_path)
        if os.path.isfile(full_model_path):
            subprocess.run(["python", LIIF_VAL_SCRIPT, "--config", os.path.join(LIIF_CONFIG_DIR, config_file), '--model', model_path], check=True)
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
