"""
All the setup required to make the project a library is done here
"""

# For reading requirements.txt
import os

# Setuptools is used to setup the library
import setuptools


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
REQUIREMENTS_PATH = CURRENT_DIR + '/requirements.txt'

install_requires = []
if os.path.isfile(REQUIREMENTS_PATH):
    with open(REQUIREMENTS_PATH) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name='final-year-project-common',
    version='0.1.3',
    description='The library of all common functionality within the project',
    url='git@gitlab.com:alex1431999/final-year-project-common.git',
    author='Alexander Haller',
    author_email='alexhaller99@yahoo.de',
    license='unlicense',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    zip_safe=False
)
