#!/bin/sh

#PART1#####################
pyinstaller --noconfirm app.spec
#PART2#####################
# Create folders.
[ -e package ] && rm -r package

chmod 755 app.py
chmod 755 cli
chmod 755 cli_code.py

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

chmod -R 777 package/opt/liewa/liewa/liewa_cli/recources/
chmod 777 package/opt/liewa/liewa/liewa.service
chmod 777 package/opt/liewa/liewa/liewa.timer
chmod 777 package/opt/liewa/app
chmod 777 package/opt/liewa/app.py
chmod 777 package/opt/liewa/cli
chmod 777 package/opt/liewa/cli_code.py

chmod +x package/opt/liewa/app

#PART3#####################
rm liewa.deb
fpm -C package -s dir -t deb -n "liewa" -v 0.1.0 -p liewa.deb
#PART4#####################
sudo dpkg -i liewa.deb 