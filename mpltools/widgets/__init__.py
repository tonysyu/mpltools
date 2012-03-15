import matplotlib.widgets as mwidgets

if not hasattr(mwidgets, 'AxesWidget'):
    branch = "<https://github.com/tonysyu/matplotlib/tree/base-widget>"
    msg = "mpltools.widgets requires a branch of Matplotlib: %s" % branch
    raise ImportError(msg)


from .rectangle_selector import RectangleSelector
from .slider import Slider


__all__ = ['RectangleSelector', 'Slider']

