"""
This module contains the functions to downsample the original images
obtained from the source datasets to be used in the training of the
different models.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 23/04/2023
"""

import os
from itertools import repeat
from multiprocessing import Pool

from PIL import Image

from config.storage_config import DOWNSAMPLE_DIR

def create_downsample_dir(source_dir:str, downsample_dir:str) -> str:
    """This function creates a copy of the source_dir in a
    different path.

    Args:
        source_dir (_type_): directory to be copied
        downsample_dir (_type_): root dir where the copy will be created

    Returns:
        str: path of the new directory
    """
    directory_name = os.path.basename(os.path.dirname(source_dir))
    target_directory = os.path.join(downsample_dir, directory_name)
    os.makedirs(target_directory, exist_ok=True)
    return target_directory


def downsample_image(image:str, original_resolution:int, new_resolution:int, output_dir:str) -> str:
    """This function will downsample the given image to a new given resolution.

    Args:
        image (str): path to the imagen to be downsampled
        original_resolution (int): original resolution of the given image (cms/pixel)
        new_resolution (int): new resolution value (cms/pixel)
        output_dir (str): output directory where th downsampled image will be stored

    Raises:
        FileNotFoundError: raised when the given image path is not a file
        ValueError: raised when the new resolution is better than the original

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


def process_images_in_folder(dataset_dir:str, original_resolution:int, new_resolution:int) -> list[str]:
    """This function will use multithreading to create downsampled version of the images found
    within the given dataset_dir in order to be used to train the models.

    Args:
        dataset_dir (str): path to the folder containing all the original images
        original_resolution (int): resolution of the original images (cm/pixel)
        new_resolution (int): desired resolution for the downsampled images (cm/pixel)

    Returns:
        list[str]: list containing all the downsampled image paths
    """
    output_dir = create_downsample_dir(dataset_dir, DOWNSAMPLE_DIR)

    # Lista de archivos en la carpeta
    file_list = os.listdir(dataset_dir)

    # Lista de paths completos de cada imagen en la carpeta
    image_paths = [os.path.join(dataset_dir, file) for file in file_list if file.endswith(".jpg")]

    # Crea un pool de hilos con el número de hilos especificado
    with Pool() as pool:
        # Ejecuta la función especificada en paralelo en cada imagen utilizando starmap
        results = pool.starmap(downsample_image, [image_paths, repeat(original_resolution), repeat(new_resolution), repeat(output_dir)])

    return results