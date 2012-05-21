import numpy as np
import matplotlib.pyplot as plt


__all__ = ['slope_marker']


def slope_marker(origin, slope, invert=False, size_frac=0.1, pad_frac=0.2,
                 text_kwargs=None, poly_kwargs=None, ax=None):
    """Plot triangular slope marker labeled with slope.

    Parameters
    ----------
    origin : 2-tuple
        (x, y) coordinates for the slope.
    slope : float or 2-tuple
        Slope of marker. If float, a single slope label is printed; if tuple,
        you can specify the (rise, run) of the slope and 2 labels are printed.
    invert : bool
        If True, hypotenuse is on the left (i.e. \| or /|).
        If False, hypotenuse is on the right (i.e. |/ or |\).
    size_frac : float
        Fraction of the xaxis length used to determine the size of the slope
        marker. Should be less than 1.
    pad_frac : float
        Fraction of the slope marker size used to pad text labels.
    fontsize : float
        Font size of slope labels.
    text_kwargs : dict
        Keyword arguments passed to `matplotlib.text.Text`.
    poly_kwargs : dict
        Keyword arguments passed to `matplotlib.patches.Polygon`.
    """
    ax = ax if ax is not None else plt.gca()
    text_kwargs = {} if text_kwargs is None else text_kwargs
    poly_kwargs = {} if poly_kwargs is None else poly_kwargs

    if np.iterable(slope):
        rise, run = slope
        slope = float(rise) / run
    else:
        rise = run = None

    x0, y0 = origin
    xlim = ax.get_xlim()
    dx_linear = size_frac * (xlim[1] - xlim[0])
    dx_decades = size_frac * (np.log10(xlim[1]) - np.log10(xlim[0]))

    if invert:
        dx_linear = -dx_linear
        dx_decades = -dx_decades

    if ax.get_xscale() == 'log':
        log_size = dx_decades
        dx = log_displace(x0, log_size) - x0
        x_run = _text_position(x0, log_size/2., scale='log')
        x_rise = _text_position(x0+dx, dx_decades*pad_frac, scale='log')
    else:
        dx = dx_linear
        x_run = _text_position(x0, dx/2.)
        x_rise = _text_position(x0+dx, pad_frac * dx)

    if ax.get_yscale() == 'log':
        log_size = dx_decades * slope
        dy = log_displace(y0, log_size) - y0
        y_run = _text_position(y0, -dx_decades*slope*pad_frac, scale='log')
        y_rise = _text_position(y0, log_size/2., scale='log')
    else:
        dy = dx_linear * slope
        y_run = _text_position(y0, -(pad_frac * dy))
        y_rise = _text_position(y0, dy/2.)

    x_pad = pad_frac * dx
    y_pad = pad_frac * dy

    va = 'top' if y_pad > 0 else 'bottom'
    ha = 'left' if x_pad > 0 else 'right'
    if rise is not None:
        ax.text(x_run, y_run, str(run), va=va, ha='center', **text_kwargs)
        ax.text(x_rise, y_rise, str(rise), ha=ha, va='center', **text_kwargs)
    else:
        ax.text(x_rise, y_rise, str(slope), ha=ha, va='center', **text_kwargs)

    ax.add_patch(_slope_triangle(origin, dx, dy, **poly_kwargs))


def log_displace(x0, dx_log):
    """Return point displaced by a logarithmic value.

    For example, if you want to move 1 decade away from `x0`, set `dx_log` = 1,
    such that for `x0` = 10, we have `log_displace(10, 1)` = 100

    Parameters
    ----------
    x0 : float
        reference point
    dx_log : float
        displacement in decades.
    """
    return 10**(np.log10(x0) + dx_log)


def _text_position(x0, dx, scale='linear'):
    if scale == 'linear':
        return x0 + dx
    elif scale == 'log':
        return log_displace(x0, dx)
    else:
        raise ValueError('Unknown value for `scale`: %s' % scale)


def _slope_triangle(origin, dx, dy, fc='0.8', **poly_kwargs):
    """Return Polygon representing slope.
          /|
         / | dy
        /__|
         dx
    """
    if 'ec' not in poly_kwargs and 'edgecolor' not in poly_kwargs:
        poly_kwargs['edgecolor'] = 'none'
    if 'fc' not in poly_kwargs and 'facecolor' not in poly_kwargs:
        poly_kwargs['facecolor'] = '0.8'
    verts = [np.asarray(origin)]
    verts.append(verts[0] + (dx, 0))
    verts.append(verts[0] + (dx, dy))
    return plt.Polygon(verts, **poly_kwargs)

