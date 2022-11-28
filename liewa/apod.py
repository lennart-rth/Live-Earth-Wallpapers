from bs4 import BeautifulSoup
import requests

# from utils import download
from liewa.utils import download


# ? this function scrapes the website if they add another image to the website before the apod image this function will not work, image does not have id tag.
def load_apod():

    url = "https://apod.nasa.gov/apod/"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    imgList = soup.find_all("img")
    imgURL = url + imgList[0]["src"]

    print(f"Downloading Image ({imgURL})")
    img = download(imgURL)

    return img
