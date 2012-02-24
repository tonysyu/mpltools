
===============
Getting Started
===============

`mpltools` provides tools for Matplotlib_ that make it easier to adjust the
style, choose colors, make specialized plots, etc.


Styles
======

A key feature of `mpltools` is the idea of "styles"---essentially stylesheets
that are similar to matplotlibrc_ files. Unfortunately, the syntax for
a "mplstyle" file is slightly different than `matplotlibrc` files because
we use ConfigObj_ to parse them.

Style names should be specified as sections in "mplstyle" files.  A simple
`mplstyle` file would look like::

    [style1]

    text.fontsize = 12
    figure.dpi = 150

    [style2]

    text.fontsize = 10
    font.family = 'serif'

`mpltools` searches the current working directory and ~/.mplstyle/ directory
for "mplstyle" files. To use a style, you just add::

    >>> import mpltools
    >>> mpltools.style.use('style1')

There are a number of pre-defined styles located in `mpltools/style/`. To list
all available styles, use::

    >>> print mpltools.styles


.. _Matplotlib: http://matplotlib.sourceforge.net/
.. _matplotlibrc: http://matplotlib.sourceforge.net/users/customizing.html
.. _ConfigObj: http://www.voidspace.org.uk/python/configobj.html

