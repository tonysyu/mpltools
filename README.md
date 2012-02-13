Tools for Matplotlib
====================

As the name implies, `mpltools` provides tools for working with
[matplotlib][1].

Source
------

git@github.com:tonysyu/mpltools.git


Requirements
------------

* [matplotlib][1] (of course)
* [ConfigObj](http://www.voidspace.org.uk/python/configobj.html)


Installation from source
------------------------

The `mpltools` may be installed globally using:

   python setup.py install

or locally using:

   python setup.py install --prefix=${HOME}

If you prefer, you can use it without installing, by simply adding
this path to your `PYTHONPATH` variable and compiling the extensions:

   python setup.py build_ext -i


Licence
-------

Please read `LICENSE` in this directory.


References
----------

[1]: http://matplotlib.sourceforge.net/

