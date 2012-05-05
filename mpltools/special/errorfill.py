import warnings

import numpy as np
import matplotlib.pyplot as plt


__all__ = ['errorfill']


def errorfill(x, y, yerr=None, xerr=None, color=None, alpha=1, alpha_fill=0.3,
              ax=None):
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
    alpha : float
        Opacity used for plotting.
    alpha_fill : float
        Opacity of filled region. Note: the actual opacity of the fill is
        `alpha * alpha_fill`.
    """
    ax = ax if ax is not None else plt.gca()

    alpha_fill *= alpha

    if color is None:
        color = ax._get_lines.color_cycle.next()
        ax.plot(x, y, color, alpha=alpha)

    if yerr is not None and xerr is not None:
        msg = "Setting both `yerr` and `xerr` is not supported. Ignore `xerr`."
        warnings.warn(msg)

    if yerr is not None:
        ymin, ymax = extrema_from_error_input(y, yerr)
        ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill)
    elif xerr is not None:
        xmin, xmax = extrema_from_error_input(x, xerr)
        ax.fill_between_x(y, xmax, xmin, color=color, alpha=alpha_fill)


def extrema_from_error_input(z, zerr):
    if np.isscalar(zerr) or len(zerr) == len(z):
        zmin = z - zerr
        zmax = z + zerr
    elif len(zerr) == 2:
        zmin, zmax = zerr
    return zmin, zmax


if __name__ == '__main__':
    x = np.linspace(0, 2 * np.pi)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    errorfill(x, y_sin, 0.2)
    errorfill(x, y_cos, 0.2)

    plt.show()
