import numpy as np
import matplotlib.pyplot as plt

import mpltools


__all__ = ['color_mapper', 'colors_from_cmap', 'cycle_cmap', 'cycle_cmap_axes']


CMAP_RANGE = mpltools.config['color']['cmap_range']


def color_mapper(parameter_range, cmap='YlOrBr', start=0, stop=1):
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
    if isinstance(cmap, basestring):
        cmap = getattr(plt.cm, cmap)
    assert start < stop
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


def colors_from_cmap(length=50, cmap='YlOrBr', start=None, stop=None):
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

    Returns
    -------
    colors : list
        List of RGBA colors.

    See Also
    --------
    `cycle_cmap`, `cycle_cmap_axes`

    """
    if isinstance(cmap, basestring):
        cmap = getattr(plt.cm, cmap)

    crange = CMAP_RANGE.get(cmap.name, (0, 1))
    print crange
    if start is not None:
        crange[0] = start
    if stop is not None:
        crange[1] = stop

    assert 0 <= crange[0] <= 1
    assert 0 <= crange[1] <= 1

    idx = np.linspace(crange[0], crange[1], num=length)
    return cmap(idx)


def cycle_cmap(length=50, cmap='YlOrBr', start=None, stop=None):
    """Set default color cycle of matplotlib based on colormap.

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

    See Also
    --------
    `colors_from_cmap`, `cycle_cmap_axes`

    """
    color_cycle = colors_from_cmap(length, cmap, start, stop)
    # set_default_color_cycle doesn't play nice with numpy arrays
    plt.rc('axes', color_cycle=color_cycle.tolist())


def cycle_cmap_axes(length=50, cmap='YlOrBr', start=None, stop=None, ax=None):
    """Return axes with color cycle set to a given colormap `cmap`.

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

    Returns
    -------
    ax : matplotlib axes
        Axes with new color cycle.

    See Also
    --------
    `colors_from_cmap`, `cycle_cmap`

    """
    ax = ax if ax is not None else plt.gca()
    color_cycle = colors_from_cmap(length, cmap, start, stop)
    # set_default_color_cycle doesn't play nice with numpy arrays
    ax.set_color_cycle(color_cycle)
    return ax


if __name__ == '__main__':
    n_lines = 10
    cycle_cmap(n_lines)
    x = np.linspace(0, 10)
    f, (ax1, ax2) = plt.subplots(ncols=2)
    for shift in np.linspace(0, np.pi, n_lines):
        ax1.plot(x, np.sin(x - shift), linewidth=2)
    ax1.set_title('cycle colormap')

    parameter_range = (0.1, 1)
    #pvalues = np.logspace(parameter_range[0], parameter_range[1], 5)
    pvalues = np.logspace(-1, 0, 5)
    map_color = color_mapper(parameter_range, start=0.1)
    x = np.linspace(0, 10)
    for pval in pvalues:
        y = np.sin(x) * np.exp(-pval * x)
        ax2.plot(x, y, 's', color=map_color(pval))
    ax2.legend(['val = %0.2f' % pval for pval in pvalues])
    ax2.set_title('color based on parameter value')

    plt.show()

