from PIL import Image

import bisect
from liewa.liewa_cli.utils import download

sizes = [512, 1024, 2048, 4096]


def calc_scale(args):
    min_side = args["size"]
    return sizes[bisect.bisect_left(sizes, min_side)]


def load_sdo(args):
    name = args["bandwidth"]
    supported_args = ["0171", "0171pfss", "0304", "0304pfss", "HMIIC"]

    if name is None:
        name = "0304"  # default color mode

    if name not in supported_args:
        raise ValueError(
            f"Wrong parameter for colorMode: SDO only support '{supported_args}' as colorMode!"
        )

    scale = calc_scale(args)

    url = f"https://sdo.gsfc.nasa.gov/assets/img/latest/latest_{scale}_{name}.jpg"

    print(f"Downloading Image ({url})")
    img = download(url)

    return img
