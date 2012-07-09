#! /usr/bin/env python
from distutils.core import setup

import setuptools

from mpltools import __version__


setup(name='mpltools',
      version=__version__,
      description='Tools for Matplotlib',
      author='Tony S. Yu',
      author_email='tsyu80@gmail.com',
      license='Modified BSD',
      url='http://tonysyu.github.com/mpltools/',
      download_url='http://github.com/tonysyu/mpltools',
      packages=setuptools.find_packages(),
      package_data={'mpltools': ['mpltoolsrc', 'style/*.rc']},
     )
