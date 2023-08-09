#-------------------------------------------------------------------------------
# Name:        a2_0_database_administration.py
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
import a2_1_remote_db_administration

def clear_screen():
    os.system('clear')

def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def handle_database_administration_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"Database Administration Menu - {hostname}")
    print(f"{selected_userstore}")
    print_bold("-------------------")
    print("1.  Check HANA Services running Status")
    print("2.  HANA Overview")
    print("3.  Check Installed Databases")
    print("4.  Start Full DB with HDB start")
    print("5.  Stop Full DB with HDB stop")
    print("6.  Start Tenant Database")
    print("7.  Stop Tenant Database")
    print("8.  Create Tenant Database")
    print("9.  Delete Tenant Database")
    print("10. Show Database Parameters")
    print("11. Remote Database Administration")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input('\033[1m' + text + '\033[0m')
    if choice == '1':
        check_hana_status(selected_userstore)
    elif choice == '2':
        hana_overview(selected_userstore)
    elif choice == '3':
        check_installed_db(selected_userstore)
    elif choice == '4':
        start_full_db(selected_userstore)
    elif choice == '5':
        stop_full_db(selected_userstore)
    elif choice == '6':
        start_tenant_db(selected_userstore)
    elif choice == '7':
        stop_tenant_db(selected_userstore)
    elif choice == '8':
        create_tenant_db(selected_userstore)
    elif choice == '9':
        delete_tenant_database(selected_userstore)
    elif choice == '10':
        show_db_parameters(selected_userstore)
    elif choice == '11':
        a2_1_remote_db_administration.handle_remote_db_administration_menu(selected_userstore)
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    # Wait for user input to return to the database administration menu
    input("Press Enter to continue...")
    handle_database_administration_menu(selected_userstore)

def check_hana_status(selected_userstore):
    clear_screen()
    print("Checking HANA Running Status")

    # Get the TINSTANCE environment variable
    tinstance = os.environ.get('TINSTANCE')
    print("Instance number obtained as:" + str(tinstance)+"\n")
    if tinstance is None:
        print("Error: TINSTANCE environment variable not set.")
        return

    # Run the sapcontrol command
    command = ["sapcontrol", "-nr", tinstance, "-function", "GetProcessList"]

    try:
        subprocess.run(command, check=True)
        print("SAP HANA system status.")
    except subprocess.CalledProcessError as ex:
        if ex.stderr:
            print(f"Error getting SAP HANA system status: {ex.stderr}")
    except Exception as ex:
        print(f"Error getting SAP HANA system status: {str(ex)}")

def hana_overview(selected_userstore):
    clear_screen()
    print("Running SAP HANA System Overview")
    print("Note, a response \"not responding. retry in 5 sec...\""+
    " would autimatically time out after 12 tries if the database is not started."+
    " You would need to start full DB to view Overview")

    # Get the SID and HDB instance number
    sid = os.environ.get('SAPSYSTEMNAME')
    tinstance = os.environ.get('TINSTANCE')
    print(f"SAP SID: {sid}")
    print(f"HDB Instance Number: {tinstance}\n")

    # Change to the python_support directory
    python_support_dir = f"/usr/sap/{sid}/HDB{tinstance}/exe/python_support"
    try:
        os.chdir(python_support_dir)
        print(f"Changed directory to: {python_support_dir}")
    except Exception as ex:
        print(f"Error changing directory: {str(ex)}")
        return

    # Run the systemOverview.py script
    command = ["python", "systemOverview.py"]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as ex:
        if ex.stderr:
            print(f"Error running systemOverview.py: {ex.stderr}")
    except Exception as ex:
        print(f"Error running systemOverview.py: {str(ex)}")

