
==========
Contribute
==========

At the moment, this is just a pet project so it's really informal. If you'd
like to contribute something to `mpltools`, just send me a pull request on
github_.


=====
Tasks
=====

Things I'd like to add:

* Infrastructure to build examples into documentation (like `scikits-image
  auto-examples`_).
* Add more styles based on journals.
* A way to support `matplotlibrc`-style config files. Currently `mpltoolsrc`
  and `mplstyle` files are parsed using ConfigObj_, which requires a different
  syntax than `matplotlibrc` files. This isn't a difficult task, but at the
  moment, I don't really care enough to do it.
* Tests!


Coding guidelines
=================

Any code you submit should follow the `PEP 8`_ guidelines and the `Numpy
Documentation Standard`_ as much as possible.


Building the documentation
==========================

The documentation is built using Sphinx_. To build the docs, run the following
in a terminal::

   $ cd /path/to/mpltools/doc
   $ make html

That's it. Sometimes you may need to clean out the cruft that builds up when
source files are deleted. To clean everything out just run::

   $ make clean


.. _github: https://github.com/tonysyu/mpltools

.. _scikits-image auto-examples: http://scikits-image.org/docs/dev/auto_examples/index.html

.. _ConfigObj: http://www.voidspace.org.uk/python/configobj.html

.. _PEP 8: http://www.python.org/dev/peps/pep-0008/

.. _Numpy Documentation Standard: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

.. _Sphinx: http://sphinx.pocoo.org/
