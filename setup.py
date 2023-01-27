import os
import platform
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def OSdependentReqs():
    system = platform.system()
    if system == 'Windows':
        return ["beautifulsoup4",
                "Pillow", 
                "numpy", 
                "opencv_python", 
                "PyYAML",
                "requests",
                "PyQt5",
                "pywin32",]
    else:
        return ["beautifulsoup4",
                "Pillow", 
                "numpy", 
                "opencv_python", 
                "PyYAML",
                "requests",
                "PyQt5"]

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = "liewa",
    version = "3.1",
    author = "lennart-rth",
    description = "Generate synthetic background images with near real time satellite images.",
    license = "GNU",
    keywords =  "Desktop Backgroundimage Satellite Live Earth meteosat himawari goes Space Images",
    url = "https://github.com/lennart-rth/Live-Earth-Wallpapers",
    packages=find_packages(),
    # excluded = ['liewa_gui.*','liewa_cli.*']
    py_modules=['cli'],
    package_dir={'liewa': 'liewa',
                'liewa.liewa_cli': 'liewa/liewa_cli',
                'liewa.liewa_gui': 'liewa/liewa_gui',},
    package_data={
        "liewa": ["liewa_cli/recources/*.yml","liewa_gui/icon.svg"],
    },
    # package_data={'liewa': [os.path.join('recources','*.yml'),'liewa-cli','liewa_gui': ['liewa-gui']]},
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=OSdependentReqs(),
    scripts=[os.path.join('liewa','liewa_cli','liewa-cli'),os.path.join('liewa','liewa_gui','liewa-gui')],
    # entry_points = {'console_scripts': ['liewa-gui=liewa.liewa_gui.'],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)