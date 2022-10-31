#!/usr/bin/env python3
import datetime
import os
import argparse
import sys

from full_disks import buildUrl,getImage
from sentinel import fetchImage
from utils import setBG


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-z", "--zoomLevel", type=int, choices=[0, 1, 2, 3, 4], default=3,
                            help="Change the ImageSize 0=678, 1=1356, 2=2712, 3=5424, 4=10848 (Meteosat does not support Level 4)")
    parser.add_argument("-s", "--source", type=str, choices=["goes-16","goes-17","goes-18","himawari","meteosat-9","meteosat-11","sentinel"], default="meteosat-9",
                            help="Select Satellite as a source. goes-16, goes-17, goes-18, himawari, meteosat-9, meteosat-11, sentinel")
    parser.add_argument("-p", "--bgProgram", type=str, choices=["feh","nitrogen","gsettings"],
                            help="Select Programm to set the Background.")
    parser.add_argument("-a", "--latitude", type=float, default=40.474114,
                            help="Set the latitude of the Background image bounding box you want to set.")
    parser.add_argument("-b", "--longitude", type=float, default=8.876953,
                            help="Set the longitude of the Background image bounding box you want to set.")

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    return args

if __name__ == "__main__":
    args = parseArgs()
    if args.source != "sentinel":
        base_url = buildUrl(args)
        bg = getImage(args,base_url)
    elif args.source == "sentinel":
        bg = fetchImage(args)

    logDate = datetime.datetime.now(datetime.timezone.utc).strftime("%d_%m_%Y_%H_%M")
    filename = f"{os.path.dirname(os.path.realpath(__file__))}/backgroundImage.png"
    bg.save(filename)
    print(f"Image saved to: {filename}")
    setBG(args.bgProgram,filename)

    