import argparse
import sys
import os

from liewa.liewa_cli.utils import get_project_path, save_image, get_current_time
from liewa.liewa_cli.image_parser import parse_image
from liewa.liewa_cli.set_background import set_background

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="gui_config",
        help="The config file location"
    )
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
        args.config = os.path.join(get_project_path(),"recources","gui_config.yml")
        img = parse_image(args.config)

    if args.output is not None:
        save_image(img, args.output, None)
        set_background(args.output)
    else:
        file_name = os.path.join(get_project_path(),"recources","backgroundImage.png")
        save_image(img, file_name, None)
        set_background(file_name)

def execute():
    main()
# if __name__ == '__main__':
#   main()
