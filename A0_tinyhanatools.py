#-------------------------------------------------------------------------------
# Name:        A0_tinyhanatools.py
# Project:     TinyHanaTools
# version:     1.05
# Author:      Tinus Mario Brink
#
# Created:     19/07/2023
# Copyright:   (c) Schoeman and Brink LLC 2023, Tinus Mario Brink "Tiny"
# Website:     www.sabtec.co
# Licence:     GNU GENERAL Public License Version 3
# License URL: #####
#
#-------------------------------------------------------------------------------

import os
import sys
import socket
import a1_0_backup_recovery
import a2_0_database_administration
import a3_0_replication
import a4_0_system_configuration
import a5_0_security_user_management
import a6_0_ssh_config
import a7_0_sapcar_prep
import a8_0_landscape_repository
import a9_0_userstore
import showme
import LICENSE

VERSION = "1.06"

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def display_version():
    print(f"TinyHanaTools {VERSION}")

def display_main_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Tiny HANA Tools Menu - {hostname}")
    print(f"{selected_userstore}")
    print_bold("-------------------")
    print("1.  Backup and Recovery")
    print("2.  Database Administration")
    print("3.  Replication")
    print("4.  System Configuration")
    print("5.  Security and User Management")
    print("6.  SSH Config")
    print("7.  SAPCAR prep")
    print("8.  Landscape Repository")
    print("9.  Userstore")
    print("L.  License Info")
    print("x.  Exit")
    print_bold("-------------------")

def handle_menu_choice(choice, selected_userstore):
    clear_screen()
    if choice == '1':
        a1_0_backup_recovery.handle_backup_recovery_menu(selected_userstore)
    elif choice == '2':
        a2_0_database_administration.handle_database_administration_menu(selected_userstore)
    elif choice == '3':
        a3_0_replication.handle_replication_menu(selected_userstore)
    elif choice == '4':
        a4_0_system_configuration.handle_system_configuration_menu(selected_userstore)
    elif choice == '5':
        a5_0_security_user_management.handle_security_user_management_menu(selected_userstore)
    elif choice == '6':
        a6_0_ssh_config.handle_ssh_config_menu()
    elif choice == '7':
        a7_0_sapcar_prep.handle_sapcar_prep(selected_userstore)
    elif choice == '8':
        a8_0_landscape_repository.handle_landscape_repository_menu(selected_userstore)
    elif choice == '9':
        userstore = a9_0_userstore.handle_userstore_menu()
    elif choice.lower() == 'l':
        LICENSE.main()
    #elif choice == '0':
    #    return False
    elif choice.lower() == 'x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    elif choice.lower() == 'bubbles':
        showme.main()
    else:
        print("Invalid choice. Please try again.")

    return True

def print_table(data, title):
    title_length = len(title)
    data_length = max(len(row[0]) for row in data)
    max_length = max(title_length, data_length)
    width = max_length + 4
    width2 = max_length + 2

    title_border = "─" * title_length
    data_border = "─" * data_length

    print(f"╭{title_border:^{width}}╮")
    print(f"│{title:^{width}}│")
    print(f"├{data_border:^{width}}┤")

    for row in data:
        print(f"│ {row[0]:<{width2}} │")

    print(f"└{data_border:^{width}}┘")

def main():
    selected_userstore = None  # Initialize selected_userstore as None

    data = [
        ["                             \`.     "],
        ["   .--------------.___________) \    "],
        ["   |//////////////|___________[ ]    "],
        ["   `--------------'           ) (    "],
        ["                              '-'    "],
        ["                                     "],
        ["Schoeman and Brink, LLC"],
        ["www.sabtec.co"]
    ]


    while selected_userstore is None:
        clear_screen()
        title = "TinyToolman - TinyHanaTools v 1.06"
        print_table(data, title)
        input("Press Enter to Continue...")

        selected_userstore = a9_0_userstore.handle_userstore_menu()

    running = True
    while running:
        display_main_menu(selected_userstore)
        text = "Enter your choice: "
        choice = input('\033[1m' + text + '\033[0m')
        running = handle_menu_choice(choice, selected_userstore)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        display_version()
    else:
        main()
