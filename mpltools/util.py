import matplotlib.pyplot as plt


__all__ = ['figure', 'figsize']


def figure(aspect_ratio=1.3, scale=1, *args, **kwargs):
    """Return matplotlib figure window.

    Parameters
    ----------
    aspect_ratio : float
        Aspect ratio, width / height, of figure.
    scale : float
        Scale default size of the figure.

    See Also
    --------
    `figsize`

    """
    assert 'figsize' not in kwargs
    size = figsize(aspect_ratio=aspect_ratio, scale=scale)
    return plt.figure(figsize=size, *args, **kwargs)


def figsize(aspect_ratio=1.3, scale=1):
    """Return figure size (width, height) in inches.

    Parameters
    ----------
    aspect_ratio : float
        Aspect ratio, width / height, of figure.
    scale : float
        Scale default size of the figure.
    """

    width, h = plt.rcParams['figure.figsize']
    height = width / aspect_ratio
    size = (width * scale, height * scale)
    return size

