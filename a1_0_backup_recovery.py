#-------------------------------------------------------------------------------
# Name:        a1_0_backup_recovery.py
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
import a2_0_database_administration

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_backup_recovery_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Backup and Recovery Menu - {hostname}")
    print(f"{selected_userstore}")
    print_bold("-------------------")
    print("1.  Perform Full Database Backup")
    print("2.  Perform Incremental Backup")
    print("3.  Perform Differential Backup")
    print("4.  Perform Tenant Database Full Recovery")
    print("5.  Perform SystemDB Database Full Recovery")
    print("6.  Stop Tenant Database")
    print("7.  Verify Backup")
    print("8.  Create Backup Operator User")
    print("9.  Delete Backup File from Directory")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input('\033[1m' + text + '\033[0m')
    if choice == '1':
        perform_full_backup(selected_userstore)
    elif choice == '2':
        perform_incremental_backup(selected_userstore)
    elif choice == '3':
        perform_differential_backup(selected_userstore)
    elif choice == '4':
        perform_tenant_database_full_recovery(selected_userstore)
    elif choice == '5':
        perform_systemdb_full_recovery(selected_userstore)
    elif choice == '6':
        a2_0_database_administration.stop_tenant_db(selected_userstore)
    #elif choice == '6':
    #    perform_database_reset(selected_userstore)
        #RECOVER DATA USING FILE ('/backup/THURSDAY') CLEAR LOG;
    elif choice == '7':
        verify_backup(selected_userstore)
    elif choice == '8':
        create_backup_operator_user(selected_userstore)
    elif choice == '9':
        delete_backup_file()
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    # Wait for user input to return to the backup recovery menu
    input("Press Enter to continue...")
    handle_backup_recovery_menu(selected_userstore)

def perform_full_backup(selected_userstore):
    clear_screen()
    a2_0_database_administration.check_installed_db(selected_userstore)
    print(f"\nPerforming Full Database Backup with userstore {selected_userstore}\n")

    db_name = input("Enter the name of the database to perform a full backup [SYSTEMDB]: ") or 'SYSTEMDB'

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        backup_path = input("Enter the full backup file directory path: ")
        if not backup_path:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif not os.path.exists(backup_path):
            attempts2 += 1
            print("Invalid location, Directory locacation does not exist.")
            if attempts2 == 2:
                return
            continue
        else:
            break

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        user_input = input("To start the " + str(db_name) + " backup enter 'backup': ")
        if not user_input:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif user_input.lower() != 'backup':
            attempts2 += 1
            print("Value entered is not equal to \033[1mbackup\033[0m")
            if attempts2 == 2:
                return
            continue
        else:
            break

    if user_input.lower() == 'backup':
        try:
            sql_script = f"BACKUP DATA FOR {db_name} USING FILE ('{backup_path}', '{db_name}_FULL');"
            print("Command: " + str(sql_script))
            input("Press Enter to continue...")
            subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
            print(f"Database '{db_name}' backed up successfully.")
            #input("Press any key to continue...")
        except subprocess.CalledProcessError as ex:
            print(f"Error backing up database: {ex.stderr}")
        except Exception as ex:
            print(f"Error backing up database: {str(ex)}")

def perform_incremental_backup(selected_userstore):
    clear_screen()
    a2_0_database_administration.check_installed_db(selected_userstore)
    print(f"Performing Incremental Backup with userstore {selected_userstore}")

    db_name = input("Enter the name of the database to perform an incremental backup [SYSTEMDB]: ") or 'SYSTEMDB'

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        backup_path = input("Enter the full backup file directory path: ")
        if not backup_path:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif not os.path.exists(backup_path):
            attempts2 += 1
            print("Invalid location, Directory locacation does not exist.")
            if attempts2 == 2:
                return
            continue
        else:
            break

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        user_input = input("To start the " + str(db_name) + " incremental backup enter 'backup': ")
        if not user_input:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif user_input.lower() != 'backup':
            attempts2 += 1
            print("Value entered is not equal to \033[1mbackup\033[0m")
            if attempts2 == 2:
                return
            continue
        else:
            break

    if user_input.lower() == 'backup':
        try:
            sql_script = f"BACKUP DATA INCREMENTAL FOR {db_name} USING FILE ('{backup_path}', '{db_name}');"
            print("Command: " + str(sql_script))
            input("Press Enter to continue...")
            subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
            print(f"Database '{db_name}' incrementally backed up successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error performing incremental backup: {ex.stderr}")
        except Exception as ex:
            print(f"Error performing incremental backup: {str(ex)}")

