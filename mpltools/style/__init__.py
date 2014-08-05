"""
This module defines styles that tweak matplotlib rc parameters. In addition,
you can override pre-defined styles with "mplstyle" files in the current
directory and your home directory (`~`). See "Getting Started" in the
``mpltools`` documentation for details.

.. note::

    The functionality in the style module has been integrated into
    Matplotlib 1.4. As a result, this module will be removed in a future
    release.


Functions
=========
use
    Redefine rc parameters using specified style.
lib
    Style library.
baselib
    Style library defined by mpltools (i.e. before user definitions).
"""

from warnings import warn

from core import *


deprecation_msg = ("The style module has been integrated into Matplotlib 1.4. "
                   "This module will be removed in a future release.")
warn(deprecation_msg)
