"""
This module contain all the different helper functions that would
be used within our code but do not fit in any other module.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 31/04/2023
"""

import os
import subprocess
import shutil
from dataset_storage import ROOT_DIR, READY_DIR, train_val_test_split
from models_storage import LIIF_DIR, SR3_DIR

###############################################################################
#                                                                             #
#                                 CONSTANTS                                   #
#                                                                             #
###############################################################################

DATASET_OUTPUT = os.path.join(ROOT_DIR, 'models', 'Image-Super-Resolution-via-Iterative-Refinement',
                      'dataset')
SCRIPT = os.path.join(ROOT_DIR, 'models', 'Image-Super-Resolution-via-Iterative-Refinement',
                      'data', 'prepare_data.py')
PARAMETERS = ['--path', READY_DIR, '--out', DATASET_OUTPUT, '--size', '64,256']

LIIF_DATA_DIR = os.path.join(LIIF_DIR, 'load')
SR3_DATA_DIR = os.path.join(SR3_DIR, 'dataset')

###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

def call_prepare_data(script_path:str, parameters:list) -> None:
    cmd = ['python', script_path] + parameters
    subprocess.run(cmd)


def pretrain_load(train_percent=.6, val_percent=.2, seed: int = -1) -> None:
    train_val_test_split(train_percent=train_percent, val_percent=val_percent, seed=seed)
    for elem in ('train', 'val', 'test'):
        custom_parameters = PARAMETERS.copy()
        custom_parameters[1] = os.path.join(PARAMETERS[1], elem)
        custom_parameters[3] = os.path.join(PARAMETERS[3], elem)
        print(custom_parameters)
        call_prepare_data(SCRIPT, custom_parameters)

    os.makedirs(LIIF_DATA_DIR, exist_ok=True)
    for elem in os.listdir(SR3_DATA_DIR):
        if "64_256" in elem:
            shutil.copytree(os.path.join(SR3_DATA_DIR, elem),
                            os.path.join(LIIF_DATA_DIR, elem), dirs_exist_ok=True)

###############################################################################
#                                                                             #
#                                   MAIN                                      #
#                                                                             #
###############################################################################

if __name__ == "__main__":
    pretrain_load()
