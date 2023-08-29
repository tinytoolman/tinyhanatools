rm -r __pycache__/ build/ dist A0_tinyhanatools.spec
sleep 1
pyinstaller --onefile A0_tinyhanatools.py
sleep 1
#PLEASE CHANGE SID BELOW!!!
chown hadadm:sapsys /tinyhanatools/dist/A0_tinyhanatools
sleep 1
chmod +x /tinyhanatools/dist/A0_tinyhanatools
sleep 1
chown hadadm:sapsys /tinyhanatools/dist/A0_tinyhanatools
sleep 1
#PLEASE CHANGE SID AND INSTANCE NUMBER BELOW!!!
cp -p /tinyhanatools/dist/A0_tinyhanatools /usr/sap/HAD/HDB00/exe/tinyhanatools
#local copy
cp -p /tinyhanatools/dist/A0_tinyhanatools /tinyhanatools/tinyhanatools
