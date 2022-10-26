from PIL import Image
import requests
from io import BytesIO
import time 

filename = '/home/lennart/Dokumente/backgroundChange/eumesat.jpg'

for i in range(3):
    response = requests.get("https://eumetview.eumetsat.int/static-images/latestImages/EUMETSAT_MSG_RGBNatColourEnhncd_FullResolution.jpg")
    status = response.status_code
    if status == 200:
        break
    time.sleep(30)

img = Image.open(BytesIO(response.content))
img.save(filename)

