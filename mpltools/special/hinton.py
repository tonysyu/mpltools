import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import matplotlib.transforms as transforms


__all__ = ['hinton']


# TOOD: Add yutils.mpl._coll to mpltools and use that for square collection.
class SquareCollection(collections.RegularPolyCollection):
    """Return a collection of squares."""

    def __init__(self, **kwargs):
        super(SquareCollection, self).__init__(4, rotation=np.pi/4., **kwargs)

    def get_transform(self):
        """Return transform scaling circle areas to data space."""
        ax = self.axes
        pts2pixels = 72.0 / ax.figure.dpi
        scale_x = pts2pixels * ax.bbox.width / ax.viewLim.width
        scale_y = pts2pixels * ax.bbox.height / ax.viewLim.height
        return transforms.Affine2D().scale(scale_x, scale_y)


def hinton(inarray, max_value=None):
    """Plot Hinton diagram for visualizing the values of a 2D array.

    Plot representation of an array with positive and negative values
    represented by white and black squares, respectively. The size of each
    square represents the magnitude of each value.

    Unlike the hinton demo in the matplotlib gallery [1]_, this implementation
    uses a RegularPolyCollection to draw squares, which is much more efficient
    than drawing individual Rectangles.

    .. [1] http://matplotlib.sourceforge.net/examples/api/hinton_demo.html

    Parameters
    ----------
    inarray : array
        Array to plot.
    max_value : float
        Any *absolute* value larger than `max_value` will be represented by a
        unit square.
    """
    ax = plt.gca()
    ax.set_axis_bgcolor('gray')
    # make sure we're working with a numpy array, not a numpy matrix
    inarray = np.asarray(inarray)
    height, width = inarray.shape
    if max_value is None:
        max_value = 2**np.ceil(np.log(np.max(np.abs(inarray)))/np.log(2))
    values = np.clip(inarray/max_value, -1, 1)
    rows, cols = np.mgrid[:height, :width]

    pos = np.where(values > 0)
    neg = np.where(values < 0)
    for idx, color in zip([pos, neg], ['white', 'black']):
        if len(idx[0]) > 0:
            xy = zip(cols[idx], rows[idx])
            circle_areas = np.pi / 2 * np.abs(values[idx])
            squares = SquareCollection(sizes=circle_areas,
                                       offsets=xy, transOffset=ax.transData,
                                       facecolor=color, edgecolor=color)
            ax.add_collection(squares, autolim=True)

    ax.axis('scaled')
    # set data limits instead of using xlim, ylim.
    ax.set_xlim(-0.5, width-0.5)
    ax.set_ylim(height-0.5, -0.5)
    # reimplement ticks using a locator object.
    ax.set_xticks(np.arange(width))
    ax.set_yticks(np.arange(height))
    ax.set_xlabel('column')
    ax.set_ylabel('row')
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')


if __name__ == '__main__':
    A = np.random.uniform(-1, 1, size=(20, 20))
    hinton(A)
    plt.show()

