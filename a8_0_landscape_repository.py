#-------------------------------------------------------------------------------
# Name:        a8_0_landscape_repository.py
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
import json
import subprocess
import a6_0_ssh_config
import a8_1_landscape_functions

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_landscape_repository_menu(selected_userstore, host_to_add=None):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Repository Landscape Menu - {hostname}")
    print_bold("-------------------")
    print("1.  Create New Landscape Repository")
    print("2.  Rename Landscape Repository")
    print("3.  Delete Landscape Repository")
    print("4.  Add New Hostname Reference")
    print("5.  Delete Hostname Reference")
    print("6.  Arrange Hostname Reference")
    print("7.  Show Repository and Reference")
    print("8.  Landscape Functions")
    print("0.  Back")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        create_repository(selected_userstore)
    elif choice == '2':
        rename_repository(selected_userstore)
    elif choice == '3':
        delete_repository(selected_userstore)
    elif choice == '4':
        if host_to_add:
            add_hostname(selected_userstore, host_to_add)
        else:
            add_hostname(selected_userstore)
    elif choice == '5':
        del_hostname(selected_userstore)
    elif choice == '6':
        arrange_hostname(selected_userstore)
    elif choice == '7':
        show_repository(selected_userstore)
    elif choice == '8':
        a8_1_landscape_functions.handle_landscape_repository_menu()
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    handle_landscape_repository_menu(selected_userstore)

def create_repository(selected_userstore):
    clear_screen()
    print("Create New Landscape Repository")

    # Get the repository name from the user
    repo_name = input("Enter the name for the new repository: ")

    # Get the home directory path
    home_dir = os.path.expanduser("~")

    # Create the full path to the .repository_hosts.json file
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    # Check if the .repository_hosts.json file exists and load existing data
    repositories = []
    if os.path.exists(repo_file_path):
        with open(repo_file_path, 'r') as file:
            repositories = json.load(file)

    # Get the list of SSH hosts from .ssh_hosts.json
    ssh_hosts = a6_0_ssh_config.get_ssh_hosts()  # Use get_ssh_hosts from a6_0_ssh_config

    # Show the list of SSH hosts to the user and ask for their choice
    print("Available SSH Hosts:")
    for i, host in enumerate(ssh_hosts, start=1):
        print(f"{i}. {host}")

    host_choice = input("Select the number of the host you want to link to the repository (or press Enter to skip): ")
    try:
        if host_choice:
            host_choice = int(host_choice)
            if 1 <= host_choice <= len(ssh_hosts):
                host_name = ssh_hosts[host_choice - 1]
            else:
                print("Invalid host choice.")
                input("Press Enter to continue...")
                return
        else:
            host_name = None
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    # Create a list to store the systems and their instance numbers
    systems = []

    if host_name:
        # Ask the user to enter the instance number for the system
        tinstance = os.environ.get('TINSTANCE')
        default_instance = tinstance if tinstance else '00'
        instance = input(f"Please enter the instance number for {host_name} [{default_instance}]: ")
        if not instance:
            instance = default_instance

        # Create a dictionary to store the system information, including the "instance" field
        system_info = {
            "name": host_name,
            "instance": instance
        }

        systems.append(system_info)

    # Create a dictionary to store the repository information
    repository = {
        "name": repo_name,
        "systems": systems
    }

    # Add the new repository to the list
    repositories.append(repository)

    # Write the updated list of repositories to the .repository_hosts.json file
    with open(repo_file_path, 'w') as file:
        json.dump(repositories, file)

    print(f"New repository '{repo_name}' created successfully.")

