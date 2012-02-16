"""Tools for Matplotlib

The primary purpose of this package is to provide tools to use pre-configured
styles with matplotlib.

Subpackages
===========
style
    Library of styles and functions for setting the style.
color
    Color choice and custom colors (e.g. parameter-based color choice).

Utility functions
=================
figure
    Create matplotlib figure with specified aspect ratio and scale.
figsize
    Calculate figure size based on aspect ratio and scale.

Attributes
==========
styles
    Available matplotlib styles.
config
    Dictionary of package configuration settings.

"""
from util import *

import os.path as _osp
pkgdir = _osp.abspath(_osp.dirname(__file__))

import _config
config = {}
for cfg in _config.iter_paths([_osp.join(pkgdir, 'mpltoolsrc'),
                               '~/.mpltoolsrc',
                               './mpltoolsrc']):
    config.update(cfg)

import style
styles = style.lib.keys()

import color

# clean up namespace
del _osp, _config
