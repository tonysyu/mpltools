import os
import glob
import copy

import numpy as np
import matplotlib.pyplot as plt

from .. import _config


__all__ = ['use', 'available', 'lib', 'baselib']


def use(name=None, use_baselib=False):
    """Use matplotlib rc parameters from a pre-defined name or from a file.

    Parameters
    ----------
    name : str or list of str
        Name of style. For list of available styles see `style.available`.
        If given a list, each style is applied from first to last in the list.

    use_baselib : bool
        If True, only use styles defined in `mpltools/style` (without user's
        customization).
    """
    if np.isscalar(name):
        name = [name]
    for s in name:
        if use_baselib:
            plt.rcParams.update(baselib[s])
        else:
            plt.rcParams.update(lib[s])


def load_base_library():
    """Load style library from package"""
    library = dict()
    style_dir = os.path.abspath(os.path.dirname(__file__))
    library.update(read_style_directory(style_dir))
    return library


def read_style_directory(style_dir):
    styles = dict()
    library_glob = os.path.join(style_dir, '*.rc')
    style_files = glob.glob(library_glob)

    for style_path in style_files:
        filename = os.path.basename(style_path)
        cfg = _config.read(style_path)
        # remove last three letters, which are '.rc'
        styles[filename[:-3]] = cfg.dict()

    return styles


def update_user_library(base_library):
    """Update style library with user-defined rc files"""

    library = copy.deepcopy(base_library)


    for cfg in _config.iter_paths(['~/.mplstyle', './mplstyle']):

        # update all styles with any global settings.
        if 'global' in cfg:
            cfg_global = cfg.pop('global')
            for rc_dict in library.itervalues():
                rc_dict.update(cfg_global)

        # update named styles specified by user
        for name, rc_dict in cfg.iteritems():
            if name in library:
                library[name].update(rc_dict)
            else:
                library[name] = rc_dict

    return library


baselib = load_base_library()
lib = update_user_library(baselib)

available = lib.keys()

