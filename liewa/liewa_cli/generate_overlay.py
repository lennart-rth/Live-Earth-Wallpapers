import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

from liewa.liewa_cli.utils import get_project_path

long_0 = {
    'goes-16': -75.0,
    'goes-18': -137.0,
    'himawari': 140.7,
    'gk2a': 128.2,
    'meteosat-9': 45.5,
    'meteosat-0deg': 0.0,
}
sizes = {
    "goes-16": 678,
    "goes-18": 678,
    "himawari": 688,
    "gk2a": 688,
    "meteosat-9": 464,
    "meteosat-0deg": 464,
}

scale_factor = {
    "goes-16": 1.0,
    "goes-18": 1.0,
    "himawari": 0.9874,
    "gk2a": 0.9856,
    "meteosat-9": 0.9765,
    "meteosat-0deg": 0.9765,
}


def generate_overlay(satellite, scale):
    height = 35785831.0
    # Define the projection
    data_proj = ccrs.Geostationary(central_longitude=long_0[satellite], satellite_height=height)

    # Create the figure
    size = (2 ** scale) * sizes[satellite] / 300
    fig = plt.figure(figsize=(size, size))
    ax = fig.add_subplot(1, 1, 1, projection=data_proj)

    # Add features to the map
    res = '50m'
    ax.add_feature(cfeature.STATES.with_scale(res), linestyle=':', edgecolor='#ed8', linewidth=0.25, alpha=0.75)
    ax.add_feature(cfeature.BORDERS.with_scale(res), linestyle='--', edgecolor='#ed8', linewidth=0.35, alpha=0.75)
    ax.add_feature(cfeature.COASTLINE.with_scale(res), edgecolor='#8ee', linewidth=0.35, alpha=0.75)

    # Add gridlines
    # ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', linestyle='--')

    # Save the figure
    ax.axis('off')
    ax.set_global()
    margin = (1 - scale_factor[satellite]) / 2
    plt.subplots_adjust(left=margin, bottom=margin, right=1 - margin, top=1 - margin, wspace=0, hspace=0)
    # 保存图片
    overlay_path = os.path.join(get_project_path(), "recources", f"border_{satellite}_{scale:02d}.png")
    plt.savefig(overlay_path, dpi=300, transparent=True)
    plt.close()


if __name__ == '__main__':
    for satellite in long_0.keys():
        for scale in range(0, 5):
            generate_overlay(satellite, scale)
