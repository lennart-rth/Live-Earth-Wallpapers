import datetime
import json
import sys
import urllib.request
from multiprocessing.pool import ThreadPool as Pool
import time

from PIL import Image

from liewa.liewa_cli.utils import download

sizes = {
    "goes-16": 678,
    "goes-17": 678,
    "goes-18": 678,
    "himawari": 688,
    "gk2a": 688,
    "meteosat-9": 464,
    "meteosat-0deg": 464,
    # "meteosat-11": 464,
}


def get_time_code(satellite, name):
    url = f"https://rammb-slider.cira.colostate.edu/data/json/{satellite}/full_disk/{name}/latest_times.json"
    f = urllib.request.urlopen(url)
    data = json.load(f)
    latest = data["timestamps_int"][0]
    date = datetime.datetime.strptime(str(latest), "%Y%m%d%H%M%S").strftime("%Y/%m/%d")

    return latest, date


def calc_tile_coordinates(scale):
    # Zoom level 0-3 or 0-4 (depending on the satellite)
    tiles_n = 2 ** scale
    row = range(0, tiles_n)
    col = range(0, tiles_n)
    return list(row), list(col)


def calc_scale(satellite, **kwargs):
    size = sizes[satellite]
    minimum_side = kwargs.get("size", 1024)
    scale = int(minimum_side / size / 1.2)  # up scale < 120%

    scale = max(min(scale.bit_length(), 4), 0)   # log_2 scale between 0-4
    if satellite.lower().startswith("meteosat") and scale == 4:
        scale = 3  # Meteosat 9 and 0deg only support up to 8x zoom

    return scale


def build_url(satellite, scale, **kwargs):
    if scale > 4:
        sys.exit("Does not support Zoom Levels greater than 4.")

    name = kwargs.get("color", "natural_color")

    supported_args = ["geocolor", "natural_color"]
    if name not in supported_args:
        raise ValueError(
            "Wrong parameter for colorMode: Meteorsat and Goes only support 'natural_color' or 'geocolor' as colorMode!"
        )

    time_code, date = get_time_code(satellite, name)
    base_url = f"https://rammb-slider.cira.colostate.edu/data/imagery/{date}/{satellite}---full_disk/{name}/{time_code}/0{scale}"
    return base_url


def load_geostationary(satellite, **kwargs):
    scale = calc_scale(satellite, **kwargs)
    base_url = build_url(satellite, scale, **kwargs)
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

    # stich the images together based on the position in the grid.
    bg = Image.new("RGB", (sizes[satellite] * (max(col) + 1), sizes[satellite] * (max(row) + 1)))
    for r, c in row_col_pairs:
        img = img_map[str(r) + ":" + str(c)]
        bg.paste(img, (img.width * (c), (r) * img.height))

    end = time.time()
    print("Downloads took: ", end - start)

    return bg