def rename_repository(selected_userstore):
    clear_screen()
    print("Rename Landscape Repository")

    # Get the home directory path
    home_dir = os.path.expanduser("~")

    # Create the full path to the .repository_hosts.json file
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    # Check if the .repository_hosts.json file exists
    if not os.path.exists(repo_file_path):
        print("No repository exists. Create a new repository first.")
        input("Press Enter to continue...")
        return

    # Load the repositories data from the .repository_hosts.json file
    with open(repo_file_path, 'r') as file:
        repositories = json.load(file)

    # Display all repositories and ask the user to select one
    print("Available Repositories:")
    for i, repo in enumerate(repositories, start=1):
        print(f"{i}. {repo['name']}")

    repo_choice = input("Select the number of the repository you want to rename: ")
    try:
        repo_choice = int(repo_choice)
        if 1 <= repo_choice <= len(repositories):
            selected_repo = repositories[repo_choice - 1]
        else:
            print("Invalid repository choice.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    new_name = input("Enter the new name for the repository: ")
    if not new_name:
        print("Invalid input. The new name cannot be empty.")
        input("Press Enter to continue...")
        return

    selected_repo['name'] = new_name

    # Update the repository data in the .repository_hosts.json file
    with open(repo_file_path, 'w') as file:
        json.dump(repositories, file)

    print(f"The repository has been renamed to '{new_name}'.")

    input("Press Enter to continue...")

def delete_repository(selected_userstore):
    clear_screen()
    print("Delete Landscape Repository")

    # Get the home directory path
    home_dir = os.path.expanduser("~")

    # Create the full path to the .repository_hosts.json file
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    # Check if the .repository_hosts.json file exists
    if not os.path.exists(repo_file_path):
        print("No repository exists. Create a new repository first.")
        input("Press Enter to continue...")
        return

    # Load the repositories data from the .repository_hosts.json file
    with open(repo_file_path, 'r') as file:
        repositories = json.load(file)

    # Display all repositories and ask the user to select one
    print("Available Repositories:")
    for i, repo in enumerate(repositories, start=1):
        print(f"{i}. {repo['name']}")

    repo_choice = input("Select the number of the repository you want to delete: ")
    try:
        repo_choice = int(repo_choice)
        if 1 <= repo_choice <= len(repositories):
            selected_repo = repositories[repo_choice - 1]
        else:
            print("Invalid repository choice.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    # Confirm deletion with the user
    confirm = input(f"Are you sure you want to delete the repository '{selected_repo['name']}'? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Repository deletion canceled.")
        input("Press Enter to continue...")
        return

    # Remove the selected repository from the list
    repositories.remove(selected_repo)

    # Update the repository data in the .repository_hosts.json file
    with open(repo_file_path, 'w') as file:
        json.dump(repositories, file)

    print(f"The repository '{selected_repo['name']}' has been deleted.")

    input("Press Enter to continue...")

def add_hostname(selected_userstore):
    clear_screen()
    print("Add New System Reference")

    # Get the home directory path
    home_dir = os.path.expanduser("~")

    # Create the full path to the .repository_hosts.json file
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    # Check if the .repository_hosts.json file exists
    if not os.path.exists(repo_file_path):
        print("No repository exists. Create a new repository first.")
        input("Press Enter to continue...")
        return

    # Load the repositories data from the .repository_hosts.json file
    with open(repo_file_path, 'r') as file:
        repositories = json.load(file)

    # List the available repositories and prompt for choice
    print("Available Repositories:")
    for i, repo in enumerate(repositories, start=1):
        print(f"{i}. {repo['name']}")

    repo_choice = input("Select the number of the repository (or press Enter to skip): ")
    try:
        if repo_choice:
            repo_choice = int(repo_choice)
            if 1 <= repo_choice <= len(repositories):
                selected_repo = repositories[repo_choice - 1]
            else:
                print("Invalid repository choice.")
                input("Press Enter to continue...")
                return
        else:
            print("No repository selected.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    # Get the list of SSH hosts from .ssh_hosts.json
    ssh_hosts = a6_0_ssh_config.get_ssh_hosts()

    # Show the list of SSH hosts to the user and ask for their choice
    print("Available SSH Hosts:")
    for i, host in enumerate(ssh_hosts, start=1):
        print(f"{i}. {host}")

    host_choice = input("Select the number of the host you want to add: ")
    try:
        host_choice = int(host_choice)
        if 1 <= host_choice <= len(ssh_hosts):
            host_name = ssh_hosts[host_choice - 1]
        else:
            print("Invalid host choice.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    # Check if the host is already in the selected repository
    for system in selected_repo['systems']:
        if system['name'] == host_name:
            print(f"The host '{host_name}' is already in the repository.")
            input("Press Enter to continue...")
            return

    # Ask the user to enter the instance number for the system
    tinstance = os.environ.get('TINSTANCE')
    default_instance = tinstance if tinstance else '00'
    instance = input(f"Please enter the instance number for {host_name} [{default_instance}]: ")
    if not instance:
        instance = default_instance

    # Create a dictionary to store the system information, including the "instance" field
    system_info = {
        "name": host_name,
        "instance": instance
    }

    # Add the new system to the selected repository and save the changes
    selected_repo['systems'].append(system_info)

    # Update the repository data in the .repository_hosts.json file
    with open(repo_file_path, 'w') as file:
        json.dump(repositories, file)

    print(f"The host '{host_name}' has been added to the repository.")

def del_hostname(selected_userstore):
    # Load all repositories
    repositories = get_repositories()

    if not repositories:
        print("No repositories found.")
        input("Press Enter to continue...")
        return

    # Display all repositories and ask the user to select one
    print("Available Repositories:")
    for i, repo in enumerate(repositories, start=1):
        print(f"{i}. {repo['name']}")

    repo_choice = input("Select the number of the repository (or press Enter to skip): ")
    try:
        if repo_choice:
            repo_choice = int(repo_choice)
            if 1 <= repo_choice <= len(repositories):
                selected_repo = repositories[repo_choice - 1]
            else:
                print("Invalid repository choice.")
                input("Press Enter to continue...")
                return
        else:
            print("No repository selected.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    systems = selected_repo.get('systems', [])

    if not systems:
        print("No systems found in the selected repository.")
        input("Press Enter to continue...")
        return

    print("Systems in the Repository:")
    for i, system_info in enumerate(systems, start=1):
        system_name = system_info['name']
        instance = system_info.get('instance', '00')
        print(f"{i}. {system_name}, instance {instance}")

    sys_idx = input("Select the number of the host you want to delete: ")
    try:
        sys_idx = int(sys_idx)
        if sys_idx < 1 or sys_idx > len(systems):
            raise ValueError
    except ValueError:
        print("Invalid system selection.")
        return

    # Remove the selected system from the repository
    system_to_delete = systems[sys_idx - 1]
    systems.remove(system_to_delete)

    # Get the home directory path
    home_dir = os.path.expanduser("~")

    # Create the full path to the .repository_hosts.json file
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    # Update the repository file with the modified systems list
    selected_repo['systems'] = systems
    with open(repo_file_path, 'w') as file:
        json.dump(repositories, file)

    print(f"System '{system_to_delete['name']}, instance {system_to_delete.get('instance', '00')}' removed from the repository '{selected_repo['name']}'.")

    input("Press Enter to continue...")

def arrange_hostname(selected_userstore):
    clear_screen()
    print("Arrange Hostname Reference")

    # Get the home directory path
    home_dir = os.path.expanduser("~")

    # Create the full path to the .repository_hosts.json file
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    # Check if the .repository_hosts.json file exists
    if not os.path.exists(repo_file_path):
        print("No repository exists. Create a new repository first.")
        input("Press Enter to continue...")
        return

    # Load the repositories data from the .repository_hosts.json file
    with open(repo_file_path, 'r') as file:
        repositories = json.load(file)

    # Display all repositories and ask the user to select one
    print("Available Repositories:")
    for i, repo in enumerate(repositories, start=1):
        print(f"{i}. {repo['name']}")

    repo_choice = input("Select the number of the repository (or press Enter to skip): ")
    try:
        if repo_choice:
            repo_choice = int(repo_choice)
            if 1 <= repo_choice <= len(repositories):
                selected_repo = repositories[repo_choice - 1]
            else:
                print("Invalid repository choice.")
                input("Press Enter to continue...")
                return
        else:
            print("No repository selected.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    # Show the selected repository name and associated systems to the user
    print(f"Repository Name: {selected_repo['name']}")
    print("Systems in the Repository:")
    for i, system_info in enumerate(selected_repo['systems'], start=1):
        system_name = system_info['name']
        instance = system_info.get('instance', '00')
        print(f"{i}. {system_name}, instance {instance}")

    # Ask the user to enter the new order of the systems
    user_input = input("Enter the new order of systems (comma-separated list of numbers): ")

    try:
        new_order_list = [int(x.strip()) for x in user_input.split(',')]
        if len(new_order_list) != len(selected_repo['systems']):
            raise ValueError
        for idx in new_order_list:
            if idx < 1 or idx > len(selected_repo['systems']):
                raise ValueError
    except ValueError:
        print("Invalid input. Please enter a comma-separated list of valid numbers.")
        input("Press Enter to continue...")
        return

    # Rearrange the systems in the repository according to the new order
    selected_repo['systems'] = [selected_repo['systems'][idx - 1] for idx in new_order_list]

    # Update the repository data in the .repository_hosts.json file
    with open(repo_file_path, 'w') as file:
        json.dump(repositories, file)

    print("Hostname references have been rearranged successfully.")

    input("Press Enter to continue...")

def show_repository(selected_userstore):
    clear_screen()
    print("Show Repository and Reference")

    # Get the home directory path
    home_dir = os.path.expanduser("~")

    # Create the full path to the .repository_hosts.json file
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    # Check if the .repository_hosts.json file exists
    if not os.path.exists(repo_file_path):
        print("No repository exists. Create a new repository first.")
        input("Press Enter to continue...")
        return None

    # Load the repositories data from the .repository_hosts.json file
    with open(repo_file_path, 'r') as file:
        repositories = json.load(file)

    # Display all repositories and ask the user to select one
    print("Available Repositories:")
    for i, repo in enumerate(repositories, start=1):
        print(f"{i}. {repo['name']}")

    repo_choice = input("Select the number of the repository (or press Enter to skip): ")
    try:
        if repo_choice:
            repo_choice = int(repo_choice)
            if 1 <= repo_choice <= len(repositories):
                selected_repo = repositories[repo_choice - 1]
            else:
                print("Invalid repository choice.")
                input("Press Enter to continue...")
                return
        else:
            print("No repository selected.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    # Show the selected repository name and associated systems to the user
    print(f"Repository Name: {selected_repo['name']}")
    print("Systems in the Repository:")
    for i, system_info in enumerate(selected_repo['systems'], start=1):
        system_name = system_info['name']
        instance = system_info.get('instance', '00')
        print(f"{i}. {system_name}, instance {instance}")

    input("Press Enter to continue...")

    # Return the selected repository
    return selected_repo

def get_repositories():
    home_dir = os.path.expanduser("~")
    repo_file_path = os.path.join(home_dir, '.repository_hosts.json')

    if not os.path.exists(repo_file_path):
        return []  # Return an empty list if the file does not exist

    with open(repo_file_path, 'r') as file:
        return json.load(file)  # Load the list of repositories from the file

if __name__ == '__main__':
    handle_landscape_repository_menu(None)
