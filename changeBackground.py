#!/usr/bin/env python3
import argparse
import datetime
import os
import random
import sys

from full_disks import build_url, get_image
from nasa_sdo import get_sdo_image
from sentinel import fetch_image
from utils import make_border, set_background

sources = [
    "goes-16",
    "goes-17",
    "goes-18",
    "himawari",
    "meteosat-9",
    "meteosat-11",
    "sentinel",
    "sdo",
]
random_sources = [
    "goes-16",
    "goes-17",
    "goes-18",
    "himawari",
    "meteosat-9",
    "meteosat-11",
    "sdo",
]

sizes=[678,1356,5424,10848]

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-z",
        "--zoomLevel",
        type=int,
        choices=[0, 1, 2, 3, 4],
        default=3,
        help="Change the ImageSize 0=678, 1=1356, 2=2712, 3=5424, 4=10848 (Meteosat does not support Level 4)",
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        choices=sources,
        help="Select Satellite as a source. goes-16, goes-17, goes-18, himawari, meteosat-9, meteosat-11, sentinel, sdo (NASA Solar Dynamics Observatory)",
    )
    parser.add_argument(
        "-m",
        "--colorMode",
        type=str,
        choices=[
            "geocolor",
            "natural_color",
            "0171",
            "0171pfss",
            "0304",
            "0304pfss",
            "HMIIC",
        ],
        help="Select a color composite. geocolor and natural_color for goes, meteosat and himawari. The rest is only for SDO",
    )
    parser.add_argument(
        "-o",
        "--outFile",
        type=str,
        help="Full path to a dir to save all loaded images. If not specified no images will be saved. Useful for Timelapse generation",
    )
    parser.add_argument(
        "-p",
        "--bgProgram",
        type=str,
        choices=[
            "feh",
            "nitrogen",
            "gsettings",
            "osascript",
            "apple_defaults",
            "windows",
        ],
        help="Select Programm to set the Background.",
    )
    parser.add_argument(
        "-a",
        "--latitude",
        type=float,
        default=40.474114,
        help="Set the latitude of the Background image bounding box you want to set. Only for Sentinel as source.",
    )
    parser.add_argument(
        "-b",
        "--longitude",
        type=float,
        default=8.876953,
        help="Set the longitude of the Background image bounding box you want to set. Only for Sentinel as source.",
    )
    parser.add_argument(
        "-w", "--width", type=int, help="wanted width of the Wallpaper Image"
    )
    parser.add_argument(
        "-he", "--height", type=int, help="wanted heigth of the Wallpaper Image"
    )

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    return args


if __name__ == "__main__":
    args = parseArgs()

    if args.width is not None and args.height is not None:
        bigger=max([args.width,args.height])

        for i in range (0,sizes):
            if(bigger<sizes[i]):
                break
        
        args.zoomLevel=i


    if args.source is None:
        args.source = random.choice(random_sources)

    if args.source == "sdo":
        bg = get_sdo_image(args)

    elif args.source == "sentinel":
        bg = fetch_image(args)

    else:
        base_url = build_url(args)
        bg = get_image(args, base_url)

    if args.width is not None and args.height is not None:
            bg=make_border(bg,args.width,args.height)

    log_date = datetime.datetime.now(datetime.timezone.utc).strftime("%d_%m_%Y_%H_%M")
    filename = f"{os.path.dirname(os.path.realpath(__file__))}/backgroundImage.png"
    bg.save(filename)
    print(f"Image saved to: {filename}")


    if args.outFile is not None:
        image_path = f"{args.outFile}/{log_date}.png"
        bg.save(image_path)

    set_background(args.bgProgram, filename)
