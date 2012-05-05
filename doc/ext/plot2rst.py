"""
Example generation from python files.

Generate the rst files for the examples by iterating over the python
example files. Files that generate images should start with 'plot'.

This code was adapted from scikits-image, which took it from scikits-learn.

Options
-------
The ``plot2rst`` extension accepts the following options:

    plot2rst_rcparams : dict
        Matplotlib configuration parameters. See
        http://matplotlib.sourceforge.net/users/customizing.html for details.
"""
import os
import shutil
import traceback
import glob

import matplotlib
matplotlib.use('Agg')

import token, tokenize


EXT = 'rst'
# config paths relative to doc-source directory
GEN_RST_PATH = 'auto_examples'
PY_GALLERY_PATH = '../examples'


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

MULTI_IMAGE_HEADER = """
.. rst-class:: multi-image

"""

MULTI_IMAGE_TEMPLATE = """

      .. image:: images/%s
          :align: center

"""

SINGLE_IMAGE_TEMPLATE = """
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
    app.add_config_value('plot2rst_rcparams', {}, True)


def generate_rst_gallery(app):
    """Add list of examples and gallery to Sphinx app."""
    doc_src = os.path.abspath(app.builder.srcdir) # path/to/doc/source
    rst_dir = os.path.join(doc_src, GEN_RST_PATH)
    example_dir = os.path.join(doc_src, PY_GALLERY_PATH)

    if not os.path.exists(example_dir):
        print "No example directory found at", example_dir
        return
    if not os.path.exists(rst_dir):
        os.makedirs(rst_dir)

    # we create an index.rst with all examples
    gallery_index = file(os.path.join(rst_dir, 'index.' + EXT), 'w')
    gallery_index.write(GALLERY_HEADER)

    cfg = app.builder.config
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
    if not os.path.exists(os.path.join(src_dir, 'index.' + EXT)):
        print src_dir
        print 80*'_'
        print ('Example directory %s does not have a %s file'
                        % (src_dir, 'index.' + EXT))
        print 'Skipping this directory'
        print 80*'_'
        return

    gallery_description = file(os.path.join(src_dir, 'index.' + EXT)).read()
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
    figure_list = save_plot(src_path, image_path, thumb_path, cfg)

    if not os.path.exists(thumb_path):
        # create something to stand in for the thumbnail
        # TODO: figure out a way that doesn't require storing an image.
        #shutil.copy('source/auto_examples/images/blank_image.png', thumb_path)
        pass

    docstring, short_desc, end_row = extract_module_docstring(example_file)
    info['docstring'] = docstring
    info['end_row'] = end_row

    # Depending on whether we have one or more figures, we're using a
    # horizontal list or a single rst call to 'image'.

    if len(figure_list) == 1:
        figure_name = figure_list[0]
        image_list = SINGLE_IMAGE_TEMPLATE % figure_name.lstrip('/')
    else:
        image_list = MULTI_IMAGE_HEADER
        for figure_name in figure_list:
            image_list += MULTI_IMAGE_TEMPLATE % figure_name.lstrip('/')
    info['image_list'] = image_list

    f = open(os.path.join(rst_dir, src_name[:-2] + EXT),'w')
    f.write(plot_rst_template % info)
    f.flush()


def save_plot(src_path, image_path, thumb_path, cfg):
    """Save plots as images.

    Parameters
    ----------
    src_path : str
        Path to example file.
    image_path : str
        Path where plots are saved (format string with single string argument).
    thumbpath : str
        Path where thumbnails of plots are saved.
    cfg : config object
        Sphinx config object created by Sphinx.

    Returns
    -------
    figure_list : list
        List of figure names saved by the example.
    """
    figure_list = []

    src_dir, src_name = os.path.split(src_path)
    if not src_name.startswith('plot'):
        return figure_list

    image_dir, image_fmt_str = os.path.split(image_path)
    first_image_file = image_path % 1

    needs_replot = (not os.path.exists(first_image_file) or
                    mod_time(first_image_file) <= mod_time(src_path))
    if needs_replot:
        print 'plotting %s' % src_name
        import matplotlib.pyplot as plt
        plt.rcdefaults()
        plt.rcParams.update(cfg.plot2rst_rcparams)
        plt.close('all')
        cwd = os.getcwd()
        try:
            # Plot example in source directory.
            os.chdir(src_dir)
            execfile(src_name, {'pl' : plt})
            os.chdir(cwd)

            fig_mngr = matplotlib._pylab_helpers.Gcf.get_all_fig_managers()
            # Save every figure by looping over all open figures.
            for fig_num in (m.num for m in fig_mngr):
                # Set the fig_num figure as the current figure as we can't
                # save a figure that's not the current figure.
                plt.figure(fig_num)
                plt.savefig(image_path % fig_num)
                figure_list.append(image_fmt_str % fig_num)
        except:
            print 80*'_'
            print '%s is not compiling:' % src_name
            traceback.print_exc()
            print 80*'_'
        finally:
            os.chdir(cwd)
    else:
        figure_list = [f[len(image_dir):]
                        for f in glob.glob(image_path % '[1-9]')]

    # generate thumb file
    from matplotlib import image
    if os.path.exists(first_image_file):
        image.thumbnail(first_image_file, thumb_path, 0.2)

    return figure_list

def mod_time(file_path):
    return os.stat(file_path).st_mtime

def extract_module_docstring(src_name):
    """Return module-level docstring.

    Parameters
    ----------
    src_name : str
        Name of python example.

    Returns
    -------
    docstring : str
        Module docstring.
    first_par : str
        First paragraph of docstring.
    end_first_par : int
        Line where first

    """
    lines = file(src_name).readlines()
    start_row = 0
    if lines[0].startswith('#!'):
        lines.pop(0)
        start_row = 1

    docstring = ''
    first_par = ''
    tokens = tokenize.generate_tokens(lines.__iter__().next)
    for tok_type, tok_content, _, (erow, _), _ in tokens:
        tok_type = token.tok_name[tok_type]
        if tok_type in ('NEWLINE', 'COMMENT', 'NL', 'INDENT', 'DEDENT'):
            continue
        elif tok_type == 'STRING':
            docstring = eval(tok_content)
            # Extract the first paragraph of docstring:
            lines = docstring.split('\n')
            clean_docstring = '\n'.join(line.rstrip() for line in lines)
            paragraphs = clean_docstring.split('\n\n')
            if len(paragraphs) > 0:
                first_par = paragraphs[0]
        break
    end_first_par = erow + 1 + start_row
    return docstring, first_par, end_first_par

