Tools for Matplotlib
====================

As the name implies, `mpltools` provides tools for working with
[matplotlib][1].


Styles
------

A key feature of `mpltools` is the idea of "styles"---essentially stylesheets
that are similar to [matplotlibrc][2] files. Unfortunately, the syntax for
a `mplstyle` file is slightly different than `matplotlibrc` files because
we use [ConfigObj][3] to parse them.

Style names should be specified as sections in "mplstyle" files.  A simple
`mplstyle` file would look like:

    [style1]

    text.fontsize = 12
    figure.dpi = 150

    [style2]

    text.fontsize = 10
    font.family = 'serif'

`mpltools` searches the current working directory and your home directory for
`mplstyle` files. To use a style, you just add:

    >>> import mpltools
    >>> mpltools.style.use('style1')

There are a number of pre-defined styles located in `mpltools/style/`. To list
all available styles, use:

    >>> print mpltools.styles


Requirements
------------

* [matplotlib][1] (of course)
* [ConfigObj][3]


Installation from source
------------------------

`mpltools` may be installed globally using:

    $ git clone git@github.com:tonysyu/mpltools.git
    $ cd mpltools
    $ python setup.py install

or locally using:

    $ python setup.py install --prefix=${HOME}

If you prefer, you can use it without installing, by simply adding
this path to your `PYTHONPATH` variable and compiling the extensions:

    $ python setup.py build_ext -i


Licence
-------

Please read `LICENSE` in this directory.


[1]: http://matplotlib.sourceforge.net/
[2]: http://matplotlib.sourceforge.net/users/customizing.html
[3]: http://www.voidspace.org.uk/python/configobj.html

