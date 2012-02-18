"""
==========================
Color from parameter value
==========================

Suppose you want to plot a series of curves, and each curve describes
a response to different values of a parameter. ``color_mapper`` returns
a function that maps a parameter value to an RGBA color in a color map.

"""
import numpy as np
import matplotlib.pyplot as plt

import mpltools
from mpltools import color


pvalues = np.logspace(-1, 0, 4)
parameter_range = (pvalues[0], pvalues[-1])
cstart = 0.2
# Pass parameter range so that color mapper knows how to normalize the data.
map_color1 = color.color_mapper(parameter_range)
map_color2 = color.color_mapper(parameter_range, cmap='BuPu', start=cstart)

figsize = mpltools.figsize(aspect_ratio=2)
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=figsize)
x = np.linspace(0, 10)
for pval in pvalues:
    y = np.sin(x) * np.exp(-pval * x)
    ax1.plot(x, y, 's', color=map_color1(pval))
    ax2.plot(x, y, lw=3, color=map_color2(pval))

ax1.legend(['%0.1f' % v for v in pvalues], loc='lower right', ncol=2)
ax1.set_ylim(-1.5, 1.5)

# Hack to get correctly-scaled colorbar
proxy_mappable = plt.cm.ScalarMappable(cmap='BuPu')
map_start = parameter_range[1] - np.diff(parameter_range) / (1. - cstart)
proxy_mappable.set_array(parameter_range)
cbar = fig.colorbar(proxy_mappable, ax=ax2)
cbar.set_clim((map_start, parameter_range[1]))

plt.show()

