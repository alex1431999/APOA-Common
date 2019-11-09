"""
All the setup required to make the project a library is done here
"""

# Setuptools is used to setup the library
import setuptools

setuptools.setup(
    name='final-year-project-commong',
    version='0.0.1',
    description='The library of all common functionality within the project',
    url='git@gitlab.com:alex1431999/final-year-project-common.git',
    author='Alexander Haller',
    author_email='alexhaller99@yahoo.de',
    license='unlicense',
    packages=setuptools.find_packages(),
    zip_safe=False
)
