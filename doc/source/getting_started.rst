
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


``plot2rst`` Sphinx extension
=============================

The ``plot2rst`` Sphinx_ extension provides a simple way to generate
reStructuredText_ (rst) examples from python files. As the name suggests,
there's built-in handling of Matplotlib plots. Example python files will have
their docstrings converted to rst, and python code will be placed in a Sphinx
code-block. Check out the `example gallery`_ for details.

To generate your own examples, add ``'mpltools.sphinx.plot2rst'`` to the list
of ``extensions`` in your Sphinx configuration file. In addition, make sure the
example directory(ies) in ``plot2rst_paths`` points to a directory with
examples named ``plot_*.py`` and include an ``index.rst`` file. By default, the
example path points to::

   plot2rst_paths = ('../examples', 'auto_examples')

The first directory specifies the location of the python files, and the
second directory specifies where to save the rst examples. Note that the paths
are relative to the Sphinx source directory (where ``conf.py`` lives); using
these defaults, I would define my example gallery as follows (this is a snippet
from the ``mpltools`` directory structure)::

   doc/
      source/
         conf.py
         ...
      examples/
         index.rst
         layout/
            index.rst
            plot_cross_spines.py
            plot_figaspect.py
         ...
      ...

When building the docs, ``plot2rst`` will generate the ``auto_examples``
directory, which will look something like::

   doc/
      source/
         conf.py
         auto_examples/
            index.rst
            layout/
               images/
                  <generated images>
               plot_cross_spines.py
               plot_cross_spines.rst
               plot_figaspect.py
               plot_figaspect.rst
            ...
         ...
      examples/
         <unchanged>
      ...

Note that python files are copied to the ``auto_examples`` directory (and later
to the build directory) because a download link is added to the example.

If you're wondering about all of the ``index.rst`` files in the ``examples``
directory, these are used for custom markup. They could be blank files, but
more likely you'd want to add headers and possibly, descriptive text. For
example, the ``doc/examples/index.rst`` file in ``mpltools`` just has::

   Examples
   ========

and ``doc/examples/layout/index.rst`` has::

   ``layout`` module
   -----------------

Note: ``plot2rst`` was adapted from ``genrst.py`` in scikits-image_, which
borrowed the implementation from scikit-learn_.


.. _Matplotlib: http://matplotlib.sourceforge.net/
.. _matplotlibrc: http://matplotlib.sourceforge.net/users/customizing.html
.. _ggplot: http://had.co.nz/ggplot/
.. _R: http://www.r-project.org/
.. _ConfigObj: http://www.voidspace.org.uk/python/configobj.html
.. _Sphinx: http://sphinx.pocoo.org/
.. _reStructuredText: http://sphinx.pocoo.org/rest.html
.. _scikits-image: http://scikits-image.org/
.. _scikit-learn: http://scikit-learn.org/stable/

