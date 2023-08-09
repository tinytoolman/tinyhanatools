#-------------------------------------------------------------------------------
# Name:        a8_1_landscape_functions.py
# Project:     TinyTools
# version:     1.05
# Author:      Tinus Mario Brink
#
# Created:     24/07/2023
# Copyright:   (c) Schoeman and Brink LLC 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import socket
import subprocess
import a8_0_landscape_repository
import a6_0_ssh_config

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_landscape_repository_menu():
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Landscape Functions Menu - {hostname}")
    print_bold("-------------------")
    print("1.  Start Landscape")
    print("2.  Stop Landscape")
    print("3.  HANA Landscape Status")
    print("4.  HANA Landscape Overview")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        start_landscape()
    elif choice == '2':
        stop_landscape()
    elif choice == '3':
        status_landscape()
    elif choice == '4':
        overview_landscape()
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    handle_landscape_repository_menu()

def start_landscape():
    clear_screen()
    print("Starting Landscape")

    # Get the selected repository from the user
    selected_repo = a8_0_landscape_repository.show_repository(None)

    if selected_repo is None:
        return

    systems = selected_repo.get('systems', [])

    if not systems:
        print("No systems found in the selected repository.")
        input("Press Enter to continue...")
        return

    # Construct the start command
    command = ["HDB", "start"]

    user_input = input("To start all systems in the landscape, type 'start': ")

    if user_input.lower() == 'start':
        for system_info in systems:
            system_name = system_info['name']  # Get the system name from the system information dictionary
            print_bold(f"Starting system {system_name}")
            a6_0_ssh_config.execute_remote_command_on_host(system_name, command)

    input("Press Enter to continue...")

def stop_landscape():
    clear_screen()
    print("Stopping Landscape")

    # Get the selected repository from the user
    selected_repo = a8_0_landscape_repository.show_repository(None)

    if selected_repo is None:
        return

    systems = selected_repo.get('systems', [])

    if not systems:
        print("No systems found in the selected repository.")
        input("Press Enter to continue...")
        return

    # Construct the stop command
    command = ["HDB", "stop"]

    user_input = input("To stop all systems in the landscape, type 'stop': ")

    if user_input.lower() == 'stop':
        for system_info in reversed(systems):
            system_name = system_info['name']  # Get the system name from the system information dictionary
            print_bold(f"Stopping system {system_name}")
            a6_0_ssh_config.execute_remote_command_on_host(system_name, command)

    input("Press Enter to continue...")

def status_landscape():
    clear_screen()
    print("HANA Landscape Status")

    # Get the selected repository from the user
    selected_repo = a8_0_landscape_repository.show_repository(None)

    if selected_repo is None:
        return

    systems = selected_repo.get('systems', [])

    if not systems:
        print("No systems found in the selected repository.")
        input("Press Enter to continue...")
        return

    for system_info in systems:
        system_name = system_info['name']  # Get the system name from the system information dictionary

        # Get the instance number from the system information dictionary or use '00' as the default
        instance = system_info.get('instance', '00')

        print_bold(f"HANA Overview {system_name}")

        # Construct the stop command for the specific instance number of the system
        command = ["sapcontrol", "-nr", instance, "-function", "GetProcessList"]
        a6_0_ssh_config.execute_remote_command_on_host(system_name, command)

    input("Press Enter to continue...")

def overview_landscape():
    clear_screen()
    print("HANA Landscape Overview")

    # Get the selected repository from the user
    selected_repo = a8_0_landscape_repository.show_repository(None)

    if selected_repo is None:
        return

    systems = selected_repo.get('systems', [])

    if not systems:
        print("No systems found in the selected repository.")
        input("Press Enter to continue...")
        return

    # Construct the stop command
    command = ["HDBSettings.sh", "systemOverview.py"]

    for system_info in systems:
        system_name = system_info['name']  # Get the system name from the system information dictionary
        instance = system_info.get('instance', '00')  # Get the instance number or use '00' as the default

        print_bold(f"HANA Overview {system_name}, instance {instance}")
        a6_0_ssh_config.execute_remote_command_on_host(system_name, command)

    input("Press Enter to continue...")

if __name__ == '__main__':
    handle_landscape_repository_menu()
