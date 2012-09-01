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
    color_data : dict
        Dictionary of 'red', 'green', 'blue', and (optionally) 'alpha' values.
        Each color key contains a list of `x`, `y` tuples. `x` must increase
        monotonically from 0 to 1 and corresponds to input values for a mappable
        object (e.g. an image). `y` corresponds to the color intensity.
    index : list of floats (0, 1)
        Note that these indices must match the length of `color_data`.
        If None, colors in `color_data` are equally spaced in colormap.

    Examples
    --------
    Linear colormap going from white to red
    >>> white_red = LinearColormap('white_red', {'blue':  [1.0, 0.0],
                                                 'green': [1.0, 0.0],
                                                 'red':   [1.0, 0.8]})

    Colormap going from blue to white to red
    >>> bwr = LinearColormap('white_red',
                             {'blue':  [0.4, 1.0, 0.1],
                              'green': [0.2, 1.0, 0.0],
                              'red':   [0.0, 1.0, 0.4]})

    You can use a repeated index to get a segmented color.
    - Blue below midpoint of colormap, red above mid point.
    - Alpha maximum at the edges, minimum in the middle.
    >>> bcr_spec = {'blue': [0.4, 0.4, 0.1, 0.1],
                    'green': [0.2, 0.2, 0.0, 0.0],
                    'red': [0.02, 0.02, 0.4, 0.4],
                    'alpha': [1, 0.3, 0.3, 1]}
    >>> blue_clear_red = LinearColormap('blue_clear_red', bcr_spec,
                                        index=[0, 0.5, 0.5, 1])
    """

    def __init__(self, name, color_data, index=None, **kwargs):
        if index is None:
            # If index not given, RGB colors are evenly-spaced in colormap.
            index = np.linspace(0, 1, len(color_data['red']))
        # Adapt color_data to the form expected by LinearSegmentedColormap.
        color_data = dict((key, [(x, y, y) for x, y in zip(index, value)])
                          for key, value in color_data.iteritems())
        LinearSegmentedColormap.__init__(self, name, color_data, **kwargs)


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
    if isinstance(cmap, basestring):
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
    if isinstance(cmap, basestring):
        cmap = getattr(plt.cm, cmap)

    crange = CMAP_RANGE.get(cmap.name, (0, 1))
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

