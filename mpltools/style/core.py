import os
import glob
import copy

from configobj import ConfigObj
import matplotlib.pyplot as plt


__all__ = ['use', 'lib', 'baselib']


def use(name=None, use_baselib=False):
    """Use matplotlib rc parameters from a pre-defined name or from a file."""
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
        cfg = ConfigObj(style_path, unrepr=True)
        # remove last three letters, which are '.rc'
        library[filename[:-3]] = cfg.dict()

    return library


def update_user_library(base_library):
    """Update style library with user-defined rc files"""

    library = copy.deepcopy(base_library)

    rc_paths = [os.path.expanduser('~/.mpltoolsrc'),
                './mpltoolsrc']
    for path in rc_paths:

        if not os.path.exists(path):
            continue

        cfg = ConfigObj(path, unrepr=True)

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

