#!/bin/sh

#PART1#####################
pyinstaller --noconfirm app.spec
#PART2#####################
# Create folders.
[ -e package ] && rm -r package

chmod 755 app.py
chmod 755 cli.py

mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

# Copy files (change icon names, add lines for non-scaled icons)
cp -r dist/app package/opt/liewa
cp liewa/liewa_gui/icon.svg package/usr/share/icons/hicolor/scalable/apps/liewa.svg
cp liewa.desktop package/usr/share/applications

# Change permissions
find package/opt/liewa -type f -exec chmod 644 -- {} +
find package/opt/liewa -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +

chmod -R 777 package/opt/liewa/_internal/liewa/liewa_cli/recources/
# chmod 777 package/opt/liewa/_internal/liewa/liewa.service
# chmod 777 package/opt/liewa/_internal/liewa/liewa.timer
chmod 777 package/opt/liewa/_internal/liewa
chmod 777 package/opt/liewa/_internal/app.py
chmod 777 package/opt/liewa/_internal/cli.py

chmod +x package/opt/liewa/app

#PART3#####################
[ -f liewa.deb ] && rm liewa.deb

#The rest is done in the gitlab ci scipt
# fpm -C package -s dir -t deb -n "liewa" -v 0.1.0 -p liewa.deb
#PART4#####################
# sudo dpkg -i liewa.deb 
