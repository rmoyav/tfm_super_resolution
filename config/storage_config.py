"""
This is a configuration file to store diferent storage config
variables and constants.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 23/04/2023
"""

import os
from tools.dataset_storage import get_root_dir

USE_DEFAULT_PATHS = True
ROOT_DIR = get_root_dir()
DATA_DIR = os.path.join(ROOT_DIR, 'data')

DATASET1_NAME = "UCMerced_LandUse"
DATASET1_DIR = os.path.join(DATA_DIR, DATASET1_NAME)
DATASET1_DIR_READY = os.path.join(DATA_DIR, (DATASET1_NAME, '_rdy'))

DATASET2_NAME = "inria"
DATASET1_DIR = os.path.join(DATA_DIR, DATASET2_NAME)
DATASET2_DIR_READY = os.path.join(DATA_DIR, (DATASET2_NAME, '_rdy'))
