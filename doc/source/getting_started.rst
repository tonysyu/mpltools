
===============
Getting Started
===============

``mpltools`` provides tools for Matplotlib_ that make it easier to adjust the
element styles, choose colors, make specialized plots, etc. For the most part,
these tools are only loosely-connected in functionality, so the best way to get
started is to look at the `example gallery`_.


Styles
======

This package got its start by implementing plotting "styles"---essentially
style sheets that are similar to matplotlibrc_ files.

There are a number of pre-defined styles located in ``mpltools/style/``. For
example, there's a pre-defined stall called "ggplot", which emulates the
aesthetics of ggplot_ (a popular plotting package for R_). To use this style,
just add::

   >>> from mpltools import style
   >>> style.use('ggplot')

To list all available styles, use::

   >>> print style.available


Defining your own style
-----------------------

Unfortunately, the syntax for an ``mplstyle`` file is slightly different than
matplotlibrc_ files because ``mpltools`` uses ConfigObj_ to parse them. For
example the first few lines of the "ggplot" style looks like::

   patch.linewidth = 0.5
   patch.facecolor = '#348ABD'  # blue
   patch.edgecolor = '#EEEEEE'
   patch.antialiased = True

Unlike matplotlibrc_ files, key/value pairs are separated by an equals sign and
strings must be quoted.

You can specify styles in either an ``mplstyle`` file or a ``*.rc`` file
located in ``~/.mplstylelib/``. In an ``mplstyle`` file, style names should be
specified as sections. A simple ``mplstyle`` file might look like::

   [style1]

   text.fontsize = 12
   figure.dpi = 150

   [style2]

   text.fontsize = 10
   font.family = 'serif'

Alternatively, a single style is specified in each ``*.rc`` file found in
``~/.mplstylelib/``, and the file name determines the style name. For example,
a style file named ``~/.mplstylelib/mystyle.rc`` would define ``mystyle``.


Style priority
--------------

``mpltools`` searches the current working directory and your home directory for
``mplstyle`` files. In addition, it looks in ``~/.mplstylelib/`` for ``*.rc``
files. If for some reason, you decide to define the same style in multiple
places, the resolution order is

1. ``./mplstyle``
2. ``~/.mplstyle``
3. ``~/.mplstylelib/*.rc``
4. ``mpltools/style/*.rc``

So, if you define ``~/.mplstylelib/mystyle.rc`` and a section ``[mystyle]`` in
``./mplstyle``, then the later will *update* the former (redefined settings are
overridden, but keys undefined in ``./mplstyle`` remain).


.. _Matplotlib: http://matplotlib.sourceforge.net/
.. _matplotlibrc: http://matplotlib.sourceforge.net/users/customizing.html
.. _ggplot: http://had.co.nz/ggplot/
.. _R: http://www.r-project.org/
.. _ConfigObj: http://www.voidspace.org.uk/python/configobj.html

