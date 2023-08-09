rm -r pycache/ build/ dist A0_tinyhanatools.spec

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

cp -p /software/tinyhanatools/dist/A0_tinyhanatools /usr/sap//HDB##/exe/tinyhanatools

