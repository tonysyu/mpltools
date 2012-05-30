import os
import matplotlib.pyplot as plt


def save_all_figs(directory='./', fmt=None, default_name='untitled%i'):
    """Save all open figures.

    Each figure is saved with the title of the plot, if possible.

    Parameters
    ------------
    directory : str
        Path where figures are saved.
    fmt : str, list of str
        Image format(s) of saved figures. If None, default to rc parameter
        'savefig.extension'.
    default_name : str
        Default filename to use if plot has no title. Must contain '%i' for the
        figure number.

    Examples
    --------
    >>> save_all_figs('plots/', fmt=['pdf','png'])

    """
    fmt = fmt if fmt is not None else 'png'
    if isinstance(fmt, basestring):
        fmt = [fmt]

    for fignum in plt.get_fignums():
        try:
            filename = plt.figure(fignum).get_axes()[0].get_title()
        except IndexError:
            continue

        if filename == '':
            filename = default_name % fignum

        savepath = os.path.join(directory, filename)

        for a_fmt in fmt:
            savename = '%s.%s' % (savepath, a_fmt)
            plt.savefig(savename)
            print("Saved '%s'" % savename)

