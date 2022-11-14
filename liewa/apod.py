from bs4 import BeautifulSoup
import requests

from liewa.utils import download

# ? this function scrapes the website if they add another image to the website before the apod image this function will not work, image does not have id tag.
def load_apod(args):
	
	url = "https://apod.nasa.gov/apod/"
	res = requests.get(url)

	soup = BeautifulSoup(res.text, 'html.parser')
	
	imgList = soup.find_all('img')
	imgURL =  url + imgList[0]['src']
	
	img = download(imgURL)
	
	# TODO: work on resize
	# img = img.resize((args.width, args.height))

	return img