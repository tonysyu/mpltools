import numpy as np
import matplotlib.pyplot as plt

from mpltools.animation import Animation


class DecayingOscillations(Animation):

    def __init__(self, L=2*np.pi, npts=100, noscillations=5, decay_rate=0.1):
        self.fig, self.ax = plt.subplots()
        self.x = np.linspace(0, 2*np.pi, npts)
        self.noscillations = noscillations
        self.decay_rate = decay_rate

    def update(self):
        self.line, = self.ax.plot(self.x, np.sin(self.x))
        tmax = self.noscillations * 2*np.pi
        for t in np.linspace(0, tmax, 100):
            amplitude = np.exp(-t * self.decay_rate) * np.cos(t)
            self.line.set_ydata(amplitude * np.sin(self.x))
            yield self.line, # must return artist if you want to use blit

osc = DecayingOscillations()
osc.animate(blit=True)

plt.show()

