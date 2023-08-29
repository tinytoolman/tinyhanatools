#-------------------------------------------------------------------------------
# Name:        a6_0_ssh_config.py
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
import json
import a8_0_landscape_repository

def clear_screen():
  os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_ssh_config_menu():
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"SSH Config Menu - {hostname}")
    print_bold("-------------------")
    print("1.  Setup new SSH Host")
    print("2.  Test SSH Host")
    print("3.  Connect to SSH Host")
    print("4.  Delete SSH Host Config")
    #print("5.  Add Hostname to Repository")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        setup_new_ssh_host()
    elif choice == '2':
        test_ssh_host()
    elif choice == '3':
        connect_ssh_host()
    elif choice == '4':
        delete_ssh_host_config()
    #elif choice == '5':
    #    add_hostname_to_repository()
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    input("Press Enter to continue...")
    handle_ssh_config_menu()

def get_ssh_hosts():
  home = os.environ['HOME']
  json_path = os.path.join(home, '.ssh_hosts.json')
  try:
    with open(json_path) as f:
      hosts = json.load(f)
    return hosts
  except:
    return []

def update_ssh_hosts(hosts):
    # Check for duplicate host names
    unique_hosts = list(set(hosts))
    if len(unique_hosts) != len(hosts):
        print("Duplicate host names found. Aborting update.")
        return
    home = os.environ['HOME']
    json_path = os.path.join(home, '.ssh_hosts.json')
    with open(json_path, 'w') as f:
        json.dump(hosts, f)

