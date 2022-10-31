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

def deg2rad(degrees):
    return math.pi*degrees/180.0

def rad2deg(radians):
    return 180.0*radians/math.pi

# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84EarthRadius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

def boundingBox(longitudeInDegrees, latitudeInDegrees, widthInKm, heightInKm):
    lat = deg2rad(longitudeInDegrees)
    lon = deg2rad(latitudeInDegrees)
    widthSide = 1000*widthInKm
    heightSide = 1000*heightInKm


    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    latMin = lat - widthSide/radius
    latMax = lat + widthSide/radius
    lonMin = lon - heightSide/pradius
    lonMax = lon + heightSide/pradius

    return (str(rad2deg(lonMin))+","+str(rad2deg(latMin))+","+str(rad2deg(lonMax))+","+str(rad2deg(latMax)))

def calcDimensions(args):
    zoomLevel = args.zoomLevel
    maxZoom = 1000        #km for the width
    variableZoom = 850
    widthInKm = maxZoom-(((zoomLevel/4))*variableZoom)
    heightInKm = (widthInKm/16)*9
    return widthInKm,heightInKm

def combineURL(args,satellite,time):
    widthInKm,heightInKm = calcDimensions(args)
    bbox = boundingBox(args.longitude, args.latitude, widthInKm, heightInKm)
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
    


# print(boundingBox(8.876953,40.474114,1920/3,1080/3))
#fetchImage({"latitude":-19.228177,"longitude":121.069336,"zoomLevel":0})
