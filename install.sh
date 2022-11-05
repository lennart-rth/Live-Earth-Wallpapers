#!/bin/bash

#install Python venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

#find display Name
VAR=$(env | grep -i display)
DISPLAY=${VAR##*=}
#get local path variables
HOMEPATH=$(dirname -- "$( readlink -f -- "$0"; )")
ENVPATH="$HOMEPATH/venv/bin/python3"
SCRIPTPATH="$HOMEPATH/changeBackground.py"

#get the provided flags
FLAGS=""
for parameter in "$@" 
do
    FLAGS="$FLAGS $parameter"
done

# echo $DISPLAY
# echo $HOMEPATH
# echo $ENVPATH
# echo $SCRIPTPATH
# echo $FLAGS
 
#set the cronjob
crontab -l > mycron
echo "*/30 * * * * DISPLAY=${DISPLAY} ${ENVPATH} ${SCRIPTPATH} ${FLAGS}" >> mycron
crontab mycron
rm mycron