def setup_new_ssh_host():
    attempts = 0
    while attempts < 2:
        hostname = input("Enter hostname: ")
        if not hostname:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                return
            continue
        else:
            break

    attempts = 0
    while attempts < 2:
        username = input("Enter username: ")
        if not username:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                return
            continue
        else:
            break

    hosts = get_ssh_hosts()
    if hostname in hosts:
        print("Hostname already exists.")
        input("Press Enter to continue...")
        return

    # Generate SSH key pair
    ssh_keygen_command = ["ssh-keygen", "-t", "rsa"]
    subprocess.run(ssh_keygen_command)

    # Add private key to SSH agent
    ssh_add_command = ["ssh-add", os.path.expanduser("~/.ssh/id_rsa")]
    subprocess.run(ssh_add_command)

    # Copy public key to remote host
    ssh_copy_id_command = ["ssh-copy-id", f"{username}@{hostname}"]
    proc = subprocess.Popen(ssh_copy_id_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode == 0:
        print("SSH host setup successful")
        hosts.append(hostname)
        update_ssh_hosts(hosts)
    else:
        print(f"Error setting up SSH host: {err}")


'''
def setup_new_ssh_host():
    attempts = 0
    while attempts < 2:
        hostname = input("Enter hostname: ")
        if not hostname:
            attempts +=1
            print("Nothing entered.")
            if attempts == 2:
                return
            continue
        else:
            break

    hosts = get_ssh_hosts()
    if hostname in hosts:
        print("Hostname already exists.")
        input("Press Enter to continue...")
        return

    # Generate SSH key pair
    ssh_keygen_command = ["ssh-keygen", "-t", "rsa"]
    subprocess.run(ssh_keygen_command)

    # Add private key to SSH agent
    ssh_add_command = ["ssh-add", os.path.expanduser("~/.ssh/id_rsa")]
    subprocess.run(ssh_add_command)

    # Copy public key to remote host
    ssh_copy_id_command = ["ssh-copy-id", hostname]
    proc = subprocess.Popen(ssh_copy_id_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode == 0:
        print("SSH host setup successful")
        hosts.append(hostname)
        update_ssh_hosts(hosts)
    else:
        print(f"Error setting up SSH host: {err}")
'''

def test_ssh_host():
    hosts = get_ssh_hosts()

    if not hosts:
        print("No hosts configured")
        input("Press Enter to continue...")
        return

    print("Configured SSH Hosts:")

    for i, host in enumerate(hosts):
        print(f"{i+1}. {host}")

    attempts = 0
    while attempts < 2:
        host_idx = input("Select host number: ")
        if not host_idx:
            attempts += 1
            print("No host selected")
            if attempts == 2:
                return
            continue
        else:
            break

    try:
        host = hosts[int(host_idx)-1]
    except (ValueError, IndexError):
        print("Invalid host selection")
        input("Press Enter to continue...")
        return

    proc = subprocess.Popen(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", host, "echo", "SSH test OK"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode == 0:
        print(f"SSH connection successful to {host}")
    else:
        print(f"SSH test failed: {err}")

def connect_ssh_host():
    hosts = get_ssh_hosts()

    if not hosts:
        print("No hosts configured")
        input("Press Enter to continue...")
        return

    print("Configured SSH Hosts:")

    for i, host in enumerate(hosts):
        print(f"{i+1}. {host}")

    attempts = 0
    while attempts < 2:
        host_idx = input("Select host number: ")
        if not host_idx:
            attempts += 1
            print("No host selected")
            if attempts == 2:
                return
            continue
        else:
            break

    try:
        host = hosts[int(host_idx)-1]
    except IndexError:
        print("Invalid host number")
        return

    subprocess.call(["ssh", host])

def delete_ssh_host_config():
    hosts = get_ssh_hosts()

    if not hosts:
        print("No hosts configured")
        input("Press Enter to continue...")
        return

    print("Configured SSH Hosts:")

    for i, host in enumerate(hosts):
        print(f"{i+1}. {host}")

    attempts = 0
    while attempts < 2:
        host_idx = input("Select host number: ")
        if not host_idx:
            attempts += 1
            print("No host selected")
            if attempts == 2:
                return
            continue
        else:
            break

    try:
        host_to_delete = hosts[int(host_idx)-1]
    except (ValueError, IndexError):
        print("Invalid host selection")
        input("Press Enter to continue...")
        return

    proc = subprocess.Popen(["ssh-keygen", "-R", host_to_delete], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode == 0:
        print(f"{host_to_delete} config removed")
        hosts.remove(host_to_delete)
        update_ssh_hosts(hosts)
    else:
        print(f"Error deleting host {host_to_delete}: {err}")

def add_hostname_to_repository():
    hosts = get_ssh_hosts()

    if not hosts:
        print("No hosts configured")
        #input("Press Enter to continue...")
        return

    print("Configured SSH Hosts:")

    for i, host in enumerate(hosts):
        print(f"{i+1}. {host}")

    attempts = 0
    while attempts < 2:
        host_idx = input("Select host number: ")
        if not host_idx:
            attempts += 1
            print("No host selected")
            if attempts == 2:
                return
            continue
        else:
            break

    try:
        host_to_add = hosts[int(host_idx)-1]
    except (ValueError, IndexError):
        print("Invalid host selection")
        #input("Press Enter to continue...")
        return

    a8_0_landscape_repository.add_hostname(None, host_to_add)
    #input("Press Enter to continue...")

def run_remote_command(host, command):
    try:
        ssh_command = ["ssh", host] + command
        subprocess.run(ssh_command, check=True)
    except subprocess.CalledProcessError as ex:
        print(f"Error running remote command on {host}: {ex.stderr}")
    except Exception as ex:
        print(f"Error running remote command on {host}: {str(ex)}")

def execute_remote_command(command):
    host = select_ssh_host()
    if host is not None:
        # Construct the command with environment setup
        remote_command = f". ~/.bashrc && {' '.join(command)}"
        # Run remote command on the specified host
        try:
            subprocess.run(["ssh", host, remote_command], check=True)
        except subprocess.CalledProcessError as ex:
            print(f"Error running remote command on {host}: {ex.stderr}")
        except Exception as ex:
            print(f"Error running remote command on {host}: {str(ex)}")

def execute_remote_command_on_host(host, command):
    if host is not None:
        # Construct the command with environment setup
        remote_command = f". ~/.bashrc && {' '.join(command)}"
        # Run remote command on the specified host
        try:
            subprocess.run(["ssh", host, remote_command], check=True)
        except subprocess.CalledProcessError as ex:
            print(f"Error running remote command on {host}: {ex.stderr}")
        except Exception as ex:
            print(f"Error running remote command on {host}: {str(ex)}")

def select_ssh_host():
    hosts = get_ssh_hosts()

    if not hosts:
        print("No hosts configured")
        return None

    print("Configured SSH Hosts:")

    for i, host in enumerate(hosts):
        print(f"{i+1}. {host}")

    attempts = 0
    while attempts < 2:
        host_idx = input("Select host number: ")
        if not host_idx:
            attempts += 1
            print("No host selected")
            if attempts == 2:
                return
            continue
        else:
            break

    try:
        host_to_use = hosts[int(host_idx) - 1]
        return host_to_use
    except (ValueError, IndexError):
        print("Invalid host selection")
        return None

if __name__ == '__main__':
    hosts = get_ssh_hosts()
    handle_ssh_config_menu()
