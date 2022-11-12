import yaml
from PIL import Image, ImageColor
from sentinel import load_sentinel
from nasa_sdo import load_sdo
from full_disks import load_geostationary


def load_yaml(filename):
    with open(filename, "r") as ymlfile:
        cfg = yaml.load(ymlfile,Loader=yaml.Loader)

    return cfg

def parse_image(config_file_dir):
    config = load_yaml(f"{config_file_dir}/config.yml")
    image_settings = config["settings"]

    bg_color = image_settings["bg-color"]
    bg_size = (image_settings["width"],image_settings["height"])

    bg = Image.new("RGB",bg_size,ImageColor.getrgb("#"+bg_color))

    for satellite,value in config["planets"].items():
        pos = (value["x"], value["y"])
        im_size = (value["width"], value["height"])

        if satellite == "sentinel":
            raw_img = load_sentinel(value)

        elif satellite == "sdo":
            raw_img = load_sdo(value)

        #load static image of planet into the bg
        elif satellite == "external_planet":
            # raw_img = load_external(value)
            pass

        # meteosat, goes or himawari
        else:
            raw_img = load_geostationary(value,satellite)

        resized_img = raw_img.resize(im_size)
        bg.paste(resized_img, pos)
    
    return bg


# im = parse_image("./recources")
# im.show()