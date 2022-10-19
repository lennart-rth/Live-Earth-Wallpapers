#!/bin/bash

codename=$(cat /etc/os-release | grep UBUNTU_CODENAME | cut -d = -f 2)
osname=$(cat /etc/os-release | grep '="Ubuntu"' | cut -d = -f 2)

if [ "$codename" == "focal" ] || [ "$codename" == "hirsute" ] && [ "$osname" == '"Ubuntu"' ]
then
source="/usr/share/gnome-shell/theme/Yaru/gnome-shell-theme.gresource"
GDM_RESOURCE_CONFIG_NAME="gdm3"

elif [ "$codename" == "impish" ] && [ "$osname" == '"Ubuntu"' ]
then
source="/usr/share/gnome-shell/theme/Yaru/gnome-shell-theme.gresource"
GDM_RESOURCE_CONFIG_NAME="gdm"

else
echo "
------------------------------------------------------------------
Sorry, Script is only for Ubuntu 20.04, Ubuntu 21.04 & 21.10 Only
Exiting...
------------------------------------------------------------------"
exit 1
fi

pkg=$(dpkg -l | grep libglib2.0-dev-bin >/dev/null && echo "yes" || echo "no")
if [ "$pkg" == "no" ]
then
echo "
-----------------------------------------------------------------------------------------------------
Sorry, the package 'libglib2.0-dev-bin' is not installed. Install the package and then run this Script.
For now, Exiting...
-----------------------------------------------------------------------------------------------------"
exit 1
fi

dest="/usr/local/share/gnome-shell/custom-gdm"
color='#456789'

###################################################
HELP() {

echo "
ubuntu-gdm-set-background script (for changing Ubuntu 20.04, 21.04 & 21.10 GDM Background) HELP

there are four options
1. background with image
2. background with color
3. background with gradient horizontal ( requires two valid hex color inputs)
4. background with gradient vertical ( requires two valid hex color inputs)

tip: be ready with valid hex color code in place of below example like #aAbBcC or #dDeEfF. Change them to your preffered hex color codes.
you may choose colors from https://www.color-hex.com/

Example Commands:

1. sudo ./ubuntu-gdm-set-background --image /home/user/backgrounds/image.jpg
2. sudo ./ubuntu-gdm-set-background --color \#aAbBcC
3. sudo ./ubuntu-gdm-set-background --gradient horizontal \#aAbBcC \#dDeEfF
4. sudo ./ubuntu-gdm-set-background --gradient vertical \#aAbBcC \#dDeEfF
5. sudo ./ubuntu-gdm-set-background --reset
6. ./ubuntu-gdm-set-background --help

RESCUE_MODE, Example Commands:

1. sudo ./ubuntu-gdm-set-background --image /home/user/backgrounds/image.jpg rescue
2. sudo ./ubuntu-gdm-set-background --color \#aAbBcC rescue
3. sudo ./ubuntu-gdm-set-background --gradient horizontal \#aAbBcC \#dDeEfF rescue
4. sudo ./ubuntu-gdm-set-background --gradient vertical \#aAbBcC \#dDeEfF rescue

Why RESCUE_MODE?
It is when you try to change the background with some other scripts and then interacted with this script,
there will be some conflicts. In case you ran other scripts to change the background and then tried this script,
found conflicts? then add 'rescue' to the end of the command as mentiond above.

Please note that for 'RESCUE_MODE' active internet connection is necessary
"

}
###################################################

###################################################
ROUTINE_CHECK() {
if [ "$UID" != "0" ]
then
echo "This Script must be run with sudo"
exit 1
fi

cd /tmp
if [ -d /tmp/theme/ ]
then rm -r /tmp/theme
fi

if ! [ -d $dest ]
then
install -d $dest
fi

}
###################################################

###################################################
RESCUE_MODE() {
echo "
>>>>> Trying to Reinstall the package yaru-theme-gnome-shell,
if the reinstallation of the package is succesful, background change will be done
otherwise No changes will be made <<<<<<<<<
"
apt install --reinstall yaru-theme-gnome-shell
if [ $? != 0 ]
then
echo "
SCRIPT COULD NOT FINISH THE JOB, FAILURE, NO CHANGES WERE DONE".
exit 1
fi
}
###################################################

###################################################
EXTRACT() {
for r in $(gresource list $source); do
    t="${r/#\/org\/gnome\/shell\/}"
    mkdir -p $(dirname $t)
    gresource extract $source $r >$t
done
}
###################################################

###################################################
CREATE_XML() {
extractedFiles=$(find "theme" -type f -printf "%P\n" | xargs -i echo "    <file>{}</file>")
cat <<EOF >"theme/custom-gdm-background.gresource.xml"
<?xml version="1.0" encoding="UTF-8"?>
<gresources>
  <gresource prefix="/org/gnome/shell/theme">
$extractedFiles
  </gresource>
</gresources>
EOF
}
###################################################

