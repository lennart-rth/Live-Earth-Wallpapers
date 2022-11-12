import argparse
import sys

from utils import get_project_path
from image_parser import parse_image
from set_background import set_background
from utils import save_image

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--config",
        type=str,
        default=f"{get_project_path()}/recources/config.yaml",
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

if __name__ == '__main__':
    args = parseArgs()
    img = parse_image(args.config)
    file_name = "./recources/background.png"
    save_image(img, file_name)
    set_background(file_name)

    if args.output is not None:
        save_image(img, args.output)