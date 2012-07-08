"""
Configuration utilities.
"""
import os
from configobj import ConfigObj


__all__ = ['iter_paths', 'read', 'config']


def iter_paths(config_paths):
    for path in config_paths:
        path = os.path.expanduser(path)

        if not os.path.exists(path):
            continue

        yield read(path)


def read(path):
    """Return dict-like object of config parameters from file path."""
    return ConfigObj(path, unrepr=True)


# Set mpltools specific properties (i.e., not matplotlib properties).
config = {}
pkgdir = os.path.abspath(os.path.dirname(__file__))
for cfg in iter_paths([os.path.join(pkgdir, 'mpltoolsrc'),
                       '~/.mpltoolsrc',
                       './mpltoolsrc']):
    config.update(cfg)


