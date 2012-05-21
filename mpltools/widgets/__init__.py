import matplotlib.widgets as mwidgets

if not hasattr(mwidgets, 'AxesWidget'):
    version = "(github master; after March 16, 2012)"
    msg = "mpltools.widgets requires recent version of Matplotlib %s" % version
    raise ImportError(msg)


from .rectangle_selector import RectangleSelector
from .slider import Slider


__all__ = ['RectangleSelector', 'Slider']

