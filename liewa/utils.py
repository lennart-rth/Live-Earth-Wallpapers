import os
import time
from io import BytesIO

import requests
from PIL import Image


# downloads a image from a url and return a pil Image
def download(url):
    for i in range(3):
        try:
            with requests.get(url) as response:
                return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"{i}/3 Could not download Image '{url}'...")
            time.sleep(1)



# function to add black rim around image
def make_border(image, width, height):
    width_diff = width / image.width
    height_diff = height / image.height
    scale_factor = min(width_diff, height_diff)

    old_im = image.resize(
        (int(image.width * scale_factor), int(image.height * scale_factor))
    )
    new_size = (width, height)

    new_im = Image.new("RGB", new_size)  ## luckily, this is already black!
    box = tuple(int((n / 2) - (o / 2)) for n, o in zip(new_im.size, old_im.size))
    new_im.paste(old_im, box)

    return new_im

def get_project_path():
    return os.path.dirname(os.path.realpath(__file__))

def save_image(img, filename):
    img.save(f"{filename}/")
