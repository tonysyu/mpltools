import numpy as np
import matplotlib.pyplot as plt


__all__ = ['figure', 'figaspect', 'figimage',
           'clear_frame', 'cross_spines', 'pad_limits']


def figure(aspect_ratio=0.75, scale=1, width=None, **kwargs):
    """Return matplotlib figure window.

    Calculate figure height using `aspect_ratio` and *default* figure width.

    Parameters
    ----------
    aspect_ratio : float
        Aspect ratio, height / width, of figure.
    scale : float
        Scale default size of the figure.
    width : float
        Figure width in inches. If None, default to rc parameters.

    See Also
    --------
    figaspect

    """
    size = figaspect(aspect_ratio, scale=scale, width=width)
    return plt.figure(figsize=size, **kwargs)


def figaspect(aspect_ratio=0.75, scale=1, width=None):
    """Return figure size (width, height) in inches.

    Calculate figure height using `aspect_ratio` and *default* figure width.
    For example, `figaspect(2)` gives a size that's twice as tall as it is
    wide.

    Note that `figaspect` uses the default figure width, or a specified
    `width`, and adjusts the height; this is the opposite of
    `pyplot.figaspect`, which constrains the figure height and adjusts the
    width. This function's behavior is preferred when you have a constraint on
    the figure width (e.g. in a journal article or a web page with a set
    body-width).

    Parameters
    ----------
    aspect_ratio : float
        Aspect ratio, height / width, of figure.
    scale : float
        Scale default size of the figure.
    width : float
        Figure width in inches. If None, default to rc parameters.

    Returns
    -------
    width, height : float
        Width and height of figure.
    """
    if width is None:
        width, h = plt.rcParams['figure.figsize']
    height = width * aspect_ratio
    return width * scale, height * scale


def clear_frame(ax=None):
    """Remove the frame (ticks and spines) from an axes.

    This differs from turning off the axis (`plt.axis('off')` or
    `ax.set_axis_off()`) in that only the ticks and spines are removed. Turning
    off the axis also removes the axes background and axis labels.

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to modify. If None, use current axes.
    """
    ax = ax if ax is not None else plt.gca()

    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    for spine in ax.spines.itervalues():
        spine.set_visible(False)


def figimage(img, scale=1, dpi=None):
    """Return figure and axes with figure tightly surrounding image.

    Unlike pyplot.figimage, this actually plots onto an axes object, which
    fills the figure. Plotting the image onto an axes allows for subsequent
    overlays.

    Parameters
    ----------
    img : array
        image to plot
    scale : float
        If scale is 1, the figure and axes have the same dimension as the
        image.  Smaller values of `scale` will shrink the figure.
    dpi : int
        Dots per inch for figure. If None, use the default rcParam.
    """
    dpi = dpi if dpi is not None else plt.rcParams['figure.dpi']

    h, w = img.shape
    figsize = np.array((w, h), dtype=float) / dpi * scale

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.set_axis_off()
    ax.imshow(img)
    return fig, ax


def cross_spines(zero_cross=False, ax=None):
    """Remove top and right spines from an axes.

    Parameters
    ----------
    zero_cross : bool
        If True, the spines are set so that they cross at zero.
    ax : :class:`~matplotlib.axes.Axes`
        Axes to modify. If None, use current axes.
    """
    ax = ax if ax is not None else plt.gca()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    if zero_cross:
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
    return ax


def pad_limits(pad_frac=0.05, ax=None):
    """Pad data limits to nicely accomodate data.

    Padding is useful when you use markers, which often get cropped by tight
    data limits since only their center-positions are used to calculate limits.

    Parameters
    ----------
    pad_frac : float
        Padding is calculated as a fraction of the data span. `pad_frac = 0`
        is equivalent to calling plt.axis('tight').
    ax : :class:`~matplotlib.axes.Axes`
        Axes to modify. If None, use current axes.
    """
    ax = ax if ax is not None else plt.gca()
    ax.set_xlim(_calc_limits(ax.xaxis, pad_frac))
    ax.set_ylim(_calc_limits(ax.yaxis, pad_frac))


def _calc_limits(axis, frac):
    limits = axis.get_data_interval()
    if axis.get_scale() == 'log':
        log_limits = np.log10(limits)
        mag = np.diff(log_limits)[0]
        pad = np.array([-mag*frac, mag*frac])
        return 10**(log_limits + pad)
    elif axis.get_scale() == 'linear':
        mag = np.diff(limits)[0]
        pad = np.array([-mag*frac, mag*frac])
        return limits + pad

def func_on_all_figs(func, *args, **kwargs):
    """
    runs a function after making all open figures current. 
    
    Parameters
    ----------
    func : function
        function to call
    \*args, \*\*kwargs : pased to func
    
    Examples
    ----------
    >>>rf.func_on_all_figs(grid,alpha=.3)
    """
    for fig_n in plt.get_fignums():
        plt.figure(fig_n)
        func(*args, **kwargs)
        plt.draw()

def save_all_figs(dir = './', format=['eps','pdf','png']):
    """
    Save all open Figures to disk.

    Parameters
    ------------
    dir : string
            path to save figures into
    format : list of strings
            the types of formats to save figures as. The elements of this
            list are passed to :matplotlib:`savefig`. This is a list so that
            you can save each figure in multiple formats.
    """
    if dir[-1] != '/':
        dir = dir + '/'
    for fignum in plb.get_fignums():
        fileName = plb.figure(fignum).get_axes()[0].get_title()
        if fileName == '':
            fileName = 'unamedPlot'
        for fmt in format:
            plb.savefig(dir+fileName+'.'+fmt, format=fmt)
            print (dir+fileName+'.'+fmt)

def add_markers_to_lines(ax=None,marker_list=['o','D','s','+','x'], markevery=10):
    """
    adds markers to all lines of a plot, post facto.
    
    Parameters
    -----------
    ax : matplotlib.Axes
        axis which to add markers to, defaults to gca()
    marker_list : list of marker characters
        see matplotlib.plot help for possible marker characters
    markevery : int
        markevery number of points with a marker.
    
    """
    if ax is None:
        ax=plb.gca()
    lines = ax.get_lines()
    if len(lines) > len (marker_list ):
        marker_list *= 3
    [k[0].set_marker(k[1]) for k in zip(lines, marker_list)]
    [line.set_markevery(markevery) for line in lines]

if __name__ == '__main__':
    from yutils.mpl.core import demo_plot

    f, ax = plt.subplots()
    demo_plot(ax)
    cross_spines(ax)
    ax.set_title('cross_spines')

    f, ax = plt.subplots()
    demo_plot(ax)
    pad_limits(ax=ax)
    ax.set_title('floating_yaxis with pad_limits')

    plt.show()

