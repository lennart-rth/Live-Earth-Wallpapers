import datetime
import json
import sys
import urllib.request
from multiprocessing.pool import ThreadPool as Pool
import time

from PIL import Image

from liewa_cli.utils import download


sizes = {"goes-16":678,
"goes-17":678,
"goes-18":678,
"himawari":688,
"meteosat-9":464,
"meteosat-11":464}

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

def calc_scale(args,satellite):
    size = sizes[satellite]
    minimum_side = args["size"]
    return int(minimum_side/size)

def build_url(args,satellite,scale):
    if (
        satellite == "meteosat-9" or satellite == "meteorsat-10"
    ) and scale > 4:
        sys.exit("Meteosat does not support Zoom Levels greater than 4.")

    time_code, date = get_time_code(satellite)

    name = args["color"]
    if name == None:
        name = "natural_color"  # default color mode

    supported_args = ["geocolor", "natural_color"]
    if name not in supported_args:
        raise ValueError(
            "Wrong parameter for colorMode: Meteorsat and Goes only support 'natural_color' or 'geocolor' as colorMode!"
        )

    base_url = f"https://rammb-slider.cira.colostate.edu/data/imagery/{date}/{satellite}---full_disk/{name}/{time_code}/0{scale}"
    return base_url


def load_geostationary(args,satellite):
    scale = calc_scale(args,satellite)
    base_url = build_url(args,satellite,scale)
    row, col = calc_tile_coordinates(scale)

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

    return bg
