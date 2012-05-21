import os
import glob
import copy

import matplotlib.pyplot as plt

from .. import _config
from configobj import ConfigObj

__all__ = ['use', 'available', 'lib', 'baselib']


def use(name=None, use_baselib=False):
    """Use matplotlib rc parameters from a pre-defined name or from a file.

    Parameters
    ----------
    name : str
        Name of style. For list of styles see `style.available`.

    use_baselib : bool
        If True, only use styles defined in `mpltools/style` (without user's
        customization).
    """
    if use_baselib:
        plt.rcParams.update(baselib[name])
    else:
        plt.rcParams.update(lib[name])


def load_base_library():
    """Load style library from package"""

    library = dict()

    style_dir = os.path.abspath(os.path.dirname(__file__))
    library_glob = os.path.join(style_dir, '*.rc')
    style_files = glob.glob(library_glob)

    for style_path in style_files:
        filename = os.path.basename(style_path)
        cfg = _config.read(style_path)
        # remove last three letters, which are '.rc'
        library[filename[:-3]] = cfg.dict()

    return library


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

def save_param_dict(rc_param_dict, filename):
    """Save a RcParams class or similar dictionary to a style file

    Parameters
    -------------
    rc_param_dict : :class:`matplotlib.RcParams` or dictionary
        rc_params information

    filename : string
        ful path and filename to write config to

    Examples
    --------

    To save current parameters from a ipython -pylab session 

    >>> save_param_dict(rcParams, '/home/user/.mplstyle/my_param.rc')
    
    """
    current_config = ConfigObj(rc_param_dict)
    config_file = open(filename, 'w')
    current_config.write(config_file)
    config_file.close()

    

baselib = load_base_library()
lib = update_user_library(baselib)

available = lib.keys()

