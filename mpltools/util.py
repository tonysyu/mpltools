import matplotlib.pyplot as plt


__all__ = ['figure', 'figaspect', 'figsize']


def figure(aspect_ratio=1.3, scale=1, width=None, *args, **kwargs):
    """Return matplotlib figure window.

    Calculate figure height using `aspect_ratio` and *default* figure width.

    Parameters
    ----------
    aspect_ratio : float
        Aspect ratio, width / height, of figure.
    scale : float
        Scale default size of the figure.
    width : float
        Figure width in inches. If None, default to rc parameters.

    See Also
    --------
    figsize

    """
    assert 'figsize' not in kwargs
    size = figsize(aspect_ratio=aspect_ratio, scale=scale, width=width)
    return plt.figure(figsize=size, *args, **kwargs)


def figaspect(aspect_ratio=0.75, scale=1, width=None):
    """Return figure size (width, height) in inches.

    Calculate figure height using `aspect_ratio` and *default* figure width.
    For example, `figsize(2)` gives a size that's twice as tall as it is wide.

    Note that `figsize` uses the default figure width, or a specified `width`,
    and adjusts the height; this is the opposite of `pyplot.figaspect`, which
    constrains the figure height and adjusts the width. This function's
    behavior is preferred when you have a constraint on the figure width
    (e.g. in a journal article or a web page with a set body-width).

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


def figsize(aspect_ratio=1.3, **kwargs):
    from warnings import warn
    msg = ("`figsize` is deprecated; Use `figaspect` instead.\n"
           "(Note that `figaspect` uses inverse definition of aspect ratio)")
    warn(msg)
    return figaspect(1./aspect_ratio, **kwargs)

