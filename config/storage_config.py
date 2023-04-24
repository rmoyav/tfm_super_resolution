"""
This is a configuration file to store diferent storage config
variables and constants.

:author: ${1:$(git log -1 --pretty=format:'%an')}
:date: ${2:$(git log -1 --pretty=format:'%ad' --date=format:'%d-%m-%Y')}
"""

import os
from tools.helper_functions import get_root_dir

USE_DEFAULT_PATHS = True
ROOT_DIR = get_root_dir()
DATA_DIR = os.path.join(ROOT_DIR, 'data')
