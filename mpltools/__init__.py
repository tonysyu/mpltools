"""Tools for Matplotlib

The primary purpose of this package is to provide tools to use pre-configured
styles with matplotlib.

Subpackages
===========
style
    Library of styles and functions for setting the style.
color
    Color choice and custom colors (e.g. parameter-based color choice).
layout
    Alter visual layout of plots (e.g. figure size, crossed spines).

Attributes
==========
styles
    Available matplotlib styles.
config
    Dictionary of package configuration settings.

"""
import _config
config = _config.config

import style
styles = style.lib.keys()

# clean up namespace
del _config
