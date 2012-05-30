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
    for fignum in plt.get_fignums():
        try:
            # try to get title of figure(fignum)
            filename = plt.figure(fignum).get_axes()[0].get_title()

            # create filename if title doesnt exist
            if filename == '':
                filename = default_name % fignum

            savename = os.path.join(directory, filename)

            if fmt is None:
                # get default format from rcParams
                fmt = plt.rcParams.get('savefig.extension','png')

            if isinstance(fmt, basestring):
                # force string into list of strings
                fmt = [fmt]

            for a_fmt in fmt:
                plt.savefig(savename + '.' + a_fmt)
                print ('Saved \'%s\' '% (savename + '.' + a_fmt))

        except(IndexError):
            # figure has no axes to get, dont save it
            pass

