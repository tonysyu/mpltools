import matplotlib.pyplot as plt
import os

def save_all_figs(directory = './', format=['eps','pdf','png'], 
    default_name = 'untitled%i'):
    """
    Save all open Figures to a given directory, possbily in numerous 
    file formats
    
    Parameters
    ------------
    directory : str
        path to save figures into
    format : list of strs
        the types of formats to save figures as. The elements of this
        list are passed to matplotlib's `savefig`. 
    default_name : str
        the default filename to use if plot has no title. must contain 
        a '%i' for the figure number
    
    Examples
    --------
    >>> save_all_figs('plots/', ['pdf','png'])
    
    """
    
    for fignum in plt.get_fignums():
        filename = plt.figure(fignum).get_axes()[0].get_title()
        
        if filename == '':
            filename = default_name % fignum
                
        savename = os.path.join(directory, filename)

        for fmt in format:
            plt.savefig(savename + '.' + fmt)
            print ('Saved \'%s\' '% (savename + '.' + fmt))

