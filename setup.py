import os
import platform
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def OSdependentReqs():
    system = platform.system()
    if system == 'Windows':
        return ["Pillow", 
                "numpy", 
                "opencv_python", 
                "PyYAML",
                "requests",
                "win32gui;platform_system=='Linux'"]
    else:
        return ["Pillow", 
                "numpy", 
                "opencv_python", 
                "PyYAML",
                "requests"]

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = "liewa",
    version = "2.1",
    author = "lennart-rth",
    description = "Generate synthetic background images with near real time satellite images.",
    license = "GNU",
    keywords =  "Desktop Backgroundimage Satellite Live Earth meteosat himawari goes Space Images",
    url = "https://github.com/lennart-rth/Live-Earth-Wallpapers",
    packages=find_packages(),
    package_dir={'liewa': 'liewa'},
    package_data={'liewa': ['recources/*.yml']},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=OSdependentReqs(),
    entry_points = {'console_scripts': ['liewa=liewa.__main__:main'],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)