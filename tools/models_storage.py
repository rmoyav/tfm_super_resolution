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
SR3_CONFIG_FILENAME = 'sr_sr3_64_256.json'

# Liif repo
LIIF_REPO = "https://github.com/yinboc/liif.git"
LIIF_REPO_NAME = 'liif'
LIIF_CONFIG_DIR = os.path.join(ROOT_DIR, 'models', LIIF_REPO_NAME, 'config')
LIIF_TRAIN_CONFIG = "train-UCMerced_LandUse"
LIIF_TEST_CONFIG_FILENAME = "test-UCMerced_LandUse-64-256.yaml"

###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

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
        raise FileNotFoundError(f"La carpeta {LIIF_TRAIN_CONFIG} no existe en la ubicación de origen {source_folder}.")
    
    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"The config file '{LIIF_TEST_CONFIG_FILENAME}' cannot be found in '{CONFIG_DIR}'!!")

    if not os.path.exists(LIIF_CONFIG_DIR):
        os.makedirs(LIIF_CONFIG_DIR)

    destination_file = os.path.join(LIIF_CONFIG_DIR, LIIF_TEST_CONFIG_FILENAME)
    shutil.copy(source_file, destination_file)
    print(f"The config file '{LIIF_TEST_CONFIG_FILENAME}' has been copied to '{LIIF_CONFIG_DIR}'.")

    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)

    shutil.copytree(source_folder, destination_folder)
    print(f"La carpeta {LIIF_TRAIN_CONFIG} ha sido copiada a {destination_folder}.")


def copy_config_file_sr3() -> None:
    """This function is meant to copy the config file for SR3 model into
    its default configuration folder.

    Raises:
        FileNotFoundError: raised if the SR3_CONFIG_FILENAME cannot be found within CONFIG_DIR folder
    """
    source_file = os.path.join(CONFIG_DIR, SR3_CONFIG_FILENAME)
    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"The config file '{SR3_CONFIG_FILENAME}' cannot be found in '{CONFIG_DIR}'!!")

    if not os.path.exists(SR3_CONFIG_DIR):
        os.makedirs(SR3_CONFIG_DIR)

    destination_file = os.path.join(SR3_CONFIG_DIR, SR3_CONFIG_FILENAME)
    shutil.copy(source_file, destination_file)
    print(f"The config file '{SR3_CONFIG_FILENAME}' has been copied to '{SR3_CONFIG_DIR}'.")


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
