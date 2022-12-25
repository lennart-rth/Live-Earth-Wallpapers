#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p "dist/dmg"
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/app.app" "dist/dmg"
# If the DMG already exists, delete it.
test -f "dist/liewa.dmg" && rm "dist/liewa.dmg"
create-dmg \
  --volname "Liewa" \
  --volicon "icon.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon 'icon.ico' \
  --hide-extension "app.app" \
  --app-drop-link 425 120 \
  "dist/Liewa.dmg" \
  "dist/dmg/"