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


def update_user_library(base_library):
    """Update style library with user-defined rc files"""

    library = copy.deepcopy(base_library)

    stylelib_path = os.path.expanduser('~/.mplstylelib')
    if os.path.exists(stylelib_path) and os.path.isdir(stylelib_path):
        styles = read_style_directory(stylelib_path)
        update_nested_dict(library, styles)

    for cfg in _config.iter_paths(['~/.mplstyle', './mplstyle']):
        styles = read_style_dict(cfg)
        update_nested_dict(library, styles)
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


def read_style_dict(cfg):
    """Return dict of styles read from config dict.

    Sections in style file are set as top-level keys of the returned dict.
    """
    style = {}
    # update all settings with any global settings.
    if 'global' in cfg:
        cfg_global = cfg.pop('global')
        for rc_dict in style.itervalues():
            rc_dict.update(cfg_global)
    return update_nested_dict(style, cfg)


def update_nested_dict(main_dict, new_dict):
    """Update nested dict (only level of nesting) with new values.


    Unlike dict.update, this assumes that the values of the parent dict are
    dicts, so you shouldn't replace the nested dict if it already exists.
    Instead you should update the sub-dict.
    """
    # update named styles specified by user
    for name, rc_dict in new_dict.iteritems():
        if name in main_dict:
            main_dict[name].update(rc_dict)
        else:
            main_dict[name] = rc_dict
    return main_dict


# Load style libraries
# ====================
baselib = load_base_library()
lib = update_user_library(baselib)
available = lib.keys()