def check_installed_db(selected_userstore):
    clear_screen()
    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]
    sql_script = 'SELECT * FROM "SYS"."M_DATABASES";'

    try:
        result = subprocess.run(command, input=sql_script, encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error executing command: {result.stderr}")
    except subprocess.CalledProcessError as ex:
        print(f"Error executing command: {str(ex)}")
    except Exception as ex:
        print(f"Error executing command: {str(ex)}")

def start_full_db(selected_userstore):
    clear_screen()
    print("Start Full Database with HDB start")

    key = selected_userstore.split()[1]
    command = ["HDB", "start"]

    user_input = input("To start the Full HANA database, type 'start': ")

    if user_input.lower() == 'start':
        try:
            subprocess.run(command, check=True)
            print("SAP HANA system started successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error starting SAP HANA system: {ex.stderr}")
        except Exception as ex:
            print(f"Error starting SAP HANA system: {str(ex)}")
    else:
        print("Invalid input. Database start aborted. Exiting function")

def stop_full_db(selected_userstore):
    clear_screen()
    print("Stop Full Database with HDB stop")

    key = selected_userstore.split()[1]
    command = ["HDB", "stop"]

    user_input = input("To stop the Full HANA database, type 'stop': ")

    if user_input.lower() == 'stop':
        try:
            subprocess.run(command, check=True)
            print("SAP HANA system stopped successfully.")
        except subprocess.CalledProcessError as ex:
            print(f"Error stopping SAP HANA system: {ex.stderr}")
        except Exception as ex:
            print(f"Error stopping SAP HANA system: {str(ex)}")
    else:
        print("Invalid input.  Database stop aborted. Exiting function.")

def start_tenant_db(selected_userstore):
    clear_screen()
    check_installed_db(selected_userstore)
    print("Start Tenant Database")

    db_name = input("Enter the name for tenant database to START: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    user_input = input("To start the " + str(db_name) + " Tenant DB, type 'start': ")

    if user_input.lower() == 'start':
        try:
            sql_script = f"ALTER SYSTEM START DATABASE {db_name};"
            subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
            print(f"Tenant database '{db_name}' started successfully.")
            input("Press any key to continue...")
        except subprocess.CalledProcessError as ex:
            print(f"Error starting tenant database: {ex.stderr}")
        except Exception as ex:
            print(f"Error starting tenant database: {str(ex)}")
    else:
        print("Invalid input.  Tenant Database start aborted. Exiting function")

    clear_screen()
    check_installed_db(selected_userstore)

def stop_tenant_db(selected_userstore):
    clear_screen()
    check_installed_db(selected_userstore)
    print("Stop Tenant Database")

    db_name = input("Enter the name for tenant database to STOP: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    user_input = input("To stop the " + str(db_name) + " Tenant DB, type 'stop': ")

    if user_input.lower() == 'stop':
        try:
            sql_script = f"ALTER SYSTEM STOP DATABASE {db_name};"
            subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
            print(f"Tenant database '{db_name}' stopped successfully.")
            input("Press any key to continue...")
        except subprocess.CalledProcessError as ex:
            print(f"Error stopping tenant database: {ex.stderr}")
        except Exception as ex:
            print(f"Error stopping tenant database: {str(ex)}")
    else:
        print("Invalid input.  Tenant Database start aborted. Exiting function")

    clear_screen()
    check_installed_db(selected_userstore)

def create_tenant_db(selected_userstore):
    clear_screen()
    print("Creating Tenant Database")

    db_name = input("Enter the name for the new tenant database: ")
    db_user = input("Enter the database user: ")
    db_password = input("Enter the database password: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    try:
        sql_script = f"CREATE DATABASE {db_name} {db_user} USER PASSWORD {db_password};"
        subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
        print(f"Tenant database '{db_name}' created successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error creating tenant database: {ex.stderr}")
    except Exception as ex:
        print(f"Error creating tenant database: {str(ex)}")

def delete_tenant_database(selected_userstore):
    clear_screen()
    check_installed_db(selected_userstore)
    print("Creating Tenant Database")

    db_name = input("Enter the name for the new tenant database: ")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    try:
        sql_script = f"DROP DATABASE {db_name};"
        subprocess.run(command, input=sql_script, encoding='utf-8', check=True)
        print(f"Tenant database '{db_name}' deleted successfully.")
    except subprocess.CalledProcessError as ex:
        print(f"Error deleting tenant database: {ex.stderr}")
    except Exception as ex:
        print(f"Error deleting tenant database: {str(ex)}")

def show_db_parameters(selected_userstore):
    clear_screen()
    print("Start Tenant Database")

    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key, "-d", "SYSTEMDB"]

    try:
        sql_script = "SELECT DISTINCT FILE_NAME FROM M_INIFILE_CONTENTS WHERE FILE_NAME IS NOT NULL ORDER BY FILE_NAME;"
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = process.communicate(input=sql_script)
        print("Select a parameter to view:")

        # Parse the output and create a menu
        parameters = stdout.strip().split("\n")[6:-1]  # Skip the first 6 entries and the last entry
        menu = {}
        for index, parameter in enumerate(parameters, start=1):
            menu[index] = parameter
            print(f"{index}. {parameter}")

        # Ask user for selection
        print("Enter the number corresponding to your selection (or enter 'ALL' for all parameters):")
        user_input = input("> ")

        # Process user selection
        if user_input.lower() == 'all':
            selected_parameter = "ALL"
        elif user_input.isdigit() and int(user_input) in menu:
            selected_parameter = menu[int(user_input)]
            print(f"Selected parameter: {selected_parameter}")
        else:
            print("Invalid selection.")
            return

        # Execute the selected SQL script
        sql_script = "SELECT * FROM M_INIFILE_CONTENTS WHERE FILE_NAME IS NOT NULL;"
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = process.communicate(input=sql_script)
        output = stdout.strip()

        # Filter the output based on the selected parameter if 'ALL' is chosen
        if selected_parameter == "ALL":
            filtered_output = output
            count = output.count("\n") + 1  # Count the number of lines
        else:
            filtered_output = ""
            count = 0
            lines = output.splitlines()
            for line in lines:
                if selected_parameter in line:
                    filtered_output += line + "\n"
                    count += 1

        # Display the filtered output and count
        print("\nShowing database parameters:")
        print(filtered_output)
        print(f"\n{selected_parameter} count: {count}")

    except subprocess.CalledProcessError as ex:
        print(f"Error showing database parameters: {ex.stderr}")
    except Exception as ex:
        print(f"Error showing database parameters: {str(ex)}")

def future_use(selected_userstore):
    clear_screen()
    # Logic to configure future use
    print("Configuring Future Use")

if __name__ == '__main__':
    handle_database_administration_menu(None)
