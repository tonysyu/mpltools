from __future__ import division
from future.builtins import zip
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from ._config import config


__all__ = ['color_mapper', 'colors_from_cmap', 'cycle_cmap', 'LinearColormap']


class LinearColormap(LinearSegmentedColormap):
    """Create Matplotlib colormap with color values specified at key points.

    This class simplifies the call signature of LinearSegmentedColormap. By
    default, colors specified by `color_data` are equally spaced along the
    colormap.

    Parameters
    ----------
    name : str
        Name of colormap.
    color_data : list or dict
        Colors at each index value. Two input types are supported:

            List of RGB or RGBA tuples. For example, red and blue::

                color_data = [(1, 0, 0), (0, 0, 1)]

            Dict of 'red', 'green', 'blue', and (optionally) 'alpha' values.
            For example, the following would give a red-to-blue gradient::

                color_data = {'red': [1, 0], 'green': [0, 0], 'blue': [0, 1]}

    index : list of floats (0, 1)
        Note that these indices must match the length of `color_data`.
        If None, colors in `color_data` are equally spaced in colormap.

    Examples
    --------
    Linear colormap going from white to red

    >>> white_red = LinearColormap('white_red', [(1, 1, 1), (0.8, 0, 0)])

    Colormap going from blue to white to red

    >>> bwr = LinearColormap('blue_white_red', [(0.0, 0.2, 0.4),    # blue
    ...                                         (1.0, 1.0, 1.0),    # white
    ...                                         (0.4, 0.0, 0.1)])   # red

    You can use a repeated index to get a segmented color.
    - Blue below midpoint of colormap, red above mid point.
    - Alpha maximum at the edges, minimum in the middle.

    >>> bcr_rgba = [(0.02, 0.2, 0.4, 1),    # grayish blue, opaque
    ...             (0.02, 0.2, 0.4, 0.3),  # grayish blue, transparent
    ...             (0.4,  0.0, 0.1, 0.3),  # dark red, transparent
    ...             (0.4,  0.0, 0.1, 1)]    # dark red, opaque
    >>> blue_clear_red = color.LinearColormap('blue_clear_red', bcr_rgba,
    ...                                       index=[0, 0.5, 0.5, 1])

    """

    def __init__(self, name, color_data, index=None, **kwargs):
        if not hasattr(color_data, 'keys'):
            color_data = rgb_list_to_colordict(color_data)

        if index is None:
            # If index not given, RGB colors are evenly-spaced in colormap.
            index = np.linspace(0, 1, len(color_data['red']))

        # Adapt color_data to the form expected by LinearSegmentedColormap.
        color_data = dict((key, [(x, y, y) for x, y in zip(index, value)])
                          for key, value in color_data.items())
        LinearSegmentedColormap.__init__(self, name, color_data, **kwargs)


def rgb_list_to_colordict(rgb_list):
    colors_by_channel = list(zip(*rgb_list))
    channels = ('red', 'green', 'blue', 'alpha')
    return dict((color, value)
                for color, value in zip(channels, colors_by_channel))


CMAP_RANGE = config['color']['cmap_range']


def color_mapper(parameter_range, cmap=None, start=None, stop=None):
    """Return color mapper, which returns color based on parameter value.

    Parameters
    ----------
    parameter_range : tuple of floats
        Minimum and maximum value of parameter.

    cmap : str or colormap
        A matplotlib colormap (see matplotlib.pyplot.cm) or the name of one.

    start, stop: 0 <= float <= 1
        Limit colormap to this range (start < stop 1). You should limit the
        range of colormaps with light values (assuming a white background).

    Returns
    -------
    map_color : function
        Function that returns an RGBA color from a parameter value.

    """
    if cmap is None:
        cmap = config['color']['cmap']
    if isinstance(cmap, str):
        cmap = getattr(plt.cm, cmap)

    crange = list(CMAP_RANGE.get(cmap.name, (0, 1)))
    if start is None:
        start = crange[0]
    if stop is None:
        stop = crange[1]

    assert 0 <= start <= 1
    assert 0 <= stop <= 1

    pmin, pmax = parameter_range

    def map_color(val):
        """Return color based on parameter value `val`."""
        assert pmin <= val <= pmax
        val_norm = (val - pmin) * float(stop - start) / (pmax - pmin)
        idx = val_norm + start
        return cmap(idx)

    return map_color


def colors_from_cmap(length=50, cmap=None, start=None, stop=None):
    """Return color cycle from a given colormap.

    Parameters
    ----------
    length : int
        The number of colors in the cycle. When `length` is large (> ~10), it
        is difficult to distinguish between successive lines because successive
        colors are very similar.

    cmap : str
        Name of a matplotlib colormap (see matplotlib.pyplot.cm).

    start, stop: 0 <= float <= 1
        Limit colormap to this range (start < stop 1). You should limit the
        range of colormaps with light values (assuming a white background).
        Some colors have default start/stop values (see `CMAP_RANGE`).

    Returns
    -------
    colors : list
        List of RGBA colors.

    See Also
    --------
    cycle_cmap

    """
    if cmap is None:
        cmap = config['color']['cmap']
    if isinstance(cmap, str):
        cmap = getattr(plt.cm, cmap)

    crange = list(CMAP_RANGE.get(cmap.name, (0, 1)))
    if start is not None:
        crange[0] = start
    if stop is not None:
        crange[1] = stop

    assert 0 <= crange[0] <= 1
    assert 0 <= crange[1] <= 1

    idx = np.linspace(crange[0], crange[1], num=length)
    return cmap(idx)


def cycle_cmap(length=50, cmap=None, start=None, stop=None, ax=None):
    """Set default color cycle of matplotlib based on colormap.

    Note that the default color cycle is **not changed** if `ax` parameter
    is set; only the axes's color cycle will be changed.

    Parameters
    ----------
    length : int
        The number of colors in the cycle. When `length` is large (> ~10), it
        is difficult to distinguish between successive lines because successive
        colors are very similar.

    cmap : str
        Name of a matplotlib colormap (see matplotlib.pyplot.cm).

    start, stop: 0 <= float <= 1
        Limit colormap to this range (start < stop 1). You should limit the
        range of colormaps with light values (assuming a white background).
        Some colors have default start/stop values (see `CMAP_RANGE`).

    ax : matplotlib axes
        If ax is not None, then change the axes's color cycle instead of the
        default color cycle.

    See Also
    --------
    colors_from_cmap, color_mapper

    """
    color_cycle = colors_from_cmap(length, cmap, start, stop)

    if ax is None:
        plt.rc('axes', color_cycle=color_cycle.tolist())
    else:
        ax.set_color_cycle(color_cycle)
