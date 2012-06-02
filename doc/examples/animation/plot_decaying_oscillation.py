#PLOT2RST: auto_plots = False
"""
====================
Decaying oscillation
====================

The animation module provides an ``Animation`` class to clean up the creation
of animated plots. This class is built on top of matplotlib's `animation
subpackage`_, which was introduced in matplotlib v.1.1.

.. _animation subpackage:
    http://matplotlib.sourceforge.net/examples/animation/index.html#animation-examples-index

"""
import numpy as np
import matplotlib.pyplot as plt

from mpltools.animation import Animation


class DecayingOscillation(Animation):

    def __init__(self, L=2*np.pi, npts=100, num_periods=5, decay_rate=0.1):
        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.x = np.linspace(0, L, npts)
        self.num_periods = num_periods
        self.decay_rate = decay_rate
        # Note: If `num_frames` not defined, # of saved frames defaults to 100.
        self.num_frames = 500

    def update(self):
        self.line, = self.ax.plot(self.x, np.sin(self.x))
        tmax = self.num_periods * 2*np.pi
        for t in np.linspace(0, tmax, self.num_frames):
            amplitude = np.exp(-t * self.decay_rate) * np.cos(t)
            self.line.set_ydata(amplitude * np.sin(self.x))
            # must return list of artists if you want to use blit
            yield self.line,


osc = DecayingOscillation()
osc.animate(blit=True)

# Note: `save` and `show` don't play nice together. Use one at a time.
#osc.save('decaying_oscillation.avi', fps=30, bitrate=200)
plt.show()

"""
.. raw:: html

   <video controls="controls">
       <source src="../../_static/decaying_oscillation.webm"
               type="video/webm" />
       Video display requires video tag and webm support.
   </video>

"""
