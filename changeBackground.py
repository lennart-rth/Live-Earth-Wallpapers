#!/usr/bin/env python3
import datetime
import os
from PIL import Image
import argparse
import sys
import requests
from io import BytesIO
import time
import urllib.request, json

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zoomLevel", type=int, choices=[0, 1, 2, 3, 4], default=3,
                            help="Change the ImageSize 0=678, 1=1356, 2=2712, 3=5424, 4=10848 (Meteosat does not support Level 4)")
    parser.add_argument("-s", "--source", type=str, choices=["goes-16","goes-17","goes-18","himawari","meteosat-9","meteosat-11"], default="meteosat-9",
                            help="Select Satellite as a source. goes-16, goes-17, goes-18, himawari, meteosat-9 or meteosat-11")
    parser.add_argument("-p", "--bgProgram", type=str, choices=["feh","nitrogen","gsettings"],
                            help="Select Programm to set the Background.")

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    return args

satelliteData = {
        #(minute,second,MaxZoomLevel)
        "goes-16":(10,20,4),
        "goes-17":(10,31,4),
        "goes-18":(10,20,4),
        "himawari":(10,0,4),
        "meteosat-9":(15,0,3),
        "meteosat-11":(15,0,3)}

def getTimeCode(sat):
    url = f"https://rammb-slider.cira.colostate.edu/data/json/{sat}/full_disk/natural_color/latest_times.json"
    f = urllib.request.urlopen(url)
    data = json.load(f)
    latest = data["timestamps_int"][0]
    return latest

def getPictureTime(satellite):
    now = datetime.datetime.now(datetime.timezone.utc)
    minute = now.minute-(now.minute%satelliteData[satellite][0])
    second = satelliteData[satellite][1]

    lastSatImage = datetime.datetime(now.year,now.month,now.day,now.hour,minute,second)
    if now.hour <= 1:
        lastSatImage = (lastSatImage - datetime.timedelta(days=1,hours=1,minutes=30))
    else:
        lastSatImage = (lastSatImage - datetime.timedelta(hours=1,minutes=30))

    return lastSatImage.strftime("%Y/%m/%d")

def calcTileCoordinates(zoomLevel):
    #zoomlevel 0-3 or 0-4 (depending on the satellite)
    t_n = 2**zoomLevel
    row = range(0,t_n)
    col = range(0,t_n)
    return list(row), list(col)

def download(url):
    for i in range(3):
        try:
            with requests.get(url) as response:
                return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"{i}/3 Could not download Image '{url}'...")
            time.sleep(1)

def buildUrl(args):
    if (args.source == "meteosat-9" or args.source == "meteorsat-10") and args.zoomLevel > 4:
        sys.exit("Meteosat does not support Zoom Levels greater than 4.")

    date = getPictureTime(args.source)
    timeCode = getTimeCode(args.source)
    
    base_url = f"https://rammb-slider.cira.colostate.edu/data/imagery/{date}/{args.source}---full_disk/natural_color/{timeCode}/0{args.zoomLevel}"
    return base_url

def getImage(args,base_url):
    row, col = calcTileCoordinates(args.zoomLevel)
    bg = Image.new('RGB', (0,0))
    for r in row:
        for c in col:
            url = base_url + f"/{str(r).zfill(3)}_{str(c).zfill(3)}.png"
            print(f"Downloading Image ({r},{c}).{url}")
            img = download(url)

            new_bg = Image.new('RGB', (img.width*(max(col)+1), img.height*(max(row)+1)))
            new_bg.paste(bg, (0, 0))
            new_bg.paste(img, (img.width*(c), (r)*img.height))

            bg = new_bg
    #zoom out a bit
    wallpaper = Image.new('RGB', (int(bg.width*1.2),int(bg.height*1.2)))
    wallpaper.paste(bg, (int(0+(bg.width*0.1)), int(0+(bg.height*0.1))))
    return wallpaper

def setBG(p, filename):
    if p == "feh":
        os.system(f"feh --bg-max {filename}")
    elif p == "notrogen":
        os.system(f"nitrogen {filename}")
    elif p == "gsettings":
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file:{filename}")
        os.system("gsettings set org.gnome.desktop.background picture-options 'scaled'")
    
    #set the Lock screen
    #os.system(f"sudo ./ubuntu-gdm-set-background --image {filename}")


if __name__ == "__main__":
    args = parseArgs()
    base_url = buildUrl(args)
    bg = getImage(args,base_url)
    logDate = datetime.datetime.now(datetime.timezone.utc).strftime("%d_%m_%Y_%H_%M")
    filename = f"{os.path.dirname(os.path.realpath(__file__))}/backgroundImage.png"
    bg.save(filename)
    print(f"Image saved to: {filename}")
    setBG(args.bgProgram,filename)

    