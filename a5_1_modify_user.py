#-------------------------------------------------------------------------------
# Name:        a5_1_modify_user.py
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

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_modify_user_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Modify User - {hostname}")
    print_bold("-------------------")
    print("1.  Change Password")
    print("2.  Lock/Unlock User Account")
    print("3.  Grant/Revoke Roles")
    print("4.  Check Assigned Roles/Privileges")
    print("5.  Set Password Lifetime Enable/Disable")
    print("6.  Change User Validity")
    print("7.  Check User Attributes")
    print("0.  Back")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        change_password(selected_userstore)
    elif choice == '2':
        lock_unlock_account(selected_userstore)
    elif choice == '3':
        grant_revoke_roles(selected_userstore)
    elif choice == '4':
        check_assigned_role_priv(selected_userstore)
    elif choice == '5':
        set_password_lifetime(selected_userstore)
    elif choice == '6':
        change_user_validity(selected_userstore)
    elif choice == '7':
        check_user_attributes(selected_userstore)
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    input("Press Enter to continue...")
    handle_modify_user_menu(selected_userstore)

def change_password(selected_userstore):
    clear_screen()
    print(f"Changing User Password with Userstore: {selected_userstore}")
    print("")

    username = input("Enter the username to change password: ")
    new_password = input("Enter the new password: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    try:
        sql_command = f'ALTER USER {username} PASSWORD "{new_password}";'
        subprocess.run(command + [sql_command], encoding='utf-8', check=True)
        print(f"Password for user '{username}' changed successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error changing password: {ex.stderr}")
    except Exception as ex:
        print(f"Error changing password: {str(ex)}")

def lock_unlock_account(selected_userstore):
    clear_screen()
    print(f"Locking/Unlocking User Account with Userstore: {selected_userstore}")
    print("")

    username = input("Enter the username to lock/unlock: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    # Check the current user locked
    check_command = f"SELECT USER_NAME, USER_DEACTIVATED FROM USERS WHERE USER_NAME = '{username}';"
    try:
        output = subprocess.check_output(command + [check_command], encoding='utf-8')
        print(f"Current user locked setting for '{username}':")
        print(output.strip())
        print()
    except subprocess.CalledProcessError as ex:
        print(f"Error checking user lock status: {ex.stderr}")
        return
    except Exception as ex:
        print(f"Error checking user lock status: {str(ex)}")
        return

    action = input("Do you want to lock 'L' or unlock 'U' the user account? ")

    if action.lower() == 'l':
        try:
            # Lock user account
            sql_command = f"ALTER USER {username} DEACTIVATE USER NOW;"
            subprocess.run(command + [sql_command], encoding='utf-8', check=True)
            print(f"User '{username}' locked successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error locking user: {ex.stderr}")
        except Exception as ex:
            print(f"Error locking user: {str(ex)}")
    elif action.lower() == 'u':
        try:
            # Unlock user account
            sql_command = f"ALTER USER {username} ACTIVATE USER NOW;"
            subprocess.run(command + [sql_command], encoding='utf-8', check=True)
            print(f"User '{username}' unlocked successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error unlocking user: {ex.stderr}")
        except Exception as ex:
            print(f"Error unlocking user: {str(ex)}")
    else:
        print("Invalid choice. Please enter 'L' or 'U' to lock or unlock the user account.")

def grant_revoke_roles(selected_userstore):
    clear_screen()
    print(f"Granting/Revoking Roles with Userstore: {selected_userstore}")
    print("")

    username = input("Enter the username to grant/revoke roles: ")
    roles = input("Enter the comma-separated list of roles to grant/revoke: ").split(',')
    action = input("Do you want to grant 'G' or revoke 'R' these roles? ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    if action.lower() == 'g':
        try:
            for role in roles:
                sql_command = f"GRANT {role.strip()} TO {username};"
                subprocess.run(command + [sql_command], encoding='utf-8', check=True)
            print(f"Roles '{','.join(roles)}' granted to user '{username}' successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error granting roles: {ex.stderr}")
        except Exception as ex:
            print(f"Error granting roles: {str(ex)}")
    elif action.lower() == 'r':
        try:
            for role in roles:
                sql_command = f"REVOKE {role.strip()} FROM {username};"
                subprocess.run(command + [sql_command], encoding='utf-8', check=True)
            print(f"Roles '{','.join(roles)}' revoked from user '{username}' successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error revoking roles: {ex.stderr}")
        except Exception as ex:
            print(f"Error revoking roles: {str(ex)}")
    else:
        print("Invalid choice. Please enter 'grant' or 'revoke'.")

def check_assigned_role_priv(selected_userstore):
    clear_screen()
    print(f"Checking Assigned Roles/Privileges with Userstore: {selected_userstore}")
    print("")

    username = input("Enter the username to check roles/privileges: ")
    print("\nRemember to press 'q' to quit once report is displayed to quit")
    print("You can use page up and page down as well as enter key to navigate\n")
    check_option = input("Do you want to check 'P' for privileges or 'R' for roles? ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    if check_option.lower() == 'p':
        try:
            sql_command = f"SELECT * FROM \"PUBLIC\".\"EFFECTIVE_PRIVILEGES\" WHERE USER_NAME = '{username}';"
            subprocess.run(command + [sql_command], encoding='utf-8', check=True)
        except subprocess.CalledProcessError as ex:
            print(f"Error checking privileges: {ex.stderr}")
        except Exception as ex:
            print(f"Error checking privileges: {str(ex)}")
    elif check_option.lower() == 'r':
        try:
            sql_command = f"SELECT * FROM \"PUBLIC\".\"EFFECTIVE_ROLES\" WHERE USER_NAME = '{username}';"
            subprocess.run(command + [sql_command], encoding='utf-8', check=True)
        except subprocess.CalledProcessError as ex:
            print(f"Error checking roles: {ex.stderr}")
        except Exception as ex:
            print(f"Error checking roles: {str(ex)}")
    else:
        print("Invalid choice. Please enter 'P' for privileges or 'R' for roles.")

def set_password_lifetime(selected_userstore):
    clear_screen()
    print(f"Setting Password Lifetime with Userstore: {selected_userstore}")
    print("")

    username = input("Enter the username to set password lifetime: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    try:
        # Check the current password lifetime setting
        check_command = f"SELECT USER_NAME, IS_PASSWORD_LIFETIME_CHECK_ENABLED from USERS where USER_NAME = '{username}';"
        output = subprocess.check_output(command + [check_command], encoding='utf-8')
        print(f"Current password lifetime setting for user '{username}': {output.strip()}")

        # Ask user to set the password lifetime
        choice = input("Do you want to enable or disable password lifetime? (E/D): ")
        if choice.lower() == 'e':
            sql_command = f"ALTER USER {username} ENABLE PASSWORD LIFETIME;"
        elif choice.lower() == 'd':
            sql_command = f"ALTER USER {username} DISABLE PASSWORD LIFETIME;"
        else:
            print("Invalid choice. Please try again.")
            return

        subprocess.run(command + [sql_command], encoding='utf-8', check=True)
        print(f"Password lifetime for user '{username}' updated successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error setting password lifetime: {ex.stderr}")
    except Exception as ex:
        print(f"Error setting password lifetime: {str(ex)}")

def change_user_validity(selected_userstore):
    clear_screen()
    print(f"Changing User Validity with Userstore: {selected_userstore}")
    print("")

    username = input("Enter the username to change validity: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    try:
        # Check the current validity setting
        check_command = f"SELECT USER_NAME, VALID_FROM, VALID_UNTIL from USERS where USER_NAME = '{username}';"
        output = subprocess.check_output(command + [check_command], encoding='utf-8')
        print(f"Current validity setting for user '{username}': {output.strip()}")

        # Ask user to change the validity
        choice = input("Do you want to change 'Valid From' or 'Valid Until' or 'Both'? (F/U/B): ")
        if choice.upper() == 'F':
            new_date = input("Enter new 'Valid From' date in 'YYYY-MM-DD' format: ")
            sql_command = f"ALTER USER {username} VALID FROM '{new_date}';"
        elif choice.upper() == 'U':
            new_date = input("Enter new 'Valid Until' date in 'YYYY-MM-DD' format: ")
            sql_command = f"ALTER USER {username} VALID UNTIL '{new_date}';"
        elif choice.upper() == 'B':
            new_date_from = input("Enter new 'Valid From' date in 'YYYY-MM-DD' format: ")
            new_date_until = input("Enter new 'Valid Until' date in 'YYYY-MM-DD' format: ")
            sql_command = f"ALTER USER {username} VALID FROM '{new_date_from}' VALID UNTIL '{new_date_until}';"
        else:
            print("Invalid choice. Please try again.")
            return

        subprocess.run(command + [sql_command], encoding='utf-8', check=True)
        print(f"Validity for user '{username}' updated successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error changing user validity: {ex.stderr}")
    except Exception as ex:
        print(f"Error changing user validity: {str(ex)}")

def check_user_attributes(selected_userstore):
    clear_screen()
    print(f"Checking User Attributes with Userstore: {selected_userstore}")
    print("")

    username = input("Enter the username to check attributes: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]

    try:
        sql_command = f"SELECT * FROM USERS WHERE USER_NAME = '{username}';"
        output = subprocess.check_output(command + [sql_command], encoding='utf-8')

        # Print the formatted output
        attributes = output.split('\n')
        column_names = attributes[0].split(',')
        attribute_values = attributes[1].split(',')

        print("\nUser Attributes:")
        print("----------------")
        for column_name, attribute_value in zip(column_names, attribute_values):
            print(f"{column_name}: {attribute_value}")

    except subprocess.CalledProcessError as ex:
        print(f"Error checking user attributes: {ex.stderr}")
    except Exception as ex:
        print(f"Error checking user attributes: {str(ex)}")

if __name__ == '__main__':
    handle_modify_user_menu()
