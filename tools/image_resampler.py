"""
This module contains the functions to downsample the original images
obtained from the source datasets to be used in the training of the
different models.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 23/04/2023
"""

import glob
import os
from itertools import repeat
from multiprocessing import Pool

from dataset_storage import create_resample_dir
from PIL import Image, ImageFilter


def resample_image(in_image: str, output_dir: str, scale: float, blur: bool = False, radius: float = 3) -> None:
    """This function will resample the given image to a new given resolution.

    Args:
        in_image (str): path to the original imagen to be resampled
        output_dir (str): utput directory where the resampled image will be stored
        scale (float): factor of the resampling
        blur (bool, optional): condition to add blur to the resampled image. Defaults to False.
        radius (float, optional): radius of the blur if added. Defaults to 3.

    Raises:
        FileNotFoundError: raised when the given image path is not a file
    """

    if not os.path.isfile(in_image):
        raise FileNotFoundError(
            f"The given file '{in_image}' could not be found!!")

    img = Image.open(in_image).convert('RGB')

    # Resolving new resolution values
    width, height = img.size
    img_width = int(width // scale)
    img_height = int(height // scale)

    # Resizing image
    resampled_img = img.resize((img_width, img_height), resample=Image.BICUBIC)

    # Adding blur if selected
    if blur:
        resampled_img = resampled_img.filter(ImageFilter.GaussianBlur(radius))

    img_name = os.path.basename(in_image)
    resampled_img.save(os.path.join(output_dir, img_name))


def process_images_in_folder(hr_dir: str, scale: float, blur: bool = False, radius: float = 3) -> None:
    """This function will resample all the images found in a given directory,
    containing the original high resolution imagenes, into an output directory, 
    containing the low resolution generated images.

    Args:
        hr_dir (str): High resolution dir containing the input images
        scale (float): Scale to resample the images
        blur (bool, optional): Condition to add blur to the output images. Defaults to False.
        radius (float, optional): Blur radius. Defaults to 3.
    """
    output_dir = create_resample_dir(hr_dir, scale)
    # Lista de paths completos de cada imagen en la carpeta
    image_paths = sorted(glob.glob(os.path.join(hr_dir, '*.tif'), recursive=False))
                         
    for path in image_paths:
        resample_image(os.path.join(hr_dir, path), output_dir, scale, blur, radius)
