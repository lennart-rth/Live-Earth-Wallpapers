import datetime
from PIL import Image
import sys
from utils import download
import urllib.request, json

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


def buildUrl(args):
    if (args.source == "meteosat-9" or args.source == "meteorsat-10") and args.zoomLevel > 4:
        sys.exit("Meteosat does not support Zoom Levels greater than 4.")

    date = getPictureTime(args.source)
    timeCode = getTimeCode(args.source) 

    name = args.colorMode
    if name == None:
        name = "natural_color"       #default color mode

    supportedArgs = ["geocolor","natural_color"]
    if name not in supportedArgs:
        raise ValueError("Wrong parameter for colorMode: Meteorsat and Goes only support 'natural_color' or 'geocolor' as colorMode!")

    base_url = f"https://rammb-slider.cira.colostate.edu/data/imagery/{date}/{args.source}---full_disk/{name}/{timeCode}/0{args.zoomLevel}"
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