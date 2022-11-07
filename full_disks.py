import datetime
from multiprocessing.pool import ThreadPool as Pool
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
    date = datetime.datetime.strptime(str(latest), '%Y%m%d%H%M%S').strftime("%Y/%m/%d")

    return latest, date

def calcTileCoordinates(zoomLevel):
    #zoomlevel 0-3 or 0-4 (depending on the satellite)
    t_n = 2**zoomLevel
    row = range(0,t_n)
    col = range(0,t_n)
    return list(row), list(col)


def buildUrl(args):
    if (args.source == "meteosat-9" or args.source == "meteorsat-10") and args.zoomLevel > 4:
        sys.exit("Meteosat does not support Zoom Levels greater than 4.")

    timeCode, date = getTimeCode(args.source) 

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
    image_width = 678
    image_height = 678

    bg = Image.new('RGB', (image_width*len(col),image_height*len(row)))
    row_col_pairs = []
    for r in row:
        for c in col:
            row_col_pairs.append([r, c])

    img_map = {}

    def download_func(row_col):
        r = row_col[0]
        c = row_col[1]
        url = base_url + f"/{str(r).zfill(3)}_{str(c).zfill(3)}.png"
        print(f"Downloading Image ({r},{c}).{url}")
        img = download(url)
        # store the images in a dict so we don't have to care about the order they're downloaded in
        img_map[str(r)+ ":" + str(c)] = img
        return img
        
    import time
    start = time.time()

    with Pool(len(row_col_pairs)) as pool:
        pool.map(download_func, row_col_pairs)

    for r in row:
        for c in col:
            img = img_map[str(r)+ ":" + str(c)]
            bg.paste(img, (image_width*(c), (r)*image_height))
            

    end = time.time()
    print("Downloads took: ", end - start)
    #zoom out a bit
    wallpaper = Image.new('RGB', (int(bg.width*1.2),int(bg.height*1.2)))
    wallpaper.paste(bg, (int(0+(bg.width*0.1)), int(0+(bg.height*0.1))))

    return wallpaper