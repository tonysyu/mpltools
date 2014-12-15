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
from __future__ import absolute_import

from warnings import warn

from .core import *


warn("""

    The style-sheet functionality in mpltools has been integrated into
    Matplotlib >= 1.4. This module will be removed in a future release.

    Note that style-sheets used by `matplotlib.style` use the standard
    Matplotlib rc-file syntax instead of the INI format used by `mpltools`.
    This mostly means un-quoting strings and changing '=' to ':'.

""", FutureWarning)
