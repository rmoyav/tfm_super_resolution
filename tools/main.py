"""
This module contains the functionality to store the models to be used
in the expected path so the rest of the workflow can be executed without
problems.

:author: Ruben Moya Vazquez <rmoyav@uoc.edu>
:date: 28/05/2023
"""

from models_storage import download_repos
from pretrain_loader import pretrain_load
from trainvaltest_functions import train_sr3, train_liif, val_sr3, val_liif, test_sr3, test_liif

###############################################################################
#                                                                             #
#                                 FUNCTIONS                                   #
#                                                                             #
###############################################################################

def option1() -> None:
    print("Downloading model repos...")
    download_repos()
    print("Done!!")

def option2() -> None:
    print("Executing pre-train scripts...")
    pretrain_load()
    print("Done!!")

def option3() -> None:
    print("Launching SR3 training...")
    train_sr3()
    print("Done!!")

def option4() -> None:
    print("Launching Liif training...")
    train_liif()
    print("Done!!")

def option5() -> None:
    print("Launching SR3 validation...")
    val_sr3()
    print("Done!!")

def option6() -> None:
    print("Launching Liif validation...")
    # WIP: Working in this function
    val_liif()
    print("Done!!")
    
def option7() -> None:
    print("Launch SR3 infering process...")
    test_sr3()
    print("Done!!")

def option8() -> None:
    # WIP: Working in this function
    not_found_dir = True
    while not_found_dir:
        input_dir = input("Choose an input directory:")
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