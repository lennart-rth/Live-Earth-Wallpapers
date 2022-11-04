from PIL import Image
from utils import download

def getSDOImage():
    url="https://sdo.gsfc.nasa.gov/assets/img/latest/latest_4096_0304.jpg"
 
    print(f"Downloading Image ({url})")
    img = download(url)
    img = img.resize((1080,1080))

    wallpaper = Image.new('RGB', (1920,1080))
    wallpaper.paste(img, (int(960-(img.width/2)),0))
    return wallpaper