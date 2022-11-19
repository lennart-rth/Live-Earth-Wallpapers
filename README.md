[![PyPI version](https://badge.fury.io/py/liewa.svg)](https://badge.fury.io/py/liewa)
![Linux](https://svgshare.com/i/Zhy.svg)
![macOS](https://svgshare.com/i/ZjP.svg)
![Windows](https://svgshare.com/i/ZhY.svg)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

# Live-Earth-Wallpapers aka liewa
Set your Desktop background to near realtime picures of the earth.
Supports all known **geostationary** satellites, high resolution **sentinel** images, Nasa **Solar Dynamics Observatory** Images and Nasa astronomy picture of the day (Apod)! For Linux, Windows and MacOs!

***
## Examples
<!-- ![alt text](examples/config1.png) -->
![](https://github.com/lennart-rth/Live-Earth-Wallpapers/blob/main/examples/config1.png)
*Example Output of the config1.yml file. Use this by passing config1 to -o flag.*
<!-- ![alt text](examples/config2.png) -->
![](https://github.com/lennart-rth/Live-Earth-Wallpapers/blob/main/examples/config2.png)
*Example Output of the config2.yml file. Use this by passing config2 to -o flag.*
<!-- ![alt text](examples/config3.png) -->
![](https://github.com/lennart-rth/Live-Earth-Wallpapers/blob/main/examples/config3.png)
*Example Output of the config3.yml file. Use this by passing config3 to -o flag.*
<!-- ![alt text](examples/caribic.png) -->
![](https://github.com/lennart-rth/Live-Earth-Wallpapers/blob/main/examples/caribic.png)
*Example Output of the Sentinel satellite. Learn how to generate custom images for your location at the [Wiki Page](https://github.com/lennart-rth/Live-Earth-Wallpapers/wiki)*
<!-- ![alt text](examples/arctic.png) -->
![](https://github.com/lennart-rth/Live-Earth-Wallpapers/blob/main/examples/arctic.png)
*Example Output of the Sentinel satellite. Learn how to generate custom images for your location at the [Wiki Page](https://github.com/lennart-rth/Live-Earth-Wallpapers/wiki)*
<!-- ![alt text](examples/desert.png) -->
![](https://github.com/lennart-rth/Live-Earth-Wallpapers/blob/main/examples/desert.png)
*Example Output of the Sentinel satellite. Learn how to generate custom images for your location at the [Wiki Page](https://github.com/lennart-rth/Live-Earth-Wallpapers/wiki)*
<!-- ![alt text](examples/apod-cover.png) -->
![](https://github.com/lennart-rth/Live-Earth-Wallpapers/blob/main/examples/apod-cover.png)
*Example Output for astronomy picture of the day feed (apod)(2022 November 15).*
### Build images to your needs by writing your own config.yml file.
### Read more on the [Wiki Page](https://github.com/lennart-rth/Live-Earth-Wallpapers/wiki).
### You can present your creations in the [Discussions Page](https://github.com/lennart-rth/Live-Earth-Wallpapers/discussions/) under "Show and tell"

***
## Installation
1. `pip install liewa`
2. Run the program routinely\
*Note: this is only temporary and will be replaced with automatic systemd installation.*
  * **For Linux, Mac:**
    * Run `execute `env | grep -i display` to find your exact DISPLAY name. (probably :0 or :0.0)` To find your Display Name.
    * Paste this into a file called `run_script.py`: 
    ```
    from liewa import __main__
    __main__.main()
    ```
    * Paste  `*/30 * * * * DISPLAY=:{your display name from 1.} python3 path/to/your/run_script.py` in your crontab file. You can open the file with `crontab -e`. This will execute the background change every 30 min.
    * Paste  `@reboot liewa` in your crontab file. You can open the file with `crontab -e`. This will execute execute the background change on startup.\
  * **For Windows:**
    * Set a Taks with Windows Task-Scheduler to execute a `run_script.bat` file (Set this as Programm `C:\\path\to\folder\run_script.bat`). Content of the File:
    ```
    @echo off
    START /wait /B liewa -c C:\\Users\ab\Desktop\config_mama.yml
    ```
3. customize the image composition by writing your own `config.yml` file or using the preinstalled. (See [Usage](#Usage))

**Make sure that the pip directory for packages is in the system Path Variable!**\
If not see tutorials for [Unix](https://linuxhint.com/add-path-permanently-linux/) or [Windows](https://www.computerhope.com/issues/ch000549.htm).\
*Test the installation with `liewa`. Your background should have changed.*

***
## Usage
### Script Parameters:
| short | long     | type   | default                              | help                                                                 |
|-------|----------|--------|--------------------------------------|----------------------------------------------------------------------|
| -c    | --config | String | path/to/project/recources/config.yml | The absolute path to the config File. There are 3 examples preinstalled. Use them by passing `congfig1`, `config2` or `config3` as parameters.|
| -o    | --output | String | -                                    | The absolute path to a folder. All loaded Images will be saved here. |\

The composition of your background image is defined by a config.yml file.\
Read the [Wiki](https://github.com/lennart-rth/Live-Earth-Wallpapers/wiki) for a detailed instruction on how to personalize your Image composition.

***
## For Contributers
1. Read the [Contributing](CONTRIBUTING.md) Readme.
2. Filter Discussions by "For Contributers" Label to find topics to work on.
3. Feel free to add your own ideas, features or open a Discussion in the Discussions tab.
