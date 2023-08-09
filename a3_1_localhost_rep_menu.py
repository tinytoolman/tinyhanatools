#-------------------------------------------------------------------------------
# Name:        a3_1_localhost_rep_menu.py
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
import socket

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_localhost_rep_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Primary Localhost Replication Menu - {hostname}")
    print_bold("-------------------")
    print("1.  Replication Status")
    print("2.  Replication State")
    print("3.  Primary Replication Host Enable")
    print("4.  Primary replication Host Disable")
    print("5.  Localhost Host Perform Takeover")
    print("9.  Primary Host Replication Cleanup")
    print("0.  Back")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        replication_status()
    elif choice == '2':
        replication_state()
    elif choice == '3':
        replication_primary_host_enable()
    elif choice == '4':
        replication_primary_host_disable()
    elif choice == '5':
        perform_takeover_local()
    elif choice == '9':
        replication_local_cleanup()
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    # Wait for user input to continue
    input("Press Enter to continue...")
    handle_localhost_rep_menu(selected_userstore)

def replication_status():
    clear_screen()
    print(f"Replication Status")

    #key = selected_userstore.split()[1]
    command = ["HDBSettings.sh", "systemReplicationStatus.py"]

    try:
        subprocess.run(command, check=True)
        print("Current SAP HANA Replication Status")
    except subprocess.CalledProcessError as ex:
        print(f"Error showing current SAP HANA Replication Status: {ex.stderr}")
    except Exception as ex:
        print(f"Error showing current SAP HANA Replication Status: {str(ex)}")

def replication_state():
    clear_screen()
    print(f"Replication State")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_state"]

    try:
        subprocess.run(command, check=True)
        print("Current SAP HANA Replication State")
    except subprocess.CalledProcessError as ex:
        print(f"Error showing current SAP HANA Replication State: {ex.stderr}")
    except Exception as ex:
        print(f"Error showing current SAP HANA Replication State: {str(ex)}")

def replication_primary_host_enable():
    clear_screen()
    print(f"Enabling Primary Host System Replication")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_enable", "--name="]

    user_input=input("To Enable Replication on this primary host type 'enable': ")

    if user_input.lower() == 'enable':
        try:
            hostname = socket.gethostname()
            command[-1] += hostname  # Append the hostname to the last argument
            subprocess.run(command, check=True)
            print("Primary Host System Replication enabled successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error enabling Primary Host System Replication: {ex.stderr}")
        except Exception as ex:
            print(f"Error enabling Primary Host System Replication: {str(ex)}")

def replication_primary_host_disable():
    clear_screen()
    print(f"Disabling Primary Host System Replication")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_disable"]

    user_input=input("To Disable Replication on this Primary host type 'disable': ")

    if user_input.lower() == 'disable':
        try:
            subprocess.run(command, check=True)
            print("Primary Host System Replication disabled successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error disabling Primary Host System Replication: {ex.stderr}")
        except Exception as ex:
            print(f"Error disabling Primary Host System Replication: {str(ex)}")

def perform_takeover_local():
    clear_screen()
    print(f"Perform Takeover Local")
    print("This will only work if this local host is being replicated too.")
    print("Note, this will BREAK REPLICATION and perform takeover on this host\n")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_takeover"]

    user_input = input("To continue with the Replication Takeover, type 'takeover': ")

    if user_input.lower() == 'takeover':
        try:
            subprocess.run(command, check=True)
            print("Current SAP HANA Replication State")
        except subprocess.CalledProcessError as ex:
            print(f"Error showing current SAP HANA Replication State: {ex.stderr}")
        except Exception as ex:
            print(f"Error showing current SAP HANA Replication State: {str(ex)}")

def replication_local_cleanup():
    clear_screen()
    print(f"Replication Cleanup Local")
    print("Please note this will perform a HARD REMOVE of replication configuration\n")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_cleanup", "--force"]

    user_input = input("To continue with HARD REMOVE REPLICATION CLEANUP type 'remove': ")

    if user_input.lower() == 'remove':
        try:
            subprocess.run(command, check=True)
            print("Current SAP HANA Replication State")
        except subprocess.CalledProcessError as ex:
            print(f"Error showing current SAP HANA Replication State: {ex.stderr}")
        except Exception as ex:
            print(f"Error showing current SAP HANA Replication State: {str(ex)}")

if __name__ == '__main__':
    handle_localhost_rep_menu()
