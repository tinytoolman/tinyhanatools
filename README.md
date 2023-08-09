# tinyhanatools v 1.06
### www.sabtec.co
### Schoeman and Brink, LLC
### Tinus Brink AKA: "Tiny"

Currently build and tested for SUSE Linux Enterprise Server 15 SP4 (SLES15.4)
Install git on your HANA SLES DEV or SANDBOX host:

**sudo zypper install git**

You can use pyinstaller to make one file for running program as <sid>adm.  Please give correct permissions for <sid>adm to run program.

**pyinstaller --onefile --hidden-import=hdbcli A0_tinyhanatools.py**

This would create file called:  A0_tinyhanatools.  Feel free to rename to tinyhanatools if you like and copy to /usr/sap/<sid>/HDB##/exe directory.
If you do this step, please change <sid> to your system ID for your HANA host and change ## to the instance number.

**cp -p /tinyhanatools/dist/A0_tinyhanatools /usr/sap/<sid>/HDB##/exe/tinyhanatools**

Change the ownership of the file:

**sudo chown <sid>adm:sapsys tinyhanatools**

Give the file permission to be executed (run).

**chmod +x tinyhanatools**

I created this file in the /tinyhanatools/ directory everytime I update the program I run it:

**vi 1_create_hanatools.sh**

Contents: (Please also chmod +x 1_create_hanatools.sh before you run it, recommended as superuser)

rm -r __pycache__/ build/ dist A0_tinyhanatools.spec

sleep 1

pyinstaller --onefile --hidden-import=hdbcli A0_tinyhanatools.py

sleep 1

#PLEASE CHANGE SID BELOW!!!

chown hadadm:sapsys /tinyhanatools/dist/A0_tinyhanatools

sleep 1

chmod +x /software/tinyhanatools/dist/A0_tinyhanatools

sleep 1

chown hadadm:sapsys /tinyhanatools/dist/A0_tinyhanatools

sleep 1

#PLEASE CHANGE SID AND INSTANCE NUMBER BELOW!!!

cp -p /software/tinyhanatools/dist/A0_tinyhanatools /usr/sap/<sid>/HDB##/exe/tinyhanatools
