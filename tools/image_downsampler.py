"""
This module contains the functions to downsample the original images
obtained from the source datasets to be used in the training of the
different models.

:author: ${1:$(git log -1 --pretty=format:'%an')}
:date: ${2:$(git log -1 --pretty=format:'%ad' --date=format:'%d-%m-%Y')}
"""

import os
from PIL import Image


def downsample_image(image:str, original_resolution:int, new_resolution:int, output_dir:str) -> str:
    """This function will downsample the given image to a new given resolution.

    Args:
        image (str): path to the imagen to be downsampled
        original_resolution (int): original resolution of the given image (cms/pixel)
        new_resolution (int): new resolution value (cms/pixel)
        output_dir (str): output directory where th downsampled image will be stored

    Returns:
        str: path to the downsampled image
    """
    if not os.path.isfile(image):
        raise FileNotFoundError(f"The given file '{image}' could not be found!!")

    if original_resolution > new_resolution:
        raise ValueError('New resolution must be greater (cms/pixel) than original in order to downsample!!')

    img_name = image.split(os.pathsep)[-1]

    img = Image.open(image)

    # Resolving new resolution values
    width, height = img.size
    new_width = width // (original_resolution / new_resolution)
    new_height = height // (original_resolution / new_resolution)

    # Resizing image
    img_nueva_resolucion = img.resize((new_width, new_height))

    # Storage of the resized image
    img_nueva_resolucion.save(os.path.join(output_dir, img_name))