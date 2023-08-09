#-------------------------------------------------------------------------------
# Name:        a9_0_userstore.py
# Project:     TinyTools
# version:     1.05
# Author:      Tinus Mario Brink
#
# Created:     19/07/2023
# Copyright:   (c) Schoeman and Brink LLC 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import socket
import subprocess
import getpass

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_userstore_menu():
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Userstore Menu - {hostname}")
    print_bold("-------------------")
    print("Available Userstores: ")
    userstores = get_userstores()
    print("\n".join(userstores) if userstores else "No userstores available.")
    print("\n1.  Create Userstore Entry")
    print("2.  Select Userstore Entry")
    print("3.  Delete Userstore Entry")
    print("4.  Test Userstore Entry")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice [2]: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        create_userstore_entry()
    elif choice == '2':
        return select_userstore_entry()
    elif choice == '3':
        delete_userstore_entry()
    elif choice == '4':
        test_userstore_entry()
    elif choice == '':
        return select_userstore_entry()
    elif choice == '0':
        return None
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    handle_userstore_menu()

def create_userstore_entry():
    clear_screen()
    print("Creating Userstore Entry")

    key = input("Enter the userstore key: ")
    user = input("Enter the username: ")
    password = getpass.getpass("Enter the password: ")
    database = input("Enter the database name: ")
    host = os.uname()[1]
    port = input("Enter the port number: ")

    command = f"hdbuserstore set {key} {host}:{port}@{database} {user} {password}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Userstore entry created successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error creating userstore entry: {str(ex)}")

def get_userstores():
    command = "hdbuserstore list"
    try:
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.decode()
        lines = output.split("\n")
        userstores = []
        for i in range(len(lines)):
            if lines[i].startswith("KEY "):
                userstore = lines[i].strip()
                if i + 1 < len(lines) and lines[i + 1].strip().startswith("ENV :"):
                    userstore += " " + lines[i + 1].strip()
                userstores.append(userstore)
        return userstores
    except subprocess.CalledProcessError as ex:
        print(f"Error retrieving userstores: {str(ex)}")
        return []

def select_userstore_entry():
    clear_screen()
    print("Selecting Userstore Entry")
    userstores = get_userstores()

    if not userstores:
        print("No userstores available.")
        return

    print("Available Userstores:")
    for index, userstore in enumerate(userstores, start=1):
        print(f"{index}.  {userstore}")

    while True:
        print("0.  Back to previous screen")
        selection = input("Enter the userstore number: ")

        if selection == '0':
            return  # User chose to go back

        if not selection:
            print("You made no selection")
            input("Press Enter to continue...")
            return  # User chose to go back with no selection

        try:
            index = int(selection) - 1

            if index < 0 or index >= len(userstores):
                print("Invalid selection. Please try again.")
            else:
                selected_userstore = userstores[index]
                print(f"Selected Userstore: {selected_userstore}")
                return selected_userstore
        except ValueError:
            print("Invalid input. Please enter a valid userstore number.")

def delete_userstore_entry():
    clear_screen()
    print("Deleting Userstore Entry")
    userstores = get_userstores()

    if not userstores:
        print("No userstores available.")
        return

    print("Available Userstores:")
    for index, userstore in enumerate(userstores, start=1):
        print(f"{index}. {userstore}")

    selection = input("Enter the userstore number to delete: ")
    index = int(selection) - 1

    if index < 0 or index >= len(userstores):
        print("Invalid selection.")
        return

    selected_userstore = userstores[index]
    delete_userstore(selected_userstore)

def delete_userstore(userstore):
    key = userstore.split()[1]
    command = f"hdbuserstore delete {key}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Userstore entry deleted successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error deleting userstore entry: {str(ex)}")

def test_userstore_entry():
    clear_screen()
    print("Testing Userstore Entry")
    userstores = get_userstores()

    if not userstores:
        print("No userstores available.")
        return

    print("Available Userstores:")
    for index, userstore in enumerate(userstores, start=1):
        print(f"{index}. {userstore}")

    selection = input("Enter the userstore number to test: ")
    index = int(selection) - 1

    if index < 0 or index >= len(userstores):
        print("Invalid selection.")
        return

    selected_userstore = userstores[index]
    test_userstore(selected_userstore)

def test_userstore(userstore):
    key = userstore.split()[1]
    command = f"hdbsql -U {key} 'select * from dummy'"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Userstore tested successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error testing userstore: {str(ex)}")

if __name__ == '__main__':
    handle_userstore_menu()


