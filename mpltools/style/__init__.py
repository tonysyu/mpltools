"""
This module defines styles redefine matplotlib rc parameters. In addition, you
can override pre-defined styles with "mpltoolsrc" files in the current
directory and your home directory. The priority of style files is:

    1. ./mpltoolsrc
    2. ~/.mpltoolsrc
    3. mpltools/style/

Style names should be specified as sections in "mpltoolsrc" files.  A simple
"mpltoolsrc" file would look like:

    [style1]

    text.fontsize = 12
    figure.dpi = 150

    [style2]

    text.fontsize = 10
    font.family = 'serif'

Note that we use ConfigObj for parsing rc files so, unlike Matplotlib,
key/value pairs are separated by an equals sign and strings must be quoted.

Functions
=========
use
    Redefine rc parameters using specified style.
reset
    Reset rc parameters to matplotlib defaults.
lib
    Style library.
baselib
    Style library defined by mpltools (i.e. before user definitions).
"""

from core import *

