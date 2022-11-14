import os
import time
from io import BytesIO
import datetime

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

def get_project_path():
    return os.path.dirname(os.path.realpath(__file__))

def save_image(img, filename, file):
    if file == None:
        img.save(os.path.join(filename))
    else:
        img.save(os.path.join(filename,file))

def get_current_time():
    return datetime.datetime.today().strftime('%Y-%m-%d_%H-%M')
