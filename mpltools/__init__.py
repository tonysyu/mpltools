"""Tools for Matplotlib

The primary purpose of this package is to provide tools to use pre-configured
styles with matplotlib.

Subpackages
===========
style
    Library of styles and functions for setting the style.

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

"""
from utils import *
import style
styles = style.lib.keys()

