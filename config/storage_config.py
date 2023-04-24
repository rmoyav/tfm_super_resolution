"""
This is a configuration file to store diferent storage config
variables and constants.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 23/04/2023
"""

import os
from tools.helper_functions import get_root_dir

USE_DEFAULT_PATHS = True
ROOT_DIR = get_root_dir()
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DOWNSAMPLE_DIR = os.path.join(DATA_DIR, 'downsamples')