###################################################
SET_GRESOURCE() {
cd $dest
update-alternatives --quiet --install /usr/share/gnome-shell/$GDM_RESOURCE_CONFIG_NAME-theme.gresource $GDM_RESOURCE_CONFIG_NAME-theme.gresource $dest/custom-gdm-background.gresource 0
update-alternatives --quiet --set $GDM_RESOURCE_CONFIG_NAME-theme.gresource $dest/custom-gdm-background.gresource

check=$(update-alternatives --query $GDM_RESOURCE_CONFIG_NAME-theme.gresource | grep Value | grep $dest/custom-gdm-background.gresource >/dev/null && echo "pass" || echo "fail")
if [ "$check" == "pass" ]
then
echo "
seems 'background change is successful'
Changes will be effective after a Reboot (CTRL+ALT+F1 may show the changes immediately)
If something wrong, logon to tty and run the below command
sudo update-alternatives --quiet --set $GDM_RESOURCE_CONFIG_NAME-theme.gresource /usr/share/gnome-shell/theme/Yaru/gnome-shell-theme.gresource
"
else
echo Failure
exit 1
fi
}
###################################################

############################################################################################
case "$1" in ###############################################################################
############################################################################################
--help) ####################################################################################
############################################################################################
HELP
exit 1
;;
############################################################################################
--reset) ###################################################################################
############################################################################################

if ! [ -f $dest/custom-gdm-background.gresource ]
then
echo "
-----------------------------------------------------------------------------
No need, Already Reset. (or unlikely background is not set using this Script.)
-----------------------------------------------------------------------------"
exit 1
elif [ "$UID" != "0" ]
then
echo "This Script must be run with sudo"
exit 1
else
rm $dest/custom-gdm-background.gresource
update-alternatives --quiet --set $GDM_RESOURCE_CONFIG_NAME-theme.gresource "$source"
cd /usr/local/share
rmdir --ignore-fail-on-non-empty -p gnome-shell/custom-gdm
echo "
				     		---------------
						|Reset Success|
						---------------
				Changes will be effective after a Reboot"
exit 1
fi
;;
############################################################################################
--image) ###################################################################################
############################################################################################

if [ -z "$2" ]
then
echo "Image path is not provided"
exit 1
fi

if
file "$2" | grep -qE 'image|bitmap'
then

ROUTINE_CHECK

if [ "$3" == "rescue" ]
then
RESCUE_MODE
fi

EXTRACT
cd theme
cp "$2" ./gdm-background
mv $GDM_RESOURCE_CONFIG_NAME.css original.css
echo '@import url("resource:///org/gnome/shell/theme/original.css");
#lockDialogGroup {
background: '$color' url("resource:///org/gnome/shell/theme/gdm-background");
background-repeat: no-repeat;
background-size: cover;
background-position: center; }' > $GDM_RESOURCE_CONFIG_NAME.css
cd /tmp
CREATE_XML
cd theme
glib-compile-resources custom-gdm-background.gresource.xml
mv custom-gdm-background.gresource $dest

SET_GRESOURCE

exit 1

else
echo "
absolute path to image is neither provided nor it is valid.
see help with below command
./ubuntu-gdm-set-background --help"
exit 1
fi
;;
############################################################################################
--color) ###################################################################################
############################################################################################

if [ -z "$2" ]
then
echo "color is not provided"
exit 1
fi

if ! [[ $2 =~ ^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$ ]]
then
echo "provided color is not a valid 'HEX Color Code'
see help with below command
./ubuntu-gdm-set-background --help"
exit 1
fi

ROUTINE_CHECK

if [ "$3" == 'rescue' ]
then
RESCUE_MODE
fi

EXTRACT

cd theme
mv $GDM_RESOURCE_CONFIG_NAME.css original.css
echo '@import url("resource:///org/gnome/shell/theme/original.css");
#lockDialogGroup {
background-color: '$2'; }' > $GDM_RESOURCE_CONFIG_NAME.css
cd /tmp
CREATE_XML
cd theme
glib-compile-resources custom-gdm-background.gresource.xml
mv custom-gdm-background.gresource $dest

SET_GRESOURCE

exit 1
;;
############################################################################################
--gradient) ################################################################################
############################################################################################

if [ "$2" == "horizontal" ] || [ "$2" == "vertical" ]
then
direction=$2
else
echo "gradient direction is not provided"
exit 1
fi

if [[ -z "$3" || -z "$4" ]]
then
echo "color/colors is/are not provided"
exit 1
fi

if ! [[ $3 =~ ^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$ ]] || ! [[ $4 =~ ^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$ ]]
then
echo "provided color/colors is/are not a valid 'HEX Color Code'
see help with below command
./ubuntu-gdm-set-background --help"
exit 1
fi	

ROUTINE_CHECK

if [ "$5" == "rescue" ]
then
RESCUE_MODE
fi

EXTRACT
cd theme
mv $GDM_RESOURCE_CONFIG_NAME.css original.css
echo '@import url("resource:///org/gnome/shell/theme/original.css");
#lockDialogGroup {
background-gradient-direction: '$direction';
background-gradient-start: '$3';
background-gradient-end: '$4'; }' > $GDM_RESOURCE_CONFIG_NAME.css
cd /tmp
CREATE_XML
cd theme
glib-compile-resources custom-gdm-background.gresource.xml
mv custom-gdm-background.gresource $dest

SET_GRESOURCE

exit 1
;;
############################################################################################
*) #########################################################################################
############################################################################################
echo " use the options --image | --color | --gradient | --help | --reset"
exit 1
;;
############################################################################################
esac

exit
