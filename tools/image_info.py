"""
This module contain functions meant to obtain information
from the images within our datasets.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 29/04/2023
"""
import os
import shutil

from PIL import Image
from PIL.ExifTags import TAGS


def imagen_resolution(image_path: str) -> tuple:
    """This function will obtain the resolution of a
    given image in pixels. (w,h)

    Args:
        image_path (str): image full path

    Returns:
        tuple: tuple with the width and height of the image
    """
    img = Image.open(image_path)
    return img.size


def print_image_metadata(image_path: str) -> None:
    """This function will print all the metadata
    found within the image used as parameter.

    Args:
        image_path (str): the absolute path to the image
    """
    with Image.open(image_path) as img:
        exif_data = img.getexif()
        for tag_id in exif_data:
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            print(f"{tag:25}: {data}")


def delete_folder(path:str) -> None:
    """This function will delete the given folder
    and its content

    Args:
        path (str): path to the folder
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        print(f"Given dir '{path}' does not exist!!")

def drop_wrong_images(root_dir: str, std_width: int = 256, std_height: int = 256) -> None:
    """This function will remove evey image that does not fit
    the given standard widht and standard height parameters.

    Args:
        root_dir (str): path where the images will be searched
        std_width (int, optional): standard width. Defaults to 256.
        std_height (int, optional): standard height. Defaults to 256.
    """
    print('Cleaning the dataset of wrong images...')
    error_path = os.path.join(os.path.dirname(os.path.abspath(root_dir)), 'failed')
    os.makedirs(error_path, exist_ok=True)
    for current_path, folders, files in os.walk(root_dir):
        for tmpfile in files:
            if tmpfile.endswith('.tif'):
                full_path = os.path.join(current_path, tmpfile)
                try:
                    with Image.open(full_path) as image:
                        width, height = image.size
                        if width != std_width or height != std_height:
                            os.remove(full_path)
                            print(f"Removing: {os.path.basename(full_path)} with dimensions {width}x{height}")
                except (IOError, OSError):
                    shutil.move(full_path, os.path.join(error_path, tmpfile))
                    print(
                        f"File '{os.path.basename(full_path)}' has some errors and will be stored in {error_path}")
                finally:
                    delete_folder(error_path)
