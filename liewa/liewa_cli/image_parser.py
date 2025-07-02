import yaml
from PIL import Image, ImageColor, ImageOps
from liewa.liewa_cli.apod import load_apod
from liewa.liewa_cli.sentinel import load_sentinel
from liewa.liewa_cli.nasa_sdo import load_sdo
from liewa.liewa_cli.full_disks import load_geostationary


def load_yaml(filename):
    with open(filename, "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.Loader)

    return cfg


def calc_load_region(satellite_size, canvas_size, satellite_center):
    # canvas origin relative to satellite image upper-left corner
    canvas_origin_x = -(satellite_center[0] - satellite_size[0] / 2)
    canvas_origin_y = -(satellite_center[1] - satellite_size[1] / 2)
    region_left = max(0, int(canvas_origin_x))
    region_top = max(0, int(canvas_origin_y))
    region_right = min(satellite_size[0], int(canvas_origin_x + canvas_size[0]))
    region_bottom = min(satellite_size[1], int(canvas_origin_y + canvas_size[1]))
    region_right = max(region_left, region_right)
    region_bottom = max(region_top, region_bottom)
    load_region = [region_top, region_left, region_bottom, region_right]
    print(f"load region: {load_region}")
    return load_region


def parse_image(config_file_dir):
    config = load_yaml(config_file_dir)
    image_settings = config["settings"]

    bg_color = image_settings["bg-color"]
    bg_size = (image_settings["width"], image_settings["height"])

    bg = Image.new("RGB", bg_size, ImageColor.getrgb(bg_color))

    for satellite, value in config["planets"].items():
        if satellite == "sentinel":
            raw_img = load_sentinel(value)
            im_size = (value["width"], value["height"])
            resized_img = raw_img.resize(im_size)

        elif satellite == "sdo":
            raw_img = load_sdo(value)
            resized_img = raw_img.resize((value["size"], value["size"]))

        elif satellite == "apod":
            raw_img = load_apod()

            im_size = (value["width"], value["height"])
            if value['fit'] == "fill":
                resized_img = raw_img.resize(im_size)
            elif value['fit'] == "contain":
                resized_img = ImageOps.contain(raw_img, im_size)
            elif value['fit'] == "cover":
                resized_img = ImageOps.fit(raw_img, im_size)

        # load static image of planet into the bg
        elif satellite == "external_planet":
            # raw_img = load_external(value)
            pass

        # meteosat, goes or himawari
        else:
            load_region = calc_load_region((value["size"], value["size"]), bg_size, (value["x"], value["y"]))

            args = value
            raw_img = load_geostationary(satellite, region=load_region, **args)

            scale_ratio = value["size"] / max(raw_img.size)
            new_width, new_height = (int(dim * scale_ratio) for dim in raw_img.size)
            resized_img = raw_img.resize((new_width, new_height))   # keep aspect ratio of the raw image

        pos = (int(value["x"] - (resized_img.width / 2)), int(value["y"] - (resized_img.height / 2)))
        bg.paste(resized_img, pos)

    return bg

# im = parse_image("./recources")
# im.show()
