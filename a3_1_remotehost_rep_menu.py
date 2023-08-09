#-------------------------------------------------------------------------------
# Name:        a3_1_remotehost_rep_menu.py
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
import a6_0_ssh_config

def clear_screen():
  os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_remotehost_rep_menu(selected_userstore):
    clear_screen()
    print_bold("Secondary Remotehost Replication Menu")
    print_bold("-------------------")
    print("1.  Remote Host Replication Status")
    print("2.  Remote Host Replication State")
    print("3.  Remote Host Replication Register")
    print("4.  Remote Host Perform Takeover")
    print("9.  Remote Host Replication Cleanup")
    print("0.  Back")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        replication_status()
    elif choice == '2':
        replication_state()
    elif choice == '3':
        remote_host_replication_register()
    elif choice == '4':
        perform_takeover_remote()
    elif choice == '9':
        replication_remote_cleanup()
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
    handle_remotehost_rep_menu(selected_userstore)

def replication_status():
    clear_screen()
    print(f"Remote Host Replication Status")

    #key = selected_userstore.split()[1]
    command = ["HDBSettings.sh", "systemReplicationStatus.py"]

    a6_0_ssh_config.execute_remote_command(command)

def replication_state():
    clear_screen()
    print(f"Remote Host Replication State")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_state"]

    a6_0_ssh_config.execute_remote_command(command)

def remote_host_replication_register():
    localhost = socket.gethostname()
    hosts = a6_0_ssh_config.get_ssh_hosts()

    if not hosts:
        print("No hosts configured.")
        return

    print("Configured SSH Hosts:")
    for i, host in enumerate(hosts, start=1):
        print(f"{i}. {host}")

    host_idx = input("Select a host number: ")

    try:
        host = hosts[int(host_idx) - 1]
    except (ValueError, IndexError):
        print("Invalid host selection")
        return

    primary_sid = os.environ.get('SAPSYSTEMNAME')
    primary_instance = os.environ.get('TINSTANCE', '00')

    print(f"Primary SAP SID: {primary_sid}")
    print(f"Primary HDB Instance Number: {primary_instance}\n")

    default_instance = primary_instance if primary_instance else '00'
    remote_instance = input(f"Please provide remote instance number [{default_instance}]: ")
    if not remote_instance:
        remote_instance = default_instance

    replication_modes = [
        "sync",
        "syncmem",
        "async"
    ]

    print("Choose replication mode:")
    for i, mode in enumerate(replication_modes, start=1):
        print(f"{i}. {mode}")

    replication_mode_idx = input("Select replication mode: ")
    try:
        replication_mode = replication_modes[int(replication_mode_idx) - 1]
    except (ValueError, IndexError):
        print("Invalid replication mode selection")
        return

    operation_modes = [
        "delta_datashipping",
        "logreplay",
        "logreplay_readaccess"
    ]

    print("Select operation mode:")
    for i, mode in enumerate(operation_modes, start=1):
        print(f"{i}. {mode}")

    operation_mode_idx = input("Select operation mode: ")
    try:
        operation_mode = operation_modes[int(operation_mode_idx) - 1]
    except (ValueError, IndexError):
        print("Invalid operation mode selection")
        return

    use_for_hint_based_statement_routing = input("Do you want to Use for Hint Based Statement Routing Y/N [N]: ")
    use_for_hint_based_statement_routing = use_for_hint_based_statement_routing.upper() == 'Y'

    force_full_replication = input("Do you want to force full replication? This will initiate full data shipping Y/N [N]: ")
    force_full_replication = force_full_replication.upper() == 'Y'

    command = [
        "hdbnsutil",
        "-sr_register",
        f"--remoteHost={localhost}",
        f"--name={host}",
        f"--remoteInstance={remote_instance}",
        f"--replicationMode={replication_mode}",
        f"--operationMode={operation_mode}"
    ]

    if operation_mode == "logreplay_readaccess":
        if use_for_hint_based_statement_routing:
            command.append("--useForHintBasedStatementRouting")

    if force_full_replication:
        command.append("--force_full_replica")

    command.append("--online")

    print("\n----------------------------------------")
    print(f"Full Command to run: {' '.join(command)}")
    print("\n----------------------------------------\n")
    print("The PKI SSFS data/key will be copied now and setup will begin")
    input("Press enter to continue...")

    # Construct the source and destination file paths
    dat_file_path = f"/usr/sap/{primary_sid}/SYS/global/security/rsecssfs/data/SSFS_{primary_sid}.DAT"
    key_file_path = f"/usr/sap/{primary_sid}/SYS/global/security/rsecssfs/key/SSFS_{primary_sid}.KEY"

    # Copy the DAT file to the remote host
    scp_dat_command = ["scp", dat_file_path, f"{host}:{dat_file_path}"]
    try:
        subprocess.run(scp_dat_command, check=True)
    except subprocess.CalledProcessError as ex:
        print(f"Error copying DAT file to remote host: {ex.stderr}")
        return

    # Copy the KEY file to the remote host
    scp_key_command = ["scp", key_file_path, f"{host}:{key_file_path}"]
    try:
        subprocess.run(scp_key_command, check=True)
    except subprocess.CalledProcessError as ex:
        print(f"Error copying KEY file to remote host: {ex.stderr}")
        return

    a6_0_ssh_config.execute_remote_command(command)

def perform_takeover_remote():
    clear_screen()
    print(f"Perform Takeover Remote")
    print("This will only work if the remote host is being replicated too.")
    print("Note, this will BREAK REPLICATION and perform takeover on the remote host\n")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_takeover"]

    user_input = input("To continue with the Replication Takeover, type 'takeover': ")

    if user_input.lower() == 'takeover':
        a6_0_ssh_config.execute_remote_command(command)

def replication_remote_cleanup():
    clear_screen()
    print(f"Replication Cleanup Remote")
    print("Please note this will perform a HARD REMOVE of replication configuration\n")

    #key = selected_userstore.split()[1]
    command = ["hdbnsutil", "-sr_cleanup", "--force"]

    user_input = input("To continue with HARD REMOVE REPLICATION CLEANUP type 'remove': ")

    if user_input.lower() == 'remove':
        a6_0_ssh_config.execute_remote_command(command)

if __name__ == '__main__':
    hosts = a6_0_ssh_config.get_ssh_hosts()
    handle_remotehost_rep_menu(None)
