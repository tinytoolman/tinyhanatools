#-------------------------------------------------------------------------------
# Name:        a4_0_system_configuration.py
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

def handle_system_configuration_menu(selected_userstore):
    clear_screen()
    hostname = socket.gethostname()
    print_bold(f"System Configuration Menu - {hostname}")
    print_bold("-------------------")
    print("1.  N/A View HANA Log and Trace Files")
    print("2.  Future Use")
    print("3.  Future Use")
    print("4.  N/A System Monitoring and Alerts")
    print("5.  License and System Information")
    print("0.  Back")
    print("x.  Exit")
    print_bold("-------------------")

    text = "Enter your choice: "
    choice = input("\033[1m" + text + "\033[0m")
    if choice == '1':
        configure_system_landscape(selected_userstore)
    elif choice == '2':
        configure_ha_dr(selected_userstore)
    elif choice == '3':
        configure_system_parameters(selected_userstore)
    elif choice == '4':
        monitor_system(selected_userstore)
    elif choice == '5':
        view_license_system_info(selected_userstore)
    elif choice == '6':
        view_logs_traces(selected_userstore)
    elif choice == '0':
        return
    elif choice.lower() =='x':
        clear_screen()
        print("Tiny HANA Tools Exit...")
        os._exit(0)
    else:
        print("Invalid choice. Please try again.")

    # Wait for user input to return to the system configuration menu
    input("Press Enter to continue...")
    handle_system_configuration_menu(selected_userstore)

def configure_system_landscape(selected_userstore):
    clear_screen()
    print("We are still working on this")
    input("Press Enter to continue...")

def configure_ha_dr(selected_userstore):
    clear_screen()
    print(f"Configuring High Availability and Disaster Recovery with userstore {selected_userstore}")
    input("Press Enter to continue...")

def configure_system_parameters(selected_userstore):
    clear_screen()
    print(f"Configuring System Parameters and Settings with userstore {selected_userstore}")
    input("Press Enter to continue...")

def monitor_system(selected_userstore):
    clear_screen()
    print(f"Monitoring System with userstore {selected_userstore}")
    input("Press Enter to continue...")

def view_license_system_info(selected_userstore):
    clear_screen()
    print(f"Viewing License and System Information with userstore {selected_userstore}")

    # Execute the SQL query to retrieve license information
    key = selected_userstore.split()[1]
    command = ["hdbsql", "-U", key]
    sql_query = "SELECT * FROM M_LICENSE;"

    try:
        result = subprocess.run(command + [sql_query], encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            output = result.stdout.strip()
            license_info = [line.split(",") for line in output.splitlines()]
            headers = license_info[0]  # Assuming first line is the headers
            data = license_info[1:]  # Rest of the lines are data
            for row in data:
                for header, value in zip(headers, row):
                    print(f"{header.strip()}: {value.strip()}")
        else:
            print(f"Error executing command: {result.stderr}")
    except Exception as ex:
        print(f"Error executing command: {str(ex)}")

    input("Press Enter to continue...")

def view_logs_traces(selected_userstore):
    clear_screen()
    print("View HANA Log and Trace Files")

    # Get the SAPSYSTEMNAME and TINSTANCE env variables
    sapsystemname = os.environ.get('SAPSYSTEMNAME')
    print("SAPSYSTEMNAME obtained as: " + str(sapsystemname) + "\n")
    if sapsystemname is None:
        print("Error: SAPSYSTEMNAME environment variable not set.")
        return
    tinstance = os.environ.get('TINSTANCE')
    print("Instance number obtained as: " + str(tinstance) + "\n")
    if tinstance is None:
        print("Error: TINSTANCE environment variable not set.")
        return

    while True:
        print("Select an option:")
        print("1. Main Trace File (trace_<SID>.trc)")
        print("2. Name Server Trace File (nameserver_<SID>.trc)")
        print("3. Index Server Trace File (indexserver_<SID>.trc)")
        print("4. XS Engine Trace File (xsengine_<SID>.trc)")
        print("5. Name Server Log File (nameserver_trace_<SID>.log)")
        print("6. Index Server Log File (indexserver_trace_<SID>.log)")
        print("7. XS Engine Log File (xsengine_trace_<SID>.log)")
        print("8. OS /var/log/messages")
        print("9. OS /var/log/syslog")
        print("10. OS /var/log/secure")
        print("0. Back to System Configuration Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            tail_file(f"/usr/sap/{sapsystemname}/HDB{tinstance}/trace/trace_{sapsystemname}.trc", 1000)
        elif choice == '2':
            view_file(f"/usr/sap/{sapsystemname}/HDB{tinstance}/trace/nameserver_{sapsystemname}.trc")
        elif choice == '3':
            view_file(f"/usr/sap/{sapsystemname}/HDB{tinstance}/trace/indexserver_{sapsystemname}.trc")
        elif choice == '4':
            view_file(f"/usr/sap/{sapsystemname}/HDB{tinstance}/trace/xsengine_{sapsystemname}.trc")
        elif choice == '5':
            view_file(f"/usr/sap/{sapsystemname}/HDB{tinstance}/trace/nameserver_trace_{sapsystemname}.log")
        elif choice == '6':
            view_file(f"/usr/sap/{sapsystemname}/HDB{tinstance}/trace/indexserver_trace_{sapsystemname}.log")
        elif choice == '7':
            view_file(f"/usr/sap/{sapsystemname}/HDB{tinstance}/trace/xsengine_trace_{sapsystemname}.log")
        elif choice == '8':
            view_file("/var/log/messages")
        elif choice == '9':
            view_file("/var/log/syslog")
        elif choice == '10':
            view_file("/var/log/secure")
        elif choice == '0':
            return
        else:
            print("Invalid choice. Please try again.")

def tail_file(file_path, num_lines):
    command = ["tail", "-n", str(num_lines), file_path]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as ex:
        print(f"Error executing command: {ex.stderr}")
    except Exception as ex:
        print(f"Error executing command: {str(ex)}")

def view_file(file_path):
    command = ["cat", file_path]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as ex:
        print(f"Error executing command: {ex.stderr}")
    except Exception as ex:
        print(f"Error executing command: {str(ex)}")

if __name__ == '__main__':
    handle_system_configuration_menu()

