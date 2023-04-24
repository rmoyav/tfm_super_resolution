"""
This module contain all the different helper functions that would
be used within our code but do not fit in any other module.

:author: $(git log -1 --pretty=format:'%an')
:date: $(git log -1 --pretty=format:'%ad' --date=format:'%d-%m-%Y')
"""

import os

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
