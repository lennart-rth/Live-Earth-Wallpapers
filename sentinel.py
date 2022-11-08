import datetime
import math

import cv2
import numpy as np
from PIL import Image

from utils import download


def bounding_box(latitude_in_deg, longitude_in_deg, width_in_km, height_in_km):
    width_in_m = width_in_km * 1000
    height_in_m = height_in_km * 1000
    south_lat = point_lat_long(latitude_in_deg, longitude_in_deg, height_in_m, 180)[0]
    north_lat = point_lat_long(latitude_in_deg, longitude_in_deg, height_in_m, 0)[0]
    west_lon = point_lat_long(latitude_in_deg, longitude_in_deg, width_in_m, 270)[1]
    east_lon = point_lat_long(latitude_in_deg, longitude_in_deg, width_in_m, 90)[1]
    return f"{south_lat},{west_lon},{north_lat},{east_lon}"


def point_lat_long(Lat, Lng, distance, bearing):
    rad = bearing * math.pi / 180
    lat1 = Lat * math.pi / 180
    lng1 = Lng * math.pi / 180
    lat = math.asin(
        math.sin(lat1) * math.cos(distance / 6378137)
        + math.cos(lat1) * math.sin(distance / 6378137) * math.cos(rad)
    )
    lng = lng1 + math.atan2(
        math.sin(rad) * math.sin(distance / 6378137) * math.cos(lat1),
        math.cos(distance / 6378137) - math.sin(lat1) * math.sin(lat),
    )
    return round(lat * 180 / math.pi, 4), round(lng * 180 / math.pi, 4)


def calc_coord_dimension(args):
    zoom_level = args.zoomLevel
    max_zoom = 1000  # km for the width
    variable_zooom = 850  # the maximum kilometeres we can zoom in from the "maxZoom"
    # maxZoom - variableZoom determines the min zoom level

    width_in_km = max_zoom - (((zoom_level / 4)) * variable_zooom)
    if args.width is not None and args.height is not None:
        height_in_km = int(width_in_km / (args.width / args.height))
    else:  # default for args.width and args.heigth is 1920 and 1080
        height_in_km = int(width_in_km / (16 / 9))

    return width_in_km, height_in_km


def calc_img_dimensions(args):
    pixel_width = 1920
    if args.width is not None and args.height is not None:
        pixel_height = pixel_width / (args.width / args.height)
    else:
        pixel_height = pixel_width / (16 / 9)

    return int(pixel_width), int(pixel_height)


def combine_url(args, satellite, time):
    width_in_km, height_in_km = calc_coord_dimension(args)
    width_in_px, height_in_px = calc_img_dimensions(args)
    if args.latitude == None or args.longitude == None:
        raise ValueError(
            "No coordinates specified! You need to specifiy coordinates by passing the parametera -a and -b."
        )
    bbox = bounding_box(args.latitude, args.longitude, width_in_km, height_in_km)
    url = f"https://view.eumetsat.int/geoserver/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS={satellite}&STYLES=&tiled=true&TIME={time}&WIDTH={width_in_px}&HEIGHT={height_in_px}&CRS=EPSG:4326&BBOX={bbox}"
    return url


def white_balance(pilImg):
    img = np.asarray(pilImg)
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - (
        (avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1
    )
    result[:, :, 2] = result[:, :, 2] - (
        (avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1
    )
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return Image.fromarray(result)


def fetch_image(args):
    date_with_delay = datetime.datetime.now(datetime.timezone.utc)
    date_with_delay = date_with_delay - datetime.timedelta(hours=3)

    from multiprocessing.pool import ThreadPool as Pool

    def download_func(day):
        time = (
            date_with_delay.strftime("%Y-%m-")
            + str(date_with_delay.day - day).zfill(2)
            + "T00:00:00Z"
        )
        url = combine_url(args, "copernicus:daily_sentinel3ab_olci_l1_rgb_fulres", time)
        print(f"Downloading Image from {time}...\nwith URl:   {url}")
        img = download(url)
        return img

    with Pool(4) as pool:
        imgs = pool.map(download_func, [i for i in range(1, 5)])

    # Use the first image as the base
    bg = imgs[0]

    # Overlay the next 3 days worth of images overtop
    for day in range(1, 4):
        img = imgs[day]
        if img.mode == "RGB":
            a_channel = Image.new(
                "L", img.size, 255
            )  # 'L' 8-bit pixels, black and white
            img.putalpha(a_channel)

        bg.paste(img, (0, 0), img)

    color_graded = white_balance(bg)
    return color_graded
