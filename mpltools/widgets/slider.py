import matplotlib.widgets as mwidgets


class Slider(mwidgets.Slider):
    """Slider widget to select a value from a floating point range.

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes` instance
        The parent axes for the widget
    value_range : (float, float)
        (min, max) value allowed for value.
    label : str
        The slider label.
    value : float
        Initial value. If None, set to value in middle of value range.
    on_slide : function
        Callback function for slide event. Function should expect slider value.
    value_fmt : str
        Format string for formatting the slider text.
    slidermin, slidermax : float
        Used to contrain the value of this slider to the values
        of other sliders.
    dragging : bool
        If True, slider is responsive to mouse.
    pad : float
        Padding (in axes coordinates) between `label`/`value_fmt` and slider.

    Attributes
    ----------
    value : float
        Current slider value.

    """

    def __init__(self, ax, value_range, label='', value=None, on_slide=None,
                 value_fmt='%1.2f', slidermin=None, slidermax=None,
                 dragging=True, pad=0.02):

        mwidgets.AxesWidget.__init__(self, ax)

        self.valmin, self.valmax = value_range
        if value is None:
            value = 0.5 * (self.valmin + self.valmax)
        self.val = value
        self.valinit = value
        self.valfmt = value_fmt

        y0 = 0.5
        x_low = [self.valmin, value]
        x_high = [value, self.valmax]

        self.line_low, = ax.plot(x_low, [y0, y0], color='0.5', lw=2)
        self.line_high, = ax.plot(x_high, [y0, y0], color='0.7', lw=2)
        self.val_handle, = ax.plot(value, y0, 'o',
                                   mec='0.4', mfc='0.6', markersize=8)

        ax.set_xlim(value_range)
        ax.set_navigate(False)
        ax.set_axis_off()

        self.connect_event('button_press_event', self._update)
        self.connect_event('button_release_event', self._update)
        if dragging:
            self.connect_event('motion_notify_event', self._update)

        self.label = ax.text(-pad, y0, label, transform=ax.transAxes,
                             verticalalignment='center',
                             horizontalalignment='right')

        self.show_value = False if value_fmt is None else True
        if self.show_value:
            self.valtext = ax.text(1 + pad, y0, value_fmt%value,
                                   transform=ax.transAxes,
                                   verticalalignment='center',
                                   horizontalalignment='left')

        self.slidermin = slidermin
        self.slidermax = slidermax
        self.drag_active  = False

        self.cnt = 0
        self.observers = {}
        if on_slide is not None:
            self.on_changed(on_slide)

        # Attributes for matplotlib.widgets.Slider compatibility
        self.closedmin = self.closedmax = True

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, value):
        self.val = value
        self.line_low.set_xdata([self.valmin, value])
        self.line_high.set_xdata([value, self.valmax])
        self.val_handle.set_xdata([value])
        if self.show_value:
            self.valtext.set_text(self.valfmt % value)

    def set_val(self, value):
        """Set value of slider."""
        # Override matplotlib.widgets.Slider to update graphics objects.

        self.value = value

        if self.drawon:
            self.ax.figure.canvas.draw()
        if not self.eventson:
            return

        for cid, func in self.observers.iteritems():
            func(value)


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    ax = plt.subplot2grid((10, 1), (0, 0), rowspan=8)
    ax_slider = plt.subplot2grid((10, 1), (9, 0))

    a0 = 5
    x = np.arange(0.0, 1.0, 0.001)
    y = np.sin(6 * np.pi * x)

    line, = ax.plot(x, a0 * y, lw=2, color='red')
    ax.axis([x.min(), x.max(), -10, 10])

    def update(val):
        amp = samp.value
        line.set_ydata(amp * y)

    samp = Slider(ax_slider, (0.1, 10.0), on_slide=update,
                  label='Amplitude:', value=a0)

    plt.show()

