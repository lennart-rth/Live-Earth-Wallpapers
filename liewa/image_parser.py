import yaml
from PIL import Image, ImageColor, ImageOps
from liewa.apod import load_apod
from liewa.sentinel import load_sentinel
from liewa.nasa_sdo import load_sdo
from liewa.full_disks import load_geostationary


def load_yaml(filename):
    with open(filename, "r") as ymlfile:
        cfg = yaml.load(ymlfile,Loader=yaml.Loader)

    return cfg

def parse_image(config_file_dir):
    config = load_yaml(config_file_dir)
    image_settings = config["settings"]

    bg_color = image_settings["bg-color"]
    bg_size = (image_settings["width"],image_settings["height"])

    bg = Image.new("RGB",bg_size,ImageColor.getrgb(bg_color))

    for satellite,value in config["planets"].items():
        if satellite == "sentinel":
            raw_img = load_sentinel(value)
            im_size = (value["width"], value["height"])
            resized_img = raw_img.resize(im_size)

        elif satellite == "sdo":
            raw_img = load_sdo(value)
            resized_img = raw_img.resize((value["size"],value["size"]))

        elif satellite == "apod":
            raw_img = load_apod()

            im_size = (value["width"], value["height"])
            if value['fit'] == "fill":
                resized_img = raw_img.resize(im_size)
            elif value['fit'] == "contain":
                resized_img = ImageOps.contain(raw_img, im_size)
            elif value['fit'] == "cover":
                resized_img = ImageOps.fit(raw_img, im_size)

        #load static image of planet into the bg
        elif satellite == "external_planet":
            # raw_img = load_external(value)
            pass

        # meteosat, goes or himawari
        else:
            raw_img = load_geostationary(value,satellite)
            resized_img = raw_img.resize((value["size"],value["size"]))

        pos = (int(value["x"]-(resized_img.width/2)), int(value["y"]-(resized_img.height/2)))
        bg.paste(resized_img, pos)
    
    return bg


# im = parse_image("./recources")
# im.show()