def perform_differential_backup(selected_userstore):
    clear_screen()
    a2_0_database_administration.check_installed_db(selected_userstore)
    print(f"Performing Differential Backup with userstore {selected_userstore}")

    db_name = input("Enter the name of the database to perform a differential backup [SYSTEMDB]: ") or 'SYSTEMDB'

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        backup_path = input("Enter the full backup file directory path: ")
        if not backup_path:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif not os.path.exists(backup_path):
            attempts2 += 1
            print("Invalid location, Directory locacation does not exist.")
            if attempts2 == 2:
                return
            continue
        else:
            break

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        user_input = input("To start the " + str(db_name) + " differential backup enter 'backup': ")
        if not user_input:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif user_input.lower() != 'backup':
            attempts2 += 1
            print("Value entered is not equal to \033[1mbackup\033[0m")
            if attempts2 == 2:
                return
            continue
        else:
            break

    if user_input.lower() == 'backup':
        try:
            sql_script = f"BACKUP DATA DIFFERENTIAL FOR {db_name} USING FILE ('{backup_path}', '{db_name}');"
            print("Command: " + str(sql_script))
            input("Press Enter to continue...")
            subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
            print(f"Database '{db_name}' differentially backed up successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error performing differential backup: {ex.stderr}")
        except Exception as ex:
            print(f"Error performing differential backup: {str(ex)}")

def perform_tenant_database_full_recovery(selected_userstore):
    clear_screen()
    a2_0_database_administration.check_installed_tenant_db(selected_userstore)
    print("Performing Database Recovery")

    attempts = 0
    while attempts < 2:
        db_name = input("Enter the name of the database to perform the recovery (Enter SID): ")
        if not db_name:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                return
            continue
        else:
            break

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        backup_path = input("Enter the full backup file directory path: ")
        if not backup_path:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif not os.path.exists(backup_path):
            attempts2 += 1
            print("Invalid location, Directory locacation does not exist.")
            if attempts2 == 2:
                return
            continue
        else:
            break

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        user_input = input("To start Tenant Database Recovery type 'recover': ")
        if not user_input:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        elif user_input.lower() != 'recover':
            attempts2 += 1
            print("Value entered is not equal to \033[1mrecover\033[0m")
            if attempts2 == 2:
                return
            continue
        else:
            break

    if user_input.lower() == 'recover':
        sql_script = f"RECOVER DATA FOR {db_name} USING FILE ('{backup_path}/{db_name}_FULL') CLEAR LOG;"
        print("Recover Tenant Data command to be executed:")
        print(sql_script)
        input("Press Enter to continue...")

        try:
            sql_script = f"RECOVER DATA FOR {db_name} USING FILE ('{backup_path}/{db_name}_FULL') CLEAR LOG;"
            subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
            print(f"Database '{db_name}' recovered successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error recovering database: {ex.stderr}")
        except Exception as ex:
            print(f"Error recovering database: {str(ex)}")
    else:
        print("Invalid input. Tenant Recovery aborted. Exiting function")

def perform_systemdb_full_recovery(selected_userstore):
    clear_screen()
    print("Performing SystemDB Recovery")

    key = selected_userstore.split()[1]
    command = ["HDBSettings.sh", "recoverSys.py"]

    user_input = input("To start SystemDB Recovery type 'recover': ")
    if user_input.lower() == 'recover':
        print("Command: " + command)
        print("")
        input("Press Enter to continue...")

        try:
            subprocess.run(command, encoding='utf-8', check=True)
            print(f"Database '{db_name}' recovered successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error recovering database: {ex.stderr}")
        except Exception as ex:
            print(f"Error recovering database: {str(ex)}")
    else:
        print("Invalid input. SystemDB Recovery aborted. Exiting function")

def verify_backup(selected_userstore):
    while True:
        clear_screen()
        print("Verify Backup")
        print("-------------")
        print("0. Back to Previous Menu")
        print("------------------------")

        attempts = 0
        attempts2 = 0
        while attempts < 2:
            backup_dir = input("Enter the backup directory path: ")
            if not backup_dir:
                attempts += 1
                print("Nothing entered.")
                if attempts == 2:
                    return
                continue
            elif backup_dir == '0':
                return
            elif not os.path.exists(backup_dir):
                attempts2 += 1
                print("Invalid location, Directory loccation does not exist.")
                if attempts2 == 2:
                    return
                continue
            else:
                break

        '''
        if backup_dir == '0':
            return
        if not backup_dir:
            print("No backup directory specified.")
            input("Press Enter to continue...")
            continue
        if not os.path.exists(backup_dir):
            print("The specified backup directory does not exist.")
            input("Press Enter to continue...")
            continue
        '''

        backup_files = os.listdir(backup_dir)

        if not backup_files:
            print("No backup files found in the specified directory.")
            input("Press Enter to continue...")
            continue

        print("Backup Files:")
        for i, file in enumerate(backup_files, start=1):
            print(f"{i}. {file}")

        print("")

        choice = input("Enter the number corresponding to the file to verify (or 0 to go back): ")
        if choice == '0':
            return
        elif choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(backup_files):
                file_to_check = os.path.join(backup_dir, backup_files[index])
                run_backup_check(file_to_check)
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Invalid choice. Please try again.")

        input("Press Enter to continue...")

