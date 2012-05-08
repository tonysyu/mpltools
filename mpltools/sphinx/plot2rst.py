"""
Example generation from python files.

Generate the rst files for the examples by iterating over the python
example files. Files that generate images should start with 'plot'.

To generate your own examples, just add ``'mpltools.sphinx.plot2rst'``` to the
list of ``extensions``in your Sphinx configuration file.

This code was adapted from scikits-image, which took it from scikits-learn.

Options
-------
The ``plot2rst`` extension accepts the following options:

    plot2rst_paths : length-2 tuple
        Paths to (python plot, generated rst) files, i.e. (source, destination).
        Note that both paths are relative to Sphinx 'source' path.

    plot2rst_rcparams : dict
        Matplotlib configuration parameters. See
        http://matplotlib.sourceforge.net/users/customizing.html for details.

    plot2rst_default_thumb : str
        Path (relative to doc root) of default thumbnail image.

    plot2rst_thumb_scale : float
        Scale factor for thumbnail (e.g., 0.2 to scale plot to 1/5th the
        original size).

"""
import os
import shutil
import traceback
import glob

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


plot_rst_template = """
.. _example_%(short_filename)s:

%(docstring)s

%(image_list)s

**Python source code:** :download:`%(src_name)s <%(src_name)s>`
(generated using ``mpltools`` |version|)

.. literalinclude:: %(src_name)s
    :lines: %(end_row)s-

"""

toctree_template = """
.. toctree::
   :hidden:

   %s

"""


CLEAR_SECTION = """
.. raw:: html

    <div style="clear: both"></div>

"""


IMAGE_TEMPLATE = """
.. image:: images/%s
    :align: center

"""

GALLERY_HEADER = """

Examples
========

.. _examples-index:

"""


def setup(app):
    app.connect('builder-inited', generate_rst_gallery)

    app.add_config_value('plot2rst_paths',
                         ('../examples', 'auto_examples'), True)
    app.add_config_value('plot2rst_rcparams', {}, True)
    app.add_config_value('plot2rst_default_thumb', None, True)
    app.add_config_value('plot2rst_thumb_scale', 0.2, True)
    app.add_config_value('plot2rst_inline_tag', 'PLOT2RST.current_figure', True)

def generate_rst_gallery(app):
    """Add list of examples and gallery to Sphinx app."""
    cfg = app.builder.config

    doc_src = os.path.abspath(app.builder.srcdir) # path/to/doc/source

    plot_path, rst_path = cfg.plot2rst_paths
    rst_dir = os.path.join(doc_src, rst_path)
    example_dir = os.path.join(doc_src, plot_path)

    if not os.path.exists(example_dir):
        print "No example directory found at", example_dir
        return
    if not os.path.exists(rst_dir):
        os.makedirs(rst_dir)

    # we create an index.rst with all examples
    gallery_index = file(os.path.join(rst_dir, 'index'+cfg.source_suffix), 'w')
    gallery_index.write(GALLERY_HEADER)

    # Here we don't use an os.walk, but we recurse only twice: flat is
    # better than nested.
    write_gallery(gallery_index, example_dir, rst_dir, cfg)
    for d in sorted(os.listdir(example_dir)):
        example_sub = os.path.join(example_dir, d)
        if os.path.isdir(example_sub):
            rst_sub = os.path.join(rst_dir, d)
            if not os.path.exists(rst_sub):
                os.makedirs(rst_sub)
            write_gallery(gallery_index, example_sub, rst_sub, cfg, depth=1)
    gallery_index.flush()


