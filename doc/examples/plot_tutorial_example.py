#!/usr/bin/env python
"""
================
Tutorial example
================

Here's a line plot:
"""
import numpy as np
import matplotlib.pyplot as plt

'normal string'

x = np.linspace(0, 2*np.pi)
plt.plot(x, np.sin(x))

def dummy():
    """Dummy docstring"""
    pass

"""
.. image:: PLOT2RST.current_figure

Here's an image plot:
"""
# code comment
plt.figure()
plt.imshow(np.random.random(size=(20, 20)))

"""
.. image:: PLOT2RST.current_figure

# docstring comment
"""

string = """
Triple-quoted string which tries to break parser.
"""
plt.show()

