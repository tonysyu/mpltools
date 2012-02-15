"""
Configuration utilities.
"""
import os
from configobj import ConfigObj


def iter_paths(config_paths):
    for path in config_paths:
        path = os.path.expanduser(path)

        if not os.path.exists(path):
            continue

        yield read(path)


def read(path):
    """Return dict-like object of config parameters from file path."""
    return ConfigObj(path, unrepr=True)

