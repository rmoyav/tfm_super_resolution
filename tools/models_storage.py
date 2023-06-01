"""
This module contains the functionality to store the models to be used
in the expected path so the rest of the workflow can be executed without
problems.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 20/05/2023
"""

import os
import git
import shutil

from dataset_storage import ROOT_DIR

###############################################################################
#                                                                             #
#                                 CONSTANTS                                   #
#                                                                             #
###############################################################################

# Models' storage dir
MODELS_DIR = os.path.join(ROOT_DIR, 'models')

# Config folder
CONFIG_DIR = os.path.join(ROOT_DIR, 'model_config')

# SR3 repo
SR3_REPO = "https://github.com/Janspiry/Image-Super-Resolution-via-Iterative-Refinement.git"
SR3_REPO_NAME = 'Image-Super-Resolution-via-Iterative-Refinement'
SR3_CONFIG_DIR = os.path.join(ROOT_DIR, 'models', SR3_REPO_NAME, 'config')
SR3_CONFIG_TRAIN_FILENAME = 'sr_sr3_64_256.json'
SR3_CONFIG_TEST_FILENAME = 'sr_sr3_64_256_test.json'

# Liif repo
LIIF_REPO = "https://github.com/yinboc/liif.git"
LIIF_REPO_NAME = 'liif'
LIIF_DIR = os.path.join(ROOT_DIR, 'models', LIIF_REPO_NAME)
LIIF_CONFIG_DIR = os.path.join(ROOT_DIR, 'models', LIIF_REPO_NAME, 'configs')
LIIF_TEST_CONFIG_DIR = os.path.join(LIIF_CONFIG_DIR, 'test')
LIIF_TRAIN_CONFIG = "train-UCMerced_LandUse"
LIIF_TEST_CONFIG_FILENAME = "test-UCMerced_LandUse-64-256.yaml"
INFER_SCRIPT_NAME = "infer.py"
INFER_SCRIPT_FOLDER = os.path.join(ROOT_DIR, 'liif_script')

###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

def copy_liif_infer_file() -> None:
    """This function is meant to copy the infer.py script into the liif
    repository dir to be used after.

    Raises:
        FileNotFoundError: raised if the infer.py script file does not exist
        FileNotFoundError: raised if the liif model folder could not be found
    """
    source_file = os.path.join(INFER_SCRIPT_FOLDER, INFER_SCRIPT_NAME)

    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"The file '{INFER_SCRIPT_NAME}' could not be found at '{source_file}'!!")
    
    if not os.path.exists(LIIF_DIR):
        raise FileNotFoundError(f"The '{LIIF_DIR}' does not exist. Please download the model repositories before copying the files!!")

    destination_file = os.path.join(LIIF_DIR, INFER_SCRIPT_NAME)
    shutil.copy(source_file, destination_file)
    print(f"The config file '{INFER_SCRIPT_NAME}' has been copied to '{LIIF_DIR}'.")


def copy_config_folder_liif() -> None:
    """This function will copy the configuration for the liif model into
    its config directory.

    Raises:
        FileNotFoundError: raised if the LIIF_TRAIN_CONFIG cannot be found within CONFIG_DIR
        FileNotFoundError: raised if the LIIF_TEST_CONFIG_FILENAME cannot be found within CONFIG_DIR
    """
    source_file = os.path.join(CONFIG_DIR, LIIF_TEST_CONFIG_FILENAME)
    source_folder = os.path.join(CONFIG_DIR, LIIF_TRAIN_CONFIG)
    destination_folder = os.path.join(LIIF_CONFIG_DIR, LIIF_TRAIN_CONFIG)

    if not os.path.isdir(source_folder):
        raise FileNotFoundError(f"The folder '{LIIF_TRAIN_CONFIG}'does not exist within the path '{source_folder}'!!")
    
    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"The config file '{LIIF_TEST_CONFIG_FILENAME}' cannot be found in '{CONFIG_DIR}'!!")

    if not os.path.exists(LIIF_CONFIG_DIR):
        os.makedirs(LIIF_CONFIG_DIR)

    destination_file = os.path.join(LIIF_TEST_CONFIG_DIR, LIIF_TEST_CONFIG_FILENAME)
    shutil.copy(source_file, destination_file)
    print(f"The config file '{LIIF_TEST_CONFIG_FILENAME}' has been copied to '{LIIF_TEST_CONFIG_DIR}'.")

    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)

    shutil.copytree(source_folder, destination_folder)
    print(f"The folder '{LIIF_TRAIN_CONFIG}' has been copied to '{destination_folder}'!!")


def copy_config_files_sr3() -> None:
    """This function is meant to copy the config files for SR3 model into
    its default configuration folder.

    Raises:
        FileNotFoundError: raised if the SR3_CONFIG_FILENAME cannot be found within CONFIG_DIR folder
    """
    source_file = os.path.join(CONFIG_DIR, SR3_CONFIG_TRAIN_FILENAME)
    source_file_2 = os.path.join(CONFIG_DIR, SR3_CONFIG_TEST_FILENAME)

    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"The config file '{SR3_CONFIG_TRAIN_FILENAME}' cannot be found in '{CONFIG_DIR}'!!")
    
    if not os.path.isfile(source_file_2):
        raise FileNotFoundError(f"The config file '{SR3_CONFIG_TEST_FILENAME}' cannot be found in '{CONFIG_DIR}'!!")

    if not os.path.exists(SR3_CONFIG_DIR):
        os.makedirs(SR3_CONFIG_DIR)

    destination_file = os.path.join(SR3_CONFIG_DIR, SR3_CONFIG_TRAIN_FILENAME)
    destination_file_2 = os.path.join(SR3_CONFIG_DIR, SR3_CONFIG_TEST_FILENAME)

    shutil.copy(source_file, destination_file)
    print(f"The config file '{SR3_CONFIG_TRAIN_FILENAME}' has been copied to '{SR3_CONFIG_DIR}'.")

    shutil.copy(source_file_2, destination_file_2)
    print(f"The config file '{SR3_CONFIG_TEST_FILENAME}' has been copied to '{SR3_CONFIG_DIR}'.")


def download_repos() -> None:
    """This function will download the model repositories
    if it is not done yet.
    """
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)

    sr3_dir = os.path.join(MODELS_DIR, SR3_REPO_NAME)
    liif_dir = os.path.join(MODELS_DIR, LIIF_REPO_NAME)

    if not os.path.exists(sr3_dir):
        git.Repo.clone_from(SR3_REPO, sr3_dir)
    if not os.path.exists(liif_dir):
        git.Repo.clone_from(LIIF_REPO, liif_dir)
