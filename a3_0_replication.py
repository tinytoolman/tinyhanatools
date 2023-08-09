#-------------------------------------------------------------------------------
# Name:        a3_0_replication.py
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
import socket
import a3_1_localhost_rep_menu
import a3_1_remotehost_rep_menu
import a6_0_ssh_config

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_replication_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Replication Menu - {hostname}")
    print_bold("-------------------")
    print("1.  Replication Status")
    print("2.  Replication State")
    print("3.  Primary Localhost Replication Menu")
    print("4.  Secondary Remotehost Replication Menu")
    print("5.  Perform Takeover")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        replication_status(selected_userstore)
    elif choice == '2':
        replication_state(selected_userstore)
    elif choice == '3':
        a3_1_localhost_rep_menu.handle_localhost_rep_menu(selected_userstore)
    elif choice == '4':
        a3_1_remotehost_rep_menu.handle_remotehost_rep_menu(selected_userstore)
    elif choice == '5':
        perform_takeover()
    elif choice == '0':
        return
    elif choice.lower() == 'x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    # Wait for user input to return to replication menu
    input("Press Enter to continue...")
    handle_replication_menu(selected_userstore)

def replication_status(selected_userstore):
    clear_screen()
    print(f"Replication Status")

    key = selected_userstore.split()[1]
    command = ["HDBSettings.sh", "systemReplicationStatus.py"]

    try:
        subprocess.run(command, check=True)
        print("Current SAP HANA Replication Status")
    except subprocess.CalledProcessError as ex:
        print(f"Error showing current SAP HANA Replication Status: {ex.stderr}")
    except Exception as ex:
        print(f"Error showing current SAP HANA Replication Status: {str(ex)}")

def replication_state(selected_userstore):
    clear_screen()
    print(f"Replication State")

    key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_state"]

    try:
        subprocess.run(command, check=True)
        print("Current SAP HANA Replication State")
    except subprocess.CalledProcessError as ex:
        print(f"Error showing current SAP HANA Replication State: {ex.stderr}")
    except Exception as ex:
        print(f"Error showing current SAP HANA Replication State: {str(ex)}")

def perform_takeover():
    clear_screen()
    print("Please note that this operation will perform a takeover of the replicated host.")
    choice = input("Are you sure you want to continue? (Y/N): ")
    if choice.upper() != 'Y':
        return

    print("Perform takeover on the local or remote host?")
    host_choice = input("Enter 'Local' or 'Remote': ")
    if host_choice.lower() == 'local':
        perform_local_takeover()
    elif host_choice.lower() == 'remote':
        perform_remote_takeover()
    else:
        print("Invalid choice. Please try again.")

def perform_local_takeover():
    clear_screen()
    hostname = socket.gethostname()
    print(f"Performing takeover of LOCAL host: {hostname}")

    takeover_confirmation = input(f"Please type 'takeover' to perform takeover of LOCAL host {hostname}: ")
    if takeover_confirmation.lower() == 'takeover':
        command = ["hdbnsutil", "-sr_takeover"]
        try:
            subprocess.run(command, check=True)
            print("Please Perform Cleanup on Previous Primary Host if Takeover was Succesful")
        except subprocess.CalledProcessError as ex:
            print(f"Error performing takeover: {ex.stderr}")
        except Exception as ex:
            print(f"Error performing takeover: {str(ex)}")
    else:
        print("Takeover operation cancelled.")

def perform_remote_takeover():
    clear_screen()
    print(f"Performing takeover on REMOTE host")

    takeover_confirmation = input("Please type 'takeover' to continue: ")
    if takeover_confirmation.lower() == 'takeover':
        command = ["hdbnsutil", "-sr_takeover"]
        a6_0_ssh_config.execute_remote_command(command)
        print("Please Perform Cleanup on Previous Primary Host if Takeover was Succesful")
    else:
        print("Takeover operation cancelled.")

if __name__ == '__main__':
    hosts = a6_0_ssh_config.get_ssh_hosts()
    handle_replication_menu(None)
