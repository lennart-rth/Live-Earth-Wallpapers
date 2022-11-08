import datetime
import json
import sys
import urllib.request
from multiprocessing.pool import ThreadPool as Pool

from PIL import Image

from utils import download

satellite_data = {
    # (minute,second,MaxZoomLevel)
    "goes-16": (10, 20, 4),
    "goes-17": (10, 31, 4),
    "goes-18": (10, 20, 4),
    "himawari": (10, 0, 4),
    "meteosat-9": (15, 0, 3),
    "meteosat-11": (15, 0, 3),
}


def get_time_code(sat):
    url = f"https://rammb-slider.cira.colostate.edu/data/json/{sat}/full_disk/natural_color/latest_times.json"
    f = urllib.request.urlopen(url)
    data = json.load(f)
    latest = data["timestamps_int"][0]
    date = datetime.datetime.strptime(str(latest), "%Y%m%d%H%M%S").strftime("%Y/%m/%d")

    return latest, date


def calc_tile_coordinates(zoomLevel):
    # zoomlevel 0-3 or 0-4 (depending on the satellite)
    t_n = 2**zoomLevel
    row = range(0, t_n)
    col = range(0, t_n)
    return list(row), list(col)


def build_url(args):
    if (
        args.source == "meteosat-9" or args.source == "meteorsat-10"
    ) and args.zoomLevel > 4:
        sys.exit("Meteosat does not support Zoom Levels greater than 4.")

    time_code, date = get_time_code(args.source)

    name = args.colorMode
    if name == None:
        name = "natural_color"  # default color mode

    supported_args = ["geocolor", "natural_color"]
    if name not in supported_args:
        raise ValueError(
            "Wrong parameter for colorMode: Meteorsat and Goes only support 'natural_color' or 'geocolor' as colorMode!"
        )

    base_url = f"https://rammb-slider.cira.colostate.edu/data/imagery/{date}/{args.source}---full_disk/{name}/{time_code}/0{args.zoomLevel}"
    return base_url


def get_image(args, base_url):
    row, col = calc_tile_coordinates(args.zoomLevel)

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
        img_map[str(r) + ":" + str(c)] = img
        return img

    import time

    start = time.time()

    with Pool(len(row_col_pairs)) as pool:
        pool.map(download_func, row_col_pairs)
        print("Stiching images...")

    bg = Image.new("RGB", (0, 0))

    # stich the images together based n the position in the grid.
    for r in row:
        for c in col:
            img = img_map[str(r) + ":" + str(c)]
            new_bg = Image.new(
                "RGB", (img.width * (max(col) + 1), img.height * (max(row) + 1))
            )
            new_bg.paste(bg, (0, 0))
            new_bg.paste(img, (img.width * (c), (r) * img.height))

            bg = new_bg

    end = time.time()
    print("Downloads took: ", end - start)
    # zoom out a bit
    wallpaper = Image.new("RGB", (int(bg.width * 1.2), int(bg.height * 1.2)))
    wallpaper.paste(bg, (int(0 + (bg.width * 0.1)), int(0 + (bg.height * 0.1))))

    return wallpaper
