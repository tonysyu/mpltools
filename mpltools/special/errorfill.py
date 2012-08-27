import warnings

import numpy as np
import matplotlib.pyplot as plt


__all__ = ['errorfill']


def errorfill(x, y, yerr=None, xerr=None, color=None, ls=None, lw=None,
              alpha=1, alpha_fill=0.3, label='', label_fill='', ax=None):
    """Plot data with errors marked by a filled region.

    Parameters
    ----------
    x, y : arrays
        Coordinates of data.
    yerr, xerr: [scalar | N, (N, 1), or (2, N) array]
        Error for the input data.
        - If scalar, then filled region spans `y +/- yerr` or `x +/- xerr`.
    color : Matplotlib color
        Color of line and fill region.
    ls : Matplotlib line style
        Style of the line
    lw : Matplotlib line width, float value in points
        Width of the line
    alpha : float
        Opacity used for plotting.
    alpha_fill : float
        Opacity of filled region. Note: the actual opacity of the fill is
        `alpha * alpha_fill`.
    label : str
        Label for line.
    label_fill : str
        Label for filled region.
    ax : Axis instance
        The plot is drawn on axis `ax`. If `None` the current axis is used
    """
    ax = ax if ax is not None else plt.gca()

    alpha_fill *= alpha

    if color is None:
        color = ax._get_lines.color_cycle.next()
    if ls is None:
        ls = plt.rcParams['lines.linestyle']
    if lw is None:
        lw = plt.rcParams['lines.linewidth']
    ax.plot(x, y, color, linestyle=ls, linewidth=lw, alpha=alpha, label=label)

    if yerr is not None and xerr is not None:
        msg = "Setting both `yerr` and `xerr` is not supported. Ignore `xerr`."
        warnings.warn(msg)

    kwargs_fill = dict(color=color, alpha=alpha_fill, label=label_fill)
    if yerr is not None:
        ymin, ymax = extrema_from_error_input(y, yerr)
        fill_between(x, ymax, ymin, ax=ax, **kwargs_fill)
    elif xerr is not None:
        xmin, xmax = extrema_from_error_input(x, xerr)
        fill_between_x(y, xmax, xmin, ax=ax, **kwargs_fill)


def extrema_from_error_input(z, zerr):
    if np.isscalar(zerr) or len(zerr) == len(z):
        zmin = z - zerr
        zmax = z + zerr
    elif len(zerr) == 2:
        zmin, zmax = z - zerr[0], z + zerr[1]
    return zmin, zmax


# Wrappers around `fill_between` and `fill_between_x` that create proxy artists
# so that filled regions show up correctly legends.

def fill_between(x, y1, y2=0, ax=None, **kwargs):
    ax = ax if ax is not None else plt.gca()
    ax.fill_between(x, y1, y2, **kwargs)
    ax.add_patch(plt.Rectangle((0, 0), 0, 0, **kwargs))

def fill_between_x(x, y1, y2=0, ax=None, **kwargs):
    ax = ax if ax is not None else plt.gca()
    ax.fill_betweenx(x, y1, y2, **kwargs)
    ax.add_patch(plt.Rectangle((0, 0), 0, 0, **kwargs))


if __name__ == '__main__':
    x = np.linspace(0, 2 * np.pi)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    errorfill(x, y_sin, 0.2)
    errorfill(x, y_cos, 0.2)

    plt.show()
