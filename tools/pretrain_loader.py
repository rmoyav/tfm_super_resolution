
import os

from dataset_storage import train_val_test_split, DATA_DIR, DATASET1_NAME
from image_resampler import process_images_in_folder


def pretrain_load() -> None:
    ready_dir = os.path.join(DATA_DIR, DATASET1_NAME+'_rdy')
    
    if not os.path.isdir(ready_dir):
        train_val_test_split()
    
    for folder in os.listdir(ready_dir):
        process_images_in_folder(os.path.join(ready_dir, folder, "hr_256"), 4)


if __name__ == "__main__":
    pretrain_load()
