"""
This module contains the functionality to store the models to be used
in the expected path so the rest of the workflow can be executed without
problems.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 28/05/2023
"""
import os

from models_storage import (download_repos, copy_config_files_sr3, copy_config_folder_liif,
                            copy_liif_infer_file, LIIF_CONFIG_DIR, SR3_CONFIG_DIR, LIIF_TRAIN_CONFIG)
from pretrain_loader import pretrain_load
from trainvaltest_functions import train_sr3, train_liif, val_sr3, val_liif, test_sr3, test_liif, select_file_from_config_dir
from dataset_storage import DATA_DIR, DATASET1_NAME
from image_info import drop_wrong_images

###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

def get_seed_value() -> int:
    """This function collect the user input regarding the seed value.

    Returns:
        int: seed
    """
    seed = -1
    custom_seed = None
    choice = input("Do you want to set a seed for the data splitting?: [y/n]")
    if choice == 'y':
        try:
            custom_seed = int(input("Give the new value for the seed (-1 = random): "))
        except ValueError:
            print("The given value is not of the expected type (integer)")
            print("The script will be using default seed value")

    if isinstance(custom_seed, int):
        print(f'The data splitting process will be using the seed={custom_seed}')
        seed = custom_seed

    return seed

def get_train_val() -> tuple:
    """This function collects the user input related to train and val percentages.

    Returns:
        tuple: the train percentage and the val percentages
    """
    train_percent = 0.6
    custom_train = None
        
    val_percent = 0.2
    custom_val = None
    
    choice = input("Do you want to set custom data splitting percentages? (Current values: train 60%, val 20%, test 20%): [y/n]")
    if choice == 'y':
        try:
            custom_train = float(input("Give the new value for the train percentage (Current value: 0.6): "))
        except ValueError:
            print("The given value is not of the expected type (float)")
            print("The script will be using default train percentage value")
 
        try:
            custom_val = float(input("Give the new value for the val percentage (Current value: 0.2): "))
        except ValueError:
            print("The given value is not of the expected type (float)")
            print("The script will be using default val percentage value")

    if isinstance(custom_train, float) and custom_train < 1:
        print(f'The train split percertange to be use is {custom_train * 100}%')
        train_percent = custom_train

    if isinstance(custom_val, float) and custom_val < 1:
        print(f'The data splitting process will be using the seed={custom_val * 100}%')
        val_percent = custom_val

    return train_percent, val_percent


def get_liif_input_dir() -> str:
    path = ''
    not_found_dir = True
    while not_found_dir:
        input_dir = input("Choose an input directory:")
    return path


def option1() -> None:
    print("Downloading model repos...")
    download_repos()
    print("Done!!")

def option2() -> None:
    seed = get_seed_value()
    train_percent, val_percent = get_train_val()
    print("Removing images with errors...")
    drop_wrong_images(os.path.join(DATA_DIR, DATASET1_NAME, 'Images'))
    print("Executing pre-train scripts...")
    pretrain_load(train_percent=train_percent, val_percent=val_percent, seed=seed)
    try:
        print("Copying configuration files...")
        copy_config_files_sr3()
        copy_config_folder_liif()
        print("Copying infer script...")
        copy_liif_infer_file()
    except FileNotFoundError:
        print("One or more of the files could not be copied. Please copy it manually.")
    print("Done!!")

def option3() -> None:
    print("SR3 training configuration selection.")
    config = select_file_from_config_dir(SR3_CONFIG_DIR)
    print("Launching SR3 training...")
    train_sr3(config)
    print("Done!!")

def option4() -> None:
    print("Liif training configuration selection.")
    config = select_file_from_config_dir(os.path.join(LIIF_CONFIG_DIR, LIIF_TRAIN_CONFIG))
    print("Launching Liif training...")
    train_liif(config)
    print("Done!!")

def option5() -> None:
    print("SR3 validation configuration selection.")
    config = select_file_from_config_dir(SR3_CONFIG_DIR)
    print("Launching SR3 validation...")
    val_sr3(config)
    print("Done!!")

def option6() -> None:
    print("Liif training configuration selection.")
    config = select_file_from_config_dir(os.path.join(LIIF_CONFIG_DIR, LIIF_TRAIN_CONFIG))
    print("Launching Liif validation...")
    # WIP: Working in this function
    val_liif(config)
    print("Done!!")
    
def option7() -> None:
    print("SR3 testing configuration selection.")
    config = select_file_from_config_dir(SR3_CONFIG_DIR)
    print("Launch SR3 infering process...")
    test_sr3(config)
    print("Done!!")

def option8() -> None:
    # WIP: Working in this function
    input_dir = get_liif_input_dir()
    #model_path = get_liif_model_path()
    print("Launching Liif infering process...")
    test_liif()
    print("Done!!")

def main():
    while True:
        print("==================================")
        print("Options Menu:")
        print("----------------------------------")
        print("1. Download model repositories.")
        print("2. Prepare data for training")
        print("3. Launch SR3 training")
        print("4. Launch Liif training")
        print("5. Launch SR3 validation")
        print("6. Launch Liif validation")
        print("7. Launch SR3 infering process")
        print("8. Launch Liif infering process")
        print("*. Give any other option to leave")
        print("==================================")
        choice = input("Choose one of the given options: ")

        if choice == '1':
            option1()
        elif choice == '2':
            option2()
        elif choice == '3':
            option3()
        elif choice == '4':
            option4()
        elif choice == '5':
            option5()
        elif choice == '6':
            option6()
        elif choice == '7':
            option7()
        elif choice == '8':
            option8()
        else:
            print("Option not found. Bye!.")
            break


###############################################################################
#                                                                             #
#                                   MAIN                                      #
#                                                                             #
###############################################################################

if __name__ == "__main__":
    main()