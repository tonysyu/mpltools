"""
Animation class.

This implementation is a interface for Matplotlib's FuncAnimation class, but
with different interface for:

* Easy reuse of animation code.

* Logical separation of setup parameter (passed to `__init__`) and animation
  parameters (passed to `animate`).

* Unlike Matplotlib's animation class, this Animation class clearly must be
  assigned to a variable (in order to call the `animate` method). The
  FuncAnimation object needs to be assigned to a variable so that it isn't
  garbage-collected, but this requirement is confusing, and easily forgotten,
  because the user never uses the animation object directly.


"""
import matplotlib.animation as _animation


__all__ = ['Animation']


class Animation(object):
    """Base class to create animation objects.

    To create an animation, simply subclass `Animation` and override the
    `__init__` method to create a plot (`self.fig` needs to be assigned to the
    figure object here), and override `update` with a generator that updates
    the plot:

    .. code-block:: python

       class RandomPoints(Animation):

           def __init__(self, width=10):
               self.fig, self.ax = plt.subplots()
               self.width = width
               self.ax.axis([0, width, 0, width])

           def update(self):
               artists = []
               self.ax.lines = [] # Clean up plot when repeating animation.
               for i in np.arange(20):
                   x, y = np.random.uniform(0, self.width, size=2)
                   artists.append(self.ax.plot(x, y, 'ro'))
                   yield artists

       pts = RandomPoints()
       pts.animate()

    Note: if you want to use blitting (see docstring for `Animation.animate`),
    You must yield a sequence of artists in `update`.

    This Animation class does not subclass any of Matplotlib's animation
    classes because the `__init__` method takes arguments for creating the
    plot, while `animate` method is what accepts arguments that alter the
    animation.

    """
    def __init__(self):
        """Initialize plot for animation.

        Replace this method to initialize the plot. The only requirement is
        that you must create a figure object assigned to `self.fig`.
        """
        raise NotImplementedError

    def init_background(self):
        """Initialize background artists.

        Note: This method is passed to `FuncAnimation` as `init_func`.
        """
        pass

    def update(self):
        """Update frame.

        Replace this method to with a generator that updates artists and calls
        an empty `yield` when updates are complete.
        """
        raise NotImplementedError

    def animate(self, **kwargs):
        """Run animation.

        Parameters
        ----------
        interval : float, defaults to 200
            Time delay, in milliseconds, between frames.

        repeat : {True | False}
            If True, repeat animation when the sequence of frames is completed.

        repeat_delay : None
            Delay in milliseconds before repeating the animation.

        blit : {False | True}
            If True, use blitting to optimize drawing. Unsupported by some
            backends.

        init_background : function
            If None, the results of drawing
            from the first item in the frames sequence will be used. This can
            also be added as a class method instead of passing to `animate`.

        save_count : int
            If saving a movie, `save_count` determines number of frames saved.

        """
        reusable_generator = lambda: iter(self.update())
        kwargs['init_background'] = self.init_background
        self._ani = _GenAnimation(self.fig, reusable_generator, **kwargs)


class _GenAnimation(_animation.FuncAnimation):

    def __init__(self, fig, frames, init_background=None, save_count=None,
                 **kwargs):
        self._iter_gen = frames

        self._init_func = init_background
        self.save_count = save_count if save_count is not None else 100

        # Dummy args and function for compatibility with FuncAnimation
        self._args = ()
        self._func = lambda args: args

        self._save_seq = []
        _animation.TimedAnimation.__init__(self, fig, **kwargs)
        # Clear saved seq since TimedAnimation.__init__ adds a single frame.
        self._save_seq = []

