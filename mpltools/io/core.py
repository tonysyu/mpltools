import matplotlib.pyplot as plt
import os

def save_all_figs(directory = './', fmt = None, 
    default_name = 'untitled%i'):
    """
    Save all open Figures to a given directory, possbily in numerous 
    file formats
    
    Parameters
    ------------
    directory : str
        path to save figures into
    fmt : str, list of strs, or None
        the types of formats to save figures as. The elements of this
        list are passed to matplotlib's `savefig`. see example.
    default_name : str
        the default filename to use if plot has no title. must contain 
        a '%i' for the figure number
    
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
        

