#-------------------------------------------------------------------------------
# Name:        a7_0_sapcar_prep.py
# Project:     TinyTools
# version:     1.05
# Author:      Tinus Mario Brink
#
# Created:     20/07/2023
# Copyright:   (c) Schoeman and Brink LLC 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import socket

# Global variables
current_extraction_directory = os.getcwd()
patch_directory = None

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_sapcar_prep(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"SAPCAR Prep Menu - {hostname}")
    print_bold("-------------------")
    print(f"Current Extraction Directory: {current_extraction_directory}")
    print(f"Current Patch Directory: {patch_directory}")
    print("1.  Change to New Extraction Directory")
    print("2.  Set Current Patch Directory")
    print("3.  View contents of Patch Directory")
    print("4.  View contents of Extraction Directory")
    print("5.  Extract files from Patch Directory with SAPCAR")
    print("6.  Create Directory")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        change_extraction_directory()
    elif choice == '2':
        set_patch_directory()
    elif choice == '3':
        view_patch_directory()
    elif choice == '4':
        view_extraction_directory()
    elif choice == '5':
        extract_files_with_sapcar()
    elif choice == '6':
        create_directory()
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    # Wait for user input to return to sapcar prep menu
    input("Press Enter to continue...")
    handle_sapcar_prep(selected_userstore)

def change_extraction_directory():
    global current_extraction_directory

    attempts = 0
    while attempts < 2:
        new_directory = input("Please provide the new extraction directory: ")
        if not new_directory:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    if os.path.isdir(new_directory):
        current_extraction_directory = new_directory
        os.chdir(current_extraction_directory)
        print(f"Extraction directory changed to: {current_extraction_directory}")
    else:
        print(f"Directory '{new_directory}' does not exist.")

def set_patch_directory():
    global patch_directory

    attempts = 0
    while attempts < 2:
        new_directory = input("Please provide the new patch directory: ")
        if not new_directory:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    if os.path.isdir(new_directory):
        patch_directory = new_directory
        print(f"Patch directory set to: {patch_directory}")
    else:
        print(f"Directory '{new_directory}' does not exist.")

def view_patch_directory():
    global patch_directory

    if not patch_directory:
        attempts = 0
        while attempts < 2:
            new_directory = input("Please provide the path to the patch directory: ")
            if not new_directory:
                attempts += 1
                print("Nothing entered.")
                if attempts == 2:
                    print("Going back to menu.")
                    return
                continue
            else:
                break

    path = patch_directory

    try:
        files = get_files_in_directory(path)
        print(f"List obtained from {path}:")
        for i, file_name in enumerate(files, start=1):
            print(f"{i}. {file_name}")
    except FileNotFoundError:
        print(f"Invalid path: {path}")

def view_extraction_directory():
    global current_extraction_directory

    if not current_extraction_directory:
        attempts = 0
        while attempts < 2:
            new_directory = input("Please provide the path to the extraction directory: ")
            if not new_directory:
                attempts += 1
                print("Nothing entered.")
                if attempts == 2:
                    print("Going back to menu.")
                    return
                continue
            else:
                break

    path = current_extraction_directory

    try:
        files = get_files_in_directory(path)
        print(f"List obtained from {path}:")
        for i, file_name in enumerate(files, start=1):
            print(f"{i}. {file_name}")
    except FileNotFoundError:
        print(f"Invalid path: {path}")

def create_directory():
    attempts = 0
    while attempts < 2:
        directory_path = input("Please provide the full path to the directory: ")
        if not directory_path:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    try:
        os.makedirs(directory_path)
        print(f"Directory created successfully: {directory_path}")
    except OSError as e:
        print(f"Failed to create directory: {e}")

def get_files_in_directory(path):
    files = os.listdir(path)
    return files

def extract_files_with_sapcar():
    global patch_directory

    if patch_directory is None:
        print("No patch directory set.")
        return

    default_path = f"[{patch_directory}]" if patch_directory else ""
    path = input(f"Please provide the path to the patch directory {default_path}: ") or patch_directory

    try:
        files = get_files_in_directory(path)
    except FileNotFoundError:
        print(f"Invalid path: {path}")
        return

    print(f"List obtained from {path}:")
    for i, file_name in enumerate(files, start=1):
        print(f"{i}. {file_name}")

    attempts = 0
    while attempts < 2:
        file_nums = input("Enter file number(s) [comma separated or ALL]: ")
        if not file_nums:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    if file_nums.upper() == 'ALL':
        selected_files = [str(num) for num in range(1, len(files) + 1)]
    else:
        selected_files = file_nums.split(',')

    perform_extraction(path, files, selected_files)

def perform_extraction(path, files, selected_files):
    if not selected_files:
        print("No files selected.")
        return

    extracted_files = []
    selected_files = [int(num) for num in selected_files if num.isdigit()]

    for file_num in selected_files:
        if 1 <= file_num <= len(files):
            file_name = files[file_num - 1]
            file_path = os.path.join(path, file_name)
            command = f"SAPCAR -xf {file_path} -manifest SIGNATURE.SMF"
            print(f"Extracting {file_path}")
            os.system(command)
            extracted_files.append(file_name)
        else:
            print(f"Invalid file number: {file_num}")

    if not extracted_files:
        print("No files were extracted.")

    return extracted_files

if __name__ == "__main__":
    handle_sapcar_prep(None)
