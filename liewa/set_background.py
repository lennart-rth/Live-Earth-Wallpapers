#take an image as input
#get Os type and set background

def set_background(p, filename):
    if p == "feh":
        os.system(f"feh --bg-max {filename}")

    elif p == "nitrogen":
        os.system(f"nitrogen {filename}")

    elif p == "gsettings":
        os.system(
            f"gsettings set org.gnome.desktop.background picture-uri file:{filename}"
        )
        os.system("gsettings set org.gnome.desktop.background picture-options 'scaled'")

    elif p == "windows":
        os.system(
            'reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d  wallpaper_path /f'
        )
        os.system("RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameter")

    elif p == "osascript":
        os.system(f"/bin/bash apple_set_bg.sh")

    elif p == "apple_defaults":
        os.system(
            '''defaults write com.apple.desktop Background '{defaults = {ImageFilePath = "'''
            + str(filename)
            + """"; };}';"""
        )

    # set the Ubuntu lock screen
    # os.system(f"sudo ./ubuntu-gdm-set-background --image {filename}")

