import math
import datetime
from utils import download
import os
from PIL import Image
import cv2
import numpy as np

from datetime import date
import astral
from astral.sun import sun

def boundingBox(latitudeInDegrees, longitudeInDegrees, widthInKm, heightInKm):
    widthInM = widthInKm*1000
    heightInM = heightInKm*1000
    southLat = PointLatLng(latitudeInDegrees,longitudeInDegrees,heightInM,180)[0]
    northLat = PointLatLng(latitudeInDegrees,longitudeInDegrees,heightInM,0)[0]
    westLon = PointLatLng(latitudeInDegrees,longitudeInDegrees,widthInM,270)[1]
    eastLon = PointLatLng(latitudeInDegrees,longitudeInDegrees,widthInM,90)[1]
    return f"{southLat},{westLon},{northLat},{eastLon}" 

def PointLatLng(Lat,Lng, distance, bearing):
    rad = bearing * math.pi / 180
    lat1 = Lat * math.pi / 180
    lng1 = Lng * math.pi / 180
    lat = math.asin(math.sin(lat1) * math.cos(distance / 6378137) + math.cos(lat1) * math.sin(distance / 6378137) * math.cos(rad))
    lng = lng1 + math.atan2(math.sin(rad) * math.sin(distance / 6378137) * math.cos(lat1), math.cos(distance / 6378137) - math.sin(lat1) * math.sin(lat))
    return  round(lat * 180 / math.pi,4), round(lng * 180 / math.pi,4)

def calcDimensions(args):
    zoomLevel = args.zoomLevel
    maxZoom = 1000        #km for the width
    variableZoom = 850
    widthInKm = maxZoom-(((zoomLevel/4))*variableZoom)
    heightInKm = (widthInKm/16)*9
    return widthInKm,heightInKm

def combineURL(args,satellite,time):
    widthInKm,heightInKm = calcDimensions(args)
    bbox = boundingBox(args.latitude, args.longitude, widthInKm, heightInKm)
    url = f"https://view.eumetsat.int/geoserver/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS={satellite}&STYLES=&tiled=true&TIME={time}&WIDTH=1920&HEIGHT=1080&CRS=EPSG:4326&BBOX={bbox}"
    return url

def getNoon(longitude, latitude):
    pos = astral.Observer(longitude=longitude, latitude=latitude,elevation=0)
    yesterday = datetime.date.today()-datetime.timedelta(days=1)
    s = sun(pos, date=yesterday)
    noon = s["noon"]
    hour = noon.hour-(noon.hour%3)
    strTime = str(hour).zfill(2)+":00:00Z"
    return strTime

def checkForNight(img):
    #eps:m03_ir108
    pixels = img.getdata()
    nblack = 0
    for pixel in pixels:
        if pixel[3] != 255:
            nblack += 1
    n = len(pixels)

    print(nblack / float(n))

def makeColorgrading(fileName,fileNameOut):
    #fileNameOut = "final_foreground.png"
    os.system(f'magickScripts/autolevel -c rgb {fileName} autolevel_foreground.png')
    os.system('magickScripts/autotone -n -s autolevel_foreground.png autotone_foreground.png')
    os.system('magickScripts/matchimage -c rgb autotone_foreground.png sentinel_background.png matchimage_foreground.png')
    os.system(f'magickScripts/autotone -n -s matchimage_foreground.png {fileNameOut}')
    os.system('rm autolevel_foreground.png autotone_foreground.png matchimage_foreground.png')
    return fileNameOut

def transparentOverlay(img):
    h,w,_ = img.shape
    mask = np.zeros([h,w], dtype="uint8")
    for i in range(h):
        for j in range(w):
            alpha = float(img[i][j][3]/255.0)
            if alpha >= 0.7:
                mask[i][j] = 255
            else:
                mask[i][j] = 0
    return mask

def addAlphaChannel(fileNamewithAlpha, fileName):
    img = cv2.imread(fileNamewithAlpha , cv2.IMREAD_UNCHANGED)
    final_foreground = cv2.imread(fileName , cv2.IMREAD_UNCHANGED)

    mask = transparentOverlay(img)
    rgba = cv2.cvtColor(final_foreground, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = mask
    cv2.imwrite(fileNamewithAlpha, rgba)

def fetchImage(args):
    filenameForeground = "sentinel_foreground.png"
    filenameBackground = "sentinel_background.png"
    
    noonTime = getNoon(args.longitude, args.latitude)
    date = datetime.datetime.now(datetime.timezone.utc)
    date = date-datetime.timedelta(hours=3)
    noonTime = date.strftime("%Y-%m-%dT")+noonTime
    print(f"Image for: {noonTime}.")

    #download the low res full disk image. (cureeently only for coller grading)
    url_background = combineURL(args,"mumi:wideareacoverage_rgb_natural",noonTime)
    img_back =  download(url_background)
    img_back.save(filenameBackground)

    #download first image
    time = date.strftime("%Y-%m-")+str(date.day-1).zfill(2)+"T00:00:00Z"
    url = combineURL(args,"copernicus:daily_sentinel3ab_olci_l1_rgb_fulres",time)
    bg =  download(url)
    #download the rest 
    for day in reversed(range(2,5)):
        time = date.strftime("%Y-%m-")+str(date.day-day).zfill(2)+"T00:00:00Z"
        print(f"Downloading Image from {time}...")
        url = combineURL(args,"copernicus:daily_sentinel3ab_olci_l1_rgb_fulres",time)
        print(f"with URl:   {url}")
        print()
        img =  download(url)
        if img.mode == "RGB":
            a_channel = Image.new('L', img.size, 255)   # 'L' 8-bit pixels, black and white
            img.putalpha(a_channel)
        bg.paste(img, (0, 0),img)
    bg.save(filenameForeground)
    colorGradedFileName = makeColorgrading(filenameForeground,"backgroundImage.png")
    colorGraded = Image.open(colorGradedFileName)

    os.system('rm sentinel_foreground.png sentinel_background.png final_foreground.png colorGraded.png')
    return colorGraded
    