def write_gallery(gallery_index, src_dir, rst_dir, cfg, depth=0):
    """Generate the rst files for an example directory, i.e. gallery.

    Write rst files from python examples and add example links to gallery.

    Parameters
    ----------
    gallery_index : file
        Index file for plot gallery.
    src_dir : 'str'
        Source directory for python examples.
    rst_dir : 'str'
        Destination directory for rst files generated from python examples.
    cfg : config object
        Sphinx config object created by Sphinx.
    """
    index_name = 'index' + cfg.source_suffix
    if not os.path.exists(os.path.join(src_dir, index_name)):
        print src_dir
        print 80*'_'
        print ('Example directory %s does not have a %s file'
                        % (src_dir, index_name))
        print 'Skipping this directory'
        print 80*'_'
        return

    gallery_description = file(os.path.join(src_dir, index_name)).read()
    gallery_index.write('\n\n%s\n\n' % gallery_description)

    if not os.path.exists(rst_dir):
        os.makedirs(rst_dir)

    def sort_key(a):
        # Elements that are not plots should be last.
        if not valid_plot_script(a):
            return 'zz' + a
        return a

    examples = [fname for fname in sorted(os.listdir(src_dir), key=sort_key)
                      if fname.endswith('py')]
    ex_names = [ex[:-3] for ex in examples] # strip '.py' extension
    if depth == 0:
        sub_dir = ''
    else:
        sub_dir_list = src_dir.split('/')[-depth:]
        sub_dir = '/'.join(sub_dir_list) + '/'
    gallery_index.write(toctree_template % (sub_dir + '\n   '.join(ex_names)))

    write = gallery_index.write
    for src_name in examples:
        rst_file_from_example(src_name, src_dir, rst_dir, cfg)
        thumb = os.path.join(sub_dir, 'images/thumb', src_name[:-3] + '.png')
        gallery_index.write('.. figure:: %s\n' % thumb)

        link_name = sub_dir + src_name
        link_name = link_name.replace(os.path.sep, '_')
        if link_name.startswith('._'):
            link_name = link_name[2:]

        write('   :figclass: gallery\n')
        write('   :target: ./%s.html\n\n' % (sub_dir + src_name[:-3]))
        write('   :ref:`example_%s`\n\n' % (link_name))
    write(CLEAR_SECTION) # clear at the end of the section


def valid_plot_script(src_name):
    return src_name.startswith('plot') and src_name.endswith('.py')


def rst_file_from_example(src_name, src_dir, rst_dir, cfg):
    """Write rst file from a given python example.

    Parameters
    ----------
    src_name : str
        Name of example file.
    src_dir : 'str'
        Source directory for python examples.
    rst_dir : 'str'
        Destination directory for rst files generated from python examples.
    cfg : config object
        Sphinx config object created by Sphinx.
    """
    base_image_name = os.path.splitext(src_name)[0]
    image_fmt_str = '%s_%%s.png' % base_image_name

    last_dir = os.path.split(src_dir)[-1]
    # to avoid leading . in file names, and wrong names in links
    if last_dir == '.' or last_dir == 'examples':
        last_dir = ''
    else:
        last_dir += '_'

    info = dict(src_name=src_name)
    info['short_filename'] = last_dir + src_name
    src_path = os.path.join(src_dir, src_name)
    example_file = os.path.join(rst_dir, src_name)
    shutil.copyfile(src_path, example_file)

    image_dir = os.path.join(rst_dir, 'images')
    thumb_dir = os.path.join(image_dir, 'thumb')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_path = os.path.join(thumb_dir, src_name[:-3] + '.png')
    image_path = os.path.join(image_dir, image_fmt_str)

    blocks = split_code_and_text(example_file)

    plot_inline = any(b for b in blocks if cfg.plot2rst_inline_tag in b[2])
    if plot_inline:
        pass
    else:
        first_text_block = [b for b in blocks if b[0] == 'text'][0]
        label, (start, end), content = first_text_block
        info['docstring'] = content.strip().strip('"""')
        info['end_row'] = end + 1
        figure_list = save_plot(src_path, image_path, thumb_path, cfg)

        rst_blocks = [IMAGE_TEMPLATE % f.lstrip('/') for f in figure_list]
        info['image_list'] = ''.join(rst_blocks)

        basename, py_ext = os.path.splitext(src_name)
        f = open(os.path.join(rst_dir, basename + cfg.source_suffix),'w')
        f.write(plot_rst_template % info)
        f.flush()


    if not os.path.exists(thumb_path):
        if cfg.plot2rst_default_thumb is None:
            print "WARNING: No plots found and default thumbnail not defined."
            print "Specify 'plot2rst_default_thumb' in Sphinx config file."
        else:
            shutil.copy(cfg.plot2rst_default_thumb, thumb_path)

