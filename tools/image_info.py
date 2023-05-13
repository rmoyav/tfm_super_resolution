"""
This module contain functions meant to obtain information
from the images within our datasets.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 29/04/2023
"""

from PIL import Image
from PIL.ExifTags import TAGS

from PIL import Image

def imagen_resolution(image_path:str) -> tuple:
    """This function will obtain the resolution of a
    given image in pixels. (w,h)

    Args:
        image_path (str): image full path

    Returns:
        tuple: tuple with the width and height of the image
    """
    img = Image.open(image_path)
    return img.size

def print_image_metadata(image_path:str) -> None:
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
