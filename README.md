# tinyhanatools v 1.06
### www.sabtec.co
### GNU Rights distributed by: Schoeman and Brink, LLC
### Developed by: Tinus Brink AKA: "Tiny"

The below tool is created for HANA2 SPS05.  We will soon start working on SPS07.  This file explains how to download the files and build a single executable that can be run from the sidadm user.  

Currently build and tested for SUSE Linux Enterprise Server 15 SP4 (SLES15.4).  

If you have no interest to work on the python code and you only want to use the tool, then you can download the tinyhanatools file from the above repository, chmod +x the file and chown for sidadm:sapsys user and copy it to your /usr/sap/SID/HDB??/exe directory to run it from anywhere witht he sidadm user.  You can also download only the one executable file with the following command below and running it from the directory you would like to execute it from.  You might have to rename the file afterwards.  If the file has the correct permissions and it is located in the exe directory of the hana system, it should run by just typing tinyhanatools.  A rename might be required as wget might add .1 at the end of the file.  You can use mv filename newfilename for the rename.

```sh
wget https://raw.githubusercontent.com/tinytoolman/tinyhanatools/main/tinyhanatools
```

## Install git on your HANA SLES DEV or SANDBOX host:

### Git Option A: Install git

```sh
sudo zypper install git
```

If you get "No matching items found." Then you probably do not have a registered SLES system and no repositories assigned.
You can either get one by registering your system or you could use opensuse repository for git explained in Git Option B

```sh
sudo zypper install git
git --version
```

### Git Option B: Install git (No repository)

#### Please note this option uses a OpenSUSE repository which is free.  Only install on DEV/TEST or SANDBOX systems for testing purposes.  It is always best to have the paid for repositories for SLES on a SLES system.  Contact SUSE supoprt for the correct repository for your SLES version.

```sh
sudo zypper addrepo http://download.opensuse.org/distribution/leap/15.4/repo/oss/ SLES-SDK
```

Then run zypper refresh to refresh the repository.

```sh
sudo zypper refresh
```

You can select a to always trust the repository.

Then run teh zypper install git command to use git and then run the --version to check the version of git installed.

```sh
sudo zypper install git
git --version
```

## Use PyInstaller for Single Executable

To use pyinstaller to make a single executable file for the program, recommended.  Then you should first test if you can use pyinstaller on your system.

```sh
sudo pyinstaller
```

##### Note:  If you get "pyinstaller: command not found", then goto option: Install pyinstaller Option A:

### Install pyinstaller Option A:

```sh
sudo zypper install pyinstaller
```

If you get "'pyinstaller' not found in package names." Then you should add a repository for python with: Install pyinstaller Option B: (No repository)

### Install pyinstaller Option B: (No repository)
#### Please note this option uses a OpenSUSE repository which is free.  Only install on DEV/TEST or SANDBOX systems for testing purposes.  It is always best to have the paid for repositories for SLES on a SLES system.  Contact SUSE supoprt for the correct repository for your SLES version.

```sh
sudo zypper addrepo https://download.opensuse.org/repositories/devel:languages:python/15.5/devel:languages:python.repo
```

Then run zypper refresh

```sh
sudo zypper refresh
```

You can select a for trust always.

Now we can install pyinstaller on the system with the following command.

```sh
sudo zypper install python3-PyInstaller
```

You can select y to continue.

Check the version of pyinstaller.

```sh
pyinstaller --version
```

## Download files from Github Repository

To download the files from the github repository, you can use the following command.  I did it to the root diretory. If you do it other directories then it is fine, just be sure to also make adjustments to later scripts like creating the executable file with pyinstaller, as they currently point to the tinyhanatools directory created from root /.

```sh
git clone https://github.com/tinytoolman/tinyhanatools.git
```

This command would have created the directory tinyhanatools on your host.  Change to this directory.

```sh
cd tinyhanatools
```

You can now either create an executable manually with option A, or you can use the cript method below with option B.

### Option A: Create HANA Tools manually.

You can now use pyinstaller to make one file for running program as <sid>adm.  Please give correct permissions for <sid>adm to run program.

```sh
sudo pyinstaller --onefile --hidden-import=hdbcli A0_tinyhanatools.py
```

This would create file called:  A0_tinyhanatools.  Feel free to rename to tinyhanatools if you like and copy to /usr/sap/<sid>/HDB##/exe directory.
If you do this step, please change <sid> to your system ID for your HANA host and change ## to the instance number.

```sh
cp -p /tinyhanatools/dist/A0_tinyhanatools /usr/sap/SID/HDB??/exe/tinyhanatools
```

Change the ownership of the file:

```sh
sudo chown <sid>adm:sapsys tinyhanatools
```

Give the file permission to be executed (run).

```sh
chmod +x tinyhanatools
```

### Option B: Create HANA Tools script for easy use.

I created this file in the /tinyhanatools/ directory everytime I update the program I run it:

```sh
vi 1_create_hanatools.sh
```

Contents: (Please also chmod +x 1_create_hanatools.sh before you run it, recommended as superuser)

```sh
rm -r __pycache__/ build/ dist A0_tinyhanatools.spec
sleep 1
pyinstaller --onefile --hidden-import=hdbcli A0_tinyhanatools.py
sleep 1
#PLEASE CHANGE SID BELOW!!!
chown sidadm:sapsys /tinyhanatools/dist/A0_tinyhanatools
sleep 1
chmod +x /tinyhanatools/dist/A0_tinyhanatools
sleep 1
chown sidadm:sapsys /tinyhanatools/dist/A0_tinyhanatools
sleep 1
#PLEASE CHANGE SID AND INSTANCE NUMBER BELOW!!!
cp -p /tinyhanatools/dist/A0_tinyhanatools /usr/sap/SID/HDB??/exe/tinyhanatools
```

To run the file please chmod +x 1_create_hanatools.sh first

```sh
chmod +x 1_create_hanatools.sh
```

Then you could run it with:

```sh
./1_create_hanatools.sh
```

If you have pyinstaller already installed and the files from the git repository in the directory, then it should work.
Just remember to change the sid to your sid and the instance number to yours as well.

The executable tinyhanatools can be run from the sidadm user because it is copied to a PATH env variable namely the exe directory.