def split_code_and_text(source_file):
    """Return list with source file separated into code and text blocks.

    Returns
    -------
    blocks : list of (label, (start, end+1), content)
        List where each element is a tuple with the label ('text' or 'code'),
        the (start, end+1) line numbers, and content string of block.
    """
    with open(source_file) as f:
        source_lines = f.readlines()
    blocks = []
    i = 0
    last_line = len(source_lines)
    while True:
        if start_of_text(source_lines[i]):
            label = 'text'
            token = source_lines[i][:3] + '\n' # either """\n or '''\n
            j = _end_index(i, lambda k: source_lines[k].endswith(token))
            j += 1 # set j to line after text block
        else:
            label = 'code'
            j = _end_index(i, lambda k: start_of_text(source_lines[k]))
        # Add 1 to convert list indices to line numbers, which start at 1.
        blocks.append((label, (i+1, j+1), ''.join(source_lines[i:j])))
        i = j
        if i == last_line:
            break
    return blocks


def _end_index(i, stop_condition):
    j = i
    while True:
        j += 1
        try:
            if stop_condition(j):
                return j
        except IndexError:
            return j


def start_of_text(line):
    return line.startswith('"""') or line.startswith("'''")


def save_plot(src_path, image_path, thumb_path, cfg):
    """Save plots as images.

    Parameters
    ----------
    src_path : str
        Path to example file.
    image_path : str
        Path where plots are saved (format string which accepts figure number).
    thumbpath : str
        Path where thumbnails of plots are saved.
    cfg : config object
        Sphinx config object created by Sphinx.

    Returns
    -------
    figure_list : list
        List of figure names saved by the example.
    """

    src_dir, src_name = os.path.split(src_path)
    if not src_name.startswith('plot'):
        return []

    image_dir, image_fmt_str = os.path.split(image_path)
    first_image_file = image_path % 1

    needs_replot = (not os.path.exists(first_image_file) or
                    mod_time(first_image_file) <= mod_time(src_path))
    if needs_replot:
        print 'plotting %s' % src_name
        plt.rcdefaults()
        plt.rcParams.update(cfg.plot2rst_rcparams)
        plt.close('all')

        exec_source_in_dir(src_name, src_dir)
        figure_list = save_all_figures(image_path)
    else:
        figure_list = [f[len(image_dir):]
                        for f in glob.glob(image_path % '[1-9]')]

    # generate thumb file
    from matplotlib import image
    if os.path.exists(first_image_file):
        image.thumbnail(first_image_file, thumb_path, cfg.plot2rst_thumb_scale)

    return figure_list


def exec_source_in_dir(source_file, source_path):
    """Execute source file in source directory and capture & print errors."""
    cwd = os.getcwd()
    try:
        # Plot example in source directory.
        os.chdir(source_path)
        execfile(source_file, {})
    except:
        print 80*'_'
        print '%s is not compiling:' % source_file
        traceback.print_exc()
        print 80*'_'
    finally:
        os.chdir(cwd)


def save_all_figures(image_path):
    """Save all matplotlib figures.

    Parameters
    ----------
    image_path : str
        Path where plots are saved (format string which accepts figure number).
    """
    figure_list = []
    image_dir, image_fmt_str = os.path.split(image_path)
    fig_mngr = matplotlib._pylab_helpers.Gcf.get_all_fig_managers()
    for fig_num in (m.num for m in fig_mngr):
        # Set the fig_num figure as the current figure as we can't
        # save a figure that's not the current figure.
        plt.figure(fig_num)
        plt.savefig(image_path % fig_num)
        figure_list.append(image_fmt_str % fig_num)
    return figure_list


def mod_time(file_path):
    return os.stat(file_path).st_mtime

