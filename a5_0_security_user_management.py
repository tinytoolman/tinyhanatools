#-------------------------------------------------------------------------------
# Name:        a5_0_security_user_management.py
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
import a5_1_modify_user

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_security_user_management_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Security and User Management Menu - {hostname}")
    print_bold("-------------------")
    print("1.  Create User")
    print("2.  Modify User")
    print("3.  Delete User")
    print("4.  Create Role")
    print("5.  Modify Role")
    print("6.  Delete Role")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        create_user(selected_userstore)
    elif choice == '2':
        a5_1_modify_user.handle_modify_user_menu(selected_userstore)
    elif choice == '3':
        delete_user(selected_userstore)
    elif choice == '4':
        create_role(selected_userstore)
    elif choice == '5':
        modify_role(selected_userstore)
    elif choice == '6':
        delete_role(selected_userstore)
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    input("Press Enter to continue...")
    handle_security_user_management_menu(selected_userstore)

import getpass

def create_user(selected_userstore):
    clear_screen()
    print(f"Creating User with Userstore: {selected_userstore}")
    print("")

    attempts = 0
    while attempts < 2:
        username = input("Enter the username for the new user: ")
        if not username:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    attempts = 0
    while attempts < 2:
        password = getpass.getpass("Enter the password for the new user: ")
        if not password:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    attempts = 0
    while attempts < 2:
        force_change = input("Force first password change (Y/N) [N]: ") or 'n'
        if force_change.lower() not in ['y', 'n']:
            attempts += 1
            print("Wrong Input.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    permissions = input("Enter the comma-separated list of permissions to grant: ").strip()

    attempts = 0
    while attempts < 2:
        disable_lifetime = input("Disable password lifetime (Y/N) [N]: ") or 'N'
        if disable_lifetime.lower() not in ['y', 'n']:
            attempts += 1
            print("Wrong Input.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    '''
    sql_commands = [
        f"CREATE USER {username} PASSWORD {password} {'FORCE PASSWORD CHANGE' if force_change.upper() == 'Y' else ''};",
        f"GRANT {permissions} TO {username};",
        f"ALTER USER {username} {'DISABLE PASSWORD LIFETIME' if disable_lifetime.upper() == 'Y' else 'ENABLE PASSWORD LIFETIME'};"
    ]
    '''

    sql_commands = [
        f"CREATE USER {username} PASSWORD {password} {'FORCE PASSWORD CHANGE' if force_change.upper() == 'Y' else ''};"
    ]

    if permissions:
        sql_commands.append(f"GRANT {permissions} TO {username};")

    sql_commands.append(f"ALTER USER {username} {'DISABLE PASSWORD LIFETIME' if disable_lifetime.upper() == 'Y' else 'ENABLE PASSWORD LIFETIME'};")


    '''
    sql_commands = [
        f"CREATE USER {username} PASSWORD {password} {'FORCE_FIRST_PASSWORD_CHANGE' if force_change.upper() == 'Y' else ''};"
    ]

    # Adding the GRANT command only if permissions are specified
    if permissions:
        sql_commands.append(f"GRANT {permissions} TO {username};")

    sql_commands.append(f"ALTER USER {username} {'DISABLE PASSWORD LIFETIME' if disable_lifetime.upper() == 'Y' else 'ENABLE PASSWORD LIFETIME'};")
    '''

    try:
        for sql_script in sql_commands:
            print(str(command) + " : " + str(sql_script))
            subprocess.run(command + [sql_script], encoding='utf-8', check=True)

        print("User created successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error creating user: {ex.stderr}")
    except Exception as ex:
        print(f"Error creating user: {str(ex)}")

def delete_user(selected_userstore):
    clear_screen()
    print(f"Deleting User with Userstore: {selected_userstore}")
    print("")

    attempts = 0
    while attempts < 2:
        username = input("Enter the username to delete: ")
        if not username:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                return
            continue
        else:
            break

    attempts = 0
    while attempts < 2:
        confirm = input(f"Are you sure you want to delete the user '{username}'? (Y/N): ")
        if confirm.lower() not in ['y', 'n']:
            attempts += 1
            print("Wrong Input.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    if confirm.upper() == 'Y':
        key = selected_userstore.split()[1]
        command = ["hdbsql", "-U", key]

        try:
            sql_command = f"DROP USER {username};"
            subprocess.run(command + [sql_command], encoding='utf-8', check=True)
            print(f"User '{username}' deleted successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error deleting user: {ex.stderr}")
        except Exception as ex:
            print(f"Error deleting user: {str(ex)}")
    else:
        print("User deletion cancelled.")

def create_role(selected_userstore):
    clear_screen()
    print(f"Creating Role with Userstore: {selected_userstore}")
    print("")

    role_name = input("Enter the name for the new role: ")
    privileges = input("Enter the comma-separated list of privileges to grant: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    try:
        sql_commands = [
            f"CREATE ROLE {role_name};",
            f"GRANT {privileges} TO {role_name};"
        ]

        for sql_script in sql_commands:
            subprocess.run(command + [sql_script], encoding='utf-8', check=True)

        print("Role created successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error creating role: {ex.stderr}")
    except Exception as ex:
        print(f"Error creating role: {str(ex)}")

    input("Press Enter to continue...")

def modify_role(selected_userstore):
    clear_screen()
    print(f"Modifying Role with Userstore: {selected_userstore}")
    print("")

    role_name = input("Enter the name of the role to modify: ")

    action = input("Would you like to add or revoke privileges? Enter 'add' or 'revoke': ")
    if action.lower() not in ['add', 'revoke']:
        print("Invalid action. Please try again.")
        return

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    if action.lower() == 'add':
        privileges = input("Enter the comma-separated list of privileges to add: ")
        sql_command = f"GRANT {privileges} TO {role_name};"
    else:  # action is 'revoke'
        try:
            output = subprocess.check_output(command + [f"SELECT PRIVILEGE FROM GRANTED_PRIVILEGES WHERE GRANTEE = '{role_name}';"], encoding='utf-8')
            print("Current privileges:")
            privileges = output.splitlines()[1:-2]  # Remove the header and footer lines
            for i, privilege in enumerate(privileges, start=1):
                print(f"{i}. {privilege}")
            privilege_nums = input("Enter the numbers of the privileges to revoke, separated by commas: ")
            privilege_nums = [int(num) for num in privilege_nums.split(",")]
            revoked_privileges = ",".join(privileges[i-1] for i in privilege_nums)
            sql_command = f"REVOKE {revoked_privileges} FROM {role_name};"
        except subprocess.CalledProcessError as ex:
            print(f"Error retrieving current privileges: {ex.stderr}")
            return
        except Exception as ex:
            print(f"Error retrieving current privileges: {str(ex)}")
            return

    try:
        subprocess.run(command + [sql_command], encoding='utf-8', check=True)
        print("Role modified successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error modifying role: {ex.stderr}")
    except Exception as ex:
        print(f"Error modifying role: {str(ex)}")

    input("Press Enter to continue...")

def delete_role(selected_userstore):
    clear_screen()
    print(f"Deleting Role with Userstore: {selected_userstore}")
    print("")

    role_name = input("Enter the name of the role to delete: ")
    confirm = input(f"Are you sure you want to delete the role '{role_name}'? (Y/N): ")

    if confirm.upper() == 'Y':
        key = selected_userstore.split()[1]
        command = ["hdbsql", "-U", key]

        try:
            sql_command = f"DROP ROLE {role_name};"
            subprocess.run(command + [sql_command], encoding='utf-8', check=True)
            print(f"Role '{role_name}' deleted successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error deleting role: {ex.stderr}")
        except Exception as ex:
            print(f"Error deleting role: {str(ex)}")
    else:
        print("Role deletion cancelled.")

    input("Press Enter to continue...")

if __name__ == '__main__':
    handle_security_user_management_menu()


