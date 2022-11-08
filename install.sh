#!/bin/bash

#install Python venv
echo "Installing python dependecies..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
echo "successfull"

#find display Name
VAR=$(env | grep -i display)
DISPLAY=${VAR##*=}
#get local path variables
HOMEPATH=$(dirname -- "$( readlink -f -- "$0"; )")
ENVPATH="$HOMEPATH/venv/bin/python3"
SCRIPTPATH="$HOMEPATH/changeBackground.py"
IMAGEFILE="$HOMEPATH/backgroundImage.png"

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

setup_cronjob () {
    #set the cronjob
    crontab -l > mycron
    echo "*/30 * * * * DISPLAY=${DISPLAY} ${ENVPATH} ${SCRIPTPATH} -dir ${HOMEPATH} ${FLAGS}" >> mycron
    crontab mycron
    echo "Writing Cronjobs:"
    cat mycron
    rm mycron
    echo "successfull!"
}

setup_taskscheduler () {
    echo "Writing Task-Scheduler..."
    SCHTASKS /CREATE /SC DAILY /TN "FOLDERPATH\TASKNAME" /TR "C:\SOURCE\FOLDER\APP-OR-SCRIPT" /ST HH:MMExampleSCHTASKS /CREATE /SC DAILY /TN "MyTasks\Live-Earth_Wallpapers" /TR  /ST 11:00
    echo "successfull!"
}

write_appleScript_file () {
  echo "#!/bin/bash
osascript -e 'tell application \"System Events\" to tell every desktop to set picture to \"$IMAGEFILE\"'
" > apple_set_bg.sh
}

# Detect the platform
OS="`uname`"
case $OS in
  'Linux')
    OS='Linux'
    setup_cronjob
    ;;
  'WindowsNT')
    OS='Windows'
    setup_taskscheduler
    ;;
  'Darwin') 
    OS='Mac'
    setup_cronjob
    write_appleScript_file
    ;;
  *) 
    setup_cronjob
    ;;
esac

echo "Detected $OS as your Operating System!"

