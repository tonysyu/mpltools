import matplotlib.pyplot as plt

def save_all_figs(dir = './', format=['eps','pdf','png']):
    """
    Save all open Figures to a given directory, possbily in numerous 
    file formats
    
    Parameters
    ------------
        dir : string
            path to save figures into
        format : list of strings
            the types of formats to save figures as. The elements of this
            list are passed to :matplotlib:`savefig`. 
            
    Examples
    --------
    >>> save_all_figs('plots/', ['pdf','png'])
    
    """
    if dir[-1] != '/':
        dir = dir + '/'
    
    for fignum in plt.get_fignums():
        fileName = plt.figure(fignum).get_axes()[0].get_title()
        if fileName == '':
            fileName = 'unamedPlot'
        for fmt in format:
            plt.savefig(dir+fileName+'.'+fmt, format=fmt)
            print (dir+fileName+'.'+fmt)
