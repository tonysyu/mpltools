import matplotlib.pyplot as plt


__all__ = ['figure', 'figsize']


def figure(aspect_ratio=1.3, scale=1, width=None, *args, **kwargs):
    """Return matplotlib figure window.

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


def figsize(aspect_ratio=1.3, scale=1, width=None):
    """Return figure size (width, height) in inches.

    Parameters
    ----------
    aspect_ratio : float
        Aspect ratio, width / height, of figure.
    scale : float
        Scale default size of the figure.
    width : float
        Figure width in inches. If None, default to rc parameters.
    """

    if width is None:
        width, h = plt.rcParams['figure.figsize']
    height = width / aspect_ratio
    size = (width * scale, height * scale)
    return size