def run_backup_check(backup_file):
    clear_screen()
    print(f"Running backup check for file: {backup_file}\n")

    try:
        output = subprocess.check_output(["hdbbackupcheck", "-v", backup_file], encoding='utf-8')
        print(output)
    except subprocess.CalledProcessError as ex:
        print(f"Error running backup check: {ex.stderr}")
    except Exception as ex:
        print(f"Error running backup check: {str(ex)}")

def delete_backup_file():
    clear_screen()
    while True:
        attempts = 0
        attempts2 = 0
        while attempts < 2:
            backup_dir = input("Enter the backup directory path: ")
            if not backup_dir:
                attempts += 1
                print("Nothing entered.")
                if attempts == 2:
                    print("Going back to menu.")
                    return
                continue
            elif not os.path.exists(backup_dir):
                attempts2 += 1
                print("Invalid location, Directory locacation does not exist.")
                if attempts2 == 2:
                    return
                continue
            else:
                break

        backup_files = os.listdir(backup_dir)

        if not backup_files:
            print("No backup files found in the specified directory.")
            return

        while True:
            print("Backup Files:")
            for i, file in enumerate(backup_files, start=1):
                print(f"{i}. {file}")

            choice = input("Enter the number corresponding to the file to delete (or 0 to go back): ")
            if choice == '0':
                return
            elif choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(backup_files):
                    file_to_delete = os.path.join(backup_dir, backup_files[index])
                    confirm = input(f"Are you sure you want to delete '{file_to_delete}'? (Y/N): ")
                    if confirm.upper() == 'Y':
                        try:
                            os.remove(file_to_delete)
                            print(f"Backup file '{file_to_delete}' deleted successfully.")
                        except Exception as ex:
                            print(f"Error deleting backup file '{file_to_delete}': {str(ex)}")
                    else:
                        print("Deletion canceled.")
                else:
                    clear_screen()
                    print("Invalid choice. Please try again.")
            else:
                clear_screen()
                print("Invalid choice. Please try again.")

            remaining_files = os.listdir(backup_dir)
            if not remaining_files:
                print("No backup files remaining.")
                return

            print("Remaining Files:")
            for i, file in enumerate(remaining_files, start=1):
                print(f"{i}. {file}")

            choice = input("Enter the number corresponding to another file to delete (or 0 to go back): ")
            if choice == '0':
                return
            elif choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(remaining_files):
                    file_to_delete = os.path.join(backup_dir, remaining_files[index])
                    confirm = input(f"Are you sure you want to delete '{file_to_delete}'? (Y/N): ")
                    if confirm.upper() == 'Y':
                        try:
                            os.remove(file_to_delete)
                            print(f"Backup file '{file_to_delete}' deleted successfully.")
                        except Exception as ex:
                            print(f"Error deleting backup file '{file_to_delete}': {str(ex)}")
                    else:
                        print("Deletion canceled.")
                else:
                    clear_screen()
                    print("Invalid choice. Please try again.")
            else:
                clear_screen()
                print("Invalid choice. Please try again.")

def create_backup_operator_user(selected_userstore):
    clear_screen()
    print("Creating Backup Operator User")

    attempts = 0
    attempts2 = 0
    while attempts < 2:
        username = input("Enter the username for the new backup operator: ")
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
    attempts2 = 0
    while attempts < 2:
        password = getpass.getpass("Enter the password for the new backup operator: ")
        if not password:
            attempts += 1
            print("Nothing entered.")
            if attempts == 2:
                print("Going back to menu.")
                return
            continue
        else:
            break

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    try:
        sql_commands = [
            f"CREATE USER {username} PASSWORD {password} NO FORCE_FIRST_PASSWORD_CHANGE;",
            f"GRANT BACKUP ADMIN, CATALOG READ, BACKUP OPERATOR, MONITORING TO {username};",
            f"ALTER USER {username} DISABLE PASSWORD LIFETIME;"
        ]

        for sql_script in sql_commands:
            subprocess.run(command, input=sql_script, encoding='utf-8', check=True)

        print("Backup operator user created successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error creating backup operator user: {ex.stderr}")
    except Exception as ex:
        print(f"Error creating backup operator user: {str(ex)}")

def create_userstore_entry_func(key, host, port, database, user, password):
    command = f"hdbuserstore set {key} {host}:{port}@{database} {user} {password}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Userstore entry created successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error creating userstore entry: {str(ex)}")

if __name__ == '__main__':
    handle_backup_recovery_menu(None)

