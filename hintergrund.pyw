import requests
import os



def download_pic_of_day():
    url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    r = requests.get(url)

    if r.status_code != 200:
        return
    
    picture_url = r.json()['url']
    if "jpg"  in picture_url:
        pic = requests.get(picture_url , allow_redirects=True)
        filename = '/home/lennart/Dokumente/backgroundChange/nasa_pic.png'

        open(filename, 'wb').write(pic.content)
        
        os.system("gsettings set org.gnome.desktop.background picture-uri file:/home/lennart/Dokumente/backgroundChange/nasa_pic.png")
        os.system("gsettings set org.gnome.desktop.background picture-options 'wallpaper' ")

download_pic_of_day()




    

