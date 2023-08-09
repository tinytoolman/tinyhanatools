#-------------------------------------------------------------------------------
# Name:        a2_1_remote_db_administration.py
# Project:     TinyTools
# version:     1.05
# Author:      Tinus Mario Brink
#
# Created:     19/07/2023
# Copyright:   (c) Schoeman and Brink LLC 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import subprocess
import a6_0_ssh_config

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_remote_db_administration_menu(selected_userstore):
    clear_screen()
    print_bold("Remote Database Administration Menu")
    print_bold("-------------------")
    print("1.  Check HANA Services running Status")
    print("2.  HANA Overview")
    print("3.  Start Full DB with HDB start")
    print("4.  Stop Full DB with HDB stop")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        check_hana_status(selected_userstore)
        input("Press Enter to continue...")
    elif choice == '2':
        hana_overview(selected_userstore)
        input("Press Enter to continue...")
    elif choice == '3':
        start_full_db(selected_userstore)
        input("Press Enter to continue...")
    elif choice == '4':
        stop_full_db(selected_userstore)
        input("Press Enter to continue...")
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    input("Press Enter to continue...")
    handle_remote_db_administration_menu(selected_userstore)

def check_hana_status(selected_userstore):
    clear_screen()
    print("Checking Remote HANA Running Status")

    tinstance = os.environ.get('TINSTANCE')
    default_instance = tinstance if tinstance else '00'
    yinstance = input(f"Please enter instance number [{default_instance}]: ")
    if not yinstance:
        yinstance = default_instance

    # Run the sapcontrol command
    command = ["sapcontrol", "-nr", yinstance, "-function", "GetProcessList"]

    a6_0_ssh_config.execute_remote_command(command)

def hana_overview(selected_userstore):
    clear_screen()
    print("Remote Running SAP HANA System Overview")
    print("Note, a response \"not responding. retry in 5 sec...\""+
    " would autimatically time out after 12 tries if the database is not started."+
    " You would need to start full DB to view Overview")

    command = ["HDBSettings.sh", "systemOverview.py"]
    a6_0_ssh_config.execute_remote_command(command)

def start_full_db(selected_userstore):
    clear_screen()
    print("Starting Full Remote Database")

    command = ["HDB", "start"]

    user_input = input("To start the Full Remote HANA database, type 'start': ")

    if user_input.lower() == 'start':
        a6_0_ssh_config.execute_remote_command(command)

def stop_full_db(selected_userstore):
    clear_screen()
    print("Stopping Full Remote Database")

    command = ["HDB", "stop"]

    user_input = input("To stop the Full Remote HANA database, type 'stop': ")

    if user_input.lower() == 'stop':
        a6_0_ssh_config.execute_remote_command(command)

if __name__ == '__main__':
    handle_remote_db_administration_menu(None)

