import argparse
import sys
import os

from liewa.utils import get_project_path, save_image, get_current_time
from liewa.image_parser import parse_image
from liewa.set_background import set_background

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="config1",
        help="The config file location"
    )
    # parser.add_argument(
    #     '-g',
    #     action='store_true',
    #     help="set to show a gui.",
    #     )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Dir where the images are saved."
    )

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    return args

def main():
    args = parseArgs()

    if args.config == "config1":
        args.config = os.path.join(get_project_path(),"recources","config1.yml")
        img = parse_image(args.config)
    elif args.config == "config2":
        args.config = os.path.join(get_project_path(),"recources","config2.yml")
        img = parse_image(args.config)
    elif args.config == "config3":
        args.config = os.path.join(get_project_path(),"recources","config3.yml")
        img = parse_image(args.config)
    else:
        img = parse_image(args.config)

    file_name = os.path.join(get_project_path(),"recources","backgroundImage.png")
    save_image(img, file_name, None)
    set_background(file_name)

    if args.output is not None:
        file_name = get_current_time() + ".png"
        save_image(img, args.output, file_name)

if __name__ == '__main__':
  main() 