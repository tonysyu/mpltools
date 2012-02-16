
=======
Install
=======

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


