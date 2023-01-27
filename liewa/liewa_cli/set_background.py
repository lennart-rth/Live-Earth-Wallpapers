import platform
import subprocess
from PIL import Image
import os

def check_for_program(program):
    try:
        subprocess.check_output(["which", "--", program])
        return True
    except:
        return False

def set_background(file_name):
    system = platform.system()
    
    if system == "Windows":
        # try:
        #     import win32api
        #     import win32con
        #     import win32gui
        #     bmp_image = Image.open(file_name)
        #     bmp_img_path = file_name.split(".")[0:-2] + ".bmp"
        #     bmp_image.save(bmp_img_path, "BMP")
        #     key = win32api.RegOpenKeyEx(
        #         win32con.HKEY_CURRENT_USER,
        #         "Control Panel\\Desktop",
        #         0,
        #         win32con.KEY_SET_VALUE,
        #     )
        #     win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
        #     win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
        #     win32gui.SystemParametersInfo(
        #         win32con.SPI_SETDESKWALLPAPER, bmp_img_path, 1 + 2
        #     )
        #     os.remove(bmp_img_path)
        # except:
            try:
                import ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file_name, 0)
            except:
                raise ValueError("Could not set the Wallpaper.")
    elif system == "Darwin":
        # subprocess.call(
        #     [
        #         "osascript",
        #         "-e",
        #         'tell application "System Events"\n',
        #         "-e",
        #         "set theDesktops to a reference to every desktop\n",
        #         "-e",
        #         "repeat with aDesktop in theDesktops\n",
        #         "-e",
        #         'set the picture of aDesktop to "' + file_name + '"\n',
        #         "-e",
        #         'end repeat\n',
        #         "-e",
        #         'end tell',
        #     ]
        # )
        subprocess.call(
            [
                'osascript',
                '-e',
                'tell application "System Events"\n',
                '-e',
                '\tset desktopCount to count of desktops\n',
                '-e',
                '\trepeat with desktopNumber from 1 to desktopCount\n',
                '-e',
                '\t\ttell desktop desktopNumber\n',
                '-e',
                '\t\t\tset picture to "'+file_name+'"\n',
                '-e',
                '\t\tend tell\n',
                '-e',
                '\tend repeat\n',
                '-e',
                'end tell'
            ]
        ,timeout=10)
        os.system('killall Dock')
    elif system == "Linux":
        try:
            if check_for_program("feh"):
                subprocess.call(["feh", "--bg-fill", file_name],timeout=10)
            if check_for_program("nitrogen"):
                subprocess.call(["nitrogen", file_name],timeout=10)
            subprocess.call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", file_name],timeout=50) 
            subprocess.call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", file_name],timeout=50) 
            subprocess.call(["gsettings", "set", "org.gnome.desktop.background", "picture-options", "scaled"],timeout=50)
            subprocess.call(["gsettings", "set", "org.gnome.desktop.background", "primary-color", "#000000"],timeout=50)
        except: None  

    elif check_for_program("feh"):
        subprocess.call(["feh", "--bg-fill", file_name],timeout=10)
    elif check_for_program("nitrogen"):
        subprocess.call(["nitrogen", file_name],timeout=10)

    # # set the Ubuntu lock screen
    # # os.system(f"sudo ./ubuntu-gdm-set-background --image {filename}")

