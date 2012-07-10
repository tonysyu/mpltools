====================
Tools for Matplotlib
====================


As the name implies, ``mpltools`` provides tools for working with matplotlib_.
For the most part, these tools are only loosely-connected in functionality, so
the best way to get started is to look at the `example gallery`_.


Styles
======

This package got its start by implementing plotting "styles"---essentially
stylesheets that are similar to matplotlibrc_ files. Unfortunately, the syntax
for an ``mplstyle`` file is slightly different than matplotlibrc_ files because
we use ConfigObj_ to parse them.

Style names should be specified as sections in a "mplstyle" file.  A simple
``mplstyle`` file would look like::

    [style1]

    text.fontsize = 12
    figure.dpi = 150

    [style2]

    text.fontsize = 10
    font.family = 'serif'

``mpltools`` searches the current working directory and your home directory for
``mplstyle`` files. To use a style, you just add::

    >>> from mpltools import style
    >>> style.use('style1')

There are a number of pre-defined styles located in ``mpltools/style/``. To
list all available styles, use::

    >>> print style.available


Documentation
=============

For more details about use and installation, see the `mpltools documentation`_.
If you're short on time, just check out the `Getting Started`_ section or the
`example gallery`_.


Requirements
============

* matplotlib_ (of course)
* ConfigObj_


Installation from source
========================

``mpltools`` may be installed globally using::

    $ git clone git@github.com:tonysyu/mpltools.git
    $ cd mpltools
    $ python setup.py install

or locally using::

    $ python setup.py install --prefix=${HOME}

If you prefer, you can use it without installing, by simply adding
this path to your ``PYTHONPATH`` variable and compiling the extensions::

    $ python setup.py build_ext -i


Licence
=======

New BSD (a.k.a. Modified BSD). See `LICENSE` in this directory for details.


.. _matplotlib: http://matplotlib.sourceforge.net/
.. _example gallery: http://tonysyu.github.com/mpltools/auto_examples/index.html
.. _matplotlibrc: http://matplotlib.sourceforge.net/users/customizing.html
.. _ConfigObj: http://www.voidspace.org.uk/python/configobj.html
.. _mpltools documentation: http://tonysyu.github.com/mpltools
.. _Getting Started: http://tonysyu.github.com/mpltools/getting_started.html
