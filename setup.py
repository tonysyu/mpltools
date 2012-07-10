#! /usr/bin/env python
from distutils.core import setup

import setuptools

from mpltools import __version__


with open('README.rst') as f:
    long_description = f.read()

setup(name='mpltools',
      version=__version__,
      description='Tools for Matplotlib',
      long_description=long_description,
      author='Tony S. Yu',
      author_email='tsyu80@gmail.com',
      license='Modified BSD',
      url='http://tonysyu.github.com/mpltools/',
      download_url='http://github.com/tonysyu/mpltools',
      packages=setuptools.find_packages(),
      package_data={'mpltools': ['mpltoolsrc', 'style/*.rc']},
      include_package_data=True,
     )
