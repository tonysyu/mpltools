"""
Save test plots for all styles defined in `mpltools.style`.

Note that `test_artists_plot` calls `matplotlib.pyplot.tight_layout` so subplot
spacing is not tested for this plot.
"""

import os
import os.path as pth

import numpy as np
import matplotlib.pyplot as plt

import mpltools


PATH = pth.abspath(pth.dirname(__file__))

TEST_DIRS = ('test_artists_png', 'test_artists_pdf',
            'test_simple_png', 'test_simple_pdf')
for d in TEST_DIRS:
    test_dir = pth.join(PATH, d)
    if not pth.exists(test_dir):
        os.mkdir(test_dir)


def test_artists_plot():
    fig, axes = plt.subplots(2, 2)
    axes = axes.ravel()

    x = np.linspace(0, 1)
    axes[0].plot(x, np.sin(2*np.pi*x), label='line')
    c = plt.Circle((0.25, 0), radius=0.1, label='patch')
    axes[0].add_patch(c)
    axes[0].grid()
    axes[0].legend()

    axes[1].imshow(np.random.random(size=(20, 20)))
    axes[1].set_title('image')

    ncolors = len(plt.rcParams['axes.color_cycle'])
    phi = np.linspace(0, 2*np.pi, ncolors + 1)[:-1]
    for p in phi:
        axes[2].plot(x, np.sin(2*np.pi*x + p))
    axes[2].set_title('color cycle')

    axes[3].text(0, 0, 'hello world')
    axes[3].set_xlabel('x-label')
    axes[3].set_ylabel('y-label')
    axes[3].set_title('title')

    plt.tight_layout()
    return fig

def test_simple_plot():
    fig, ax = plt.subplots()

    ax.plot([0, 1])
    ax.set_xlabel('x-label')
    ax.set_ylabel('y-label')
    ax.set_title('title')

    return fig


for style in mpltools.styles:
    mpltools.style.use(style, use_baselib=True)
    print "Plotting tests for '%s' style" % style

    fig = test_artists_plot()
    fig.savefig(pth.join(PATH, 'test_artists_png', style + '.png'))
    fig.savefig(pth.join(PATH, 'test_artists_pdf', style + '.pdf'))

    fig = test_simple_plot()
    fig.savefig(pth.join(PATH, 'test_simple_png', style + '.png'))
    fig.savefig(pth.join(PATH, 'test_simple_pdf', style + '.pdf'))

