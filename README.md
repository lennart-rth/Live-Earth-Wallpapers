# Meteosat-Background
Set near-realtime satellite images of the earth full disk natural color enhanced as your background.
1. Requires Python3
2. Set a Cronjob to execute `changeBackground.sh` every hour. This updates the eumesat.jpg image in the project folder.
3. There are 3 Methods to update the background image for your desktop:
    * Use `gsettings set org.gnome.desktop.background picture-uri file:/path/to/image`\
    `gsettings set org.gnome.desktop.background picture-options 'scaled'`
    * Use `feh --bg-max /path/to/image`
    * Use `nitrogen /path/to/image`
4. You can set the Ubuntu Loginscreen with https://github.com/PRATAP-KUMAR/ubuntu-gdm-set-background.
5. More satellite images can be found here: https://eumetview.eumetsat.int/static-images/latestImages.html 

![Image](eumesat.jpg?raw=true "Eumesat Live image")

![Image](nasa_pic.jpg?raw=true "Nasa Pic of the day")


