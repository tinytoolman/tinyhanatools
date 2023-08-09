'''sh
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
