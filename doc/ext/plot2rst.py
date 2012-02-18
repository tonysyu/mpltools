"""
Example generation for the mpltools.

Generate the rst files for the examples by iterating over the python
example files. Files that generate images should start with 'plot'.

This code was taken from scikits-image, which took it from scikits-learn.

Options
-------
The ``gen_plot_rst`` extension accepts the following options:

    plot2rst_add_gallery : bool
        If true, generate gallery from python examples.
"""
import os
import shutil
import traceback
import glob

import matplotlib
matplotlib.use('Agg')

import token, tokenize


EXT = 'rst'
INDEX = 'index.rst'
# config paths relative to doc-source directory
GEN_RST_PATH = 'auto_examples'
PY_GALLERY_PATH = '../examples'


rst_template = """

.. _example_%(short_filename)s:

%(docstring)s

**Python source code:** :download:`%(src_name)s <%(src_name)s>`
(generated using ``mpltools`` |version|)

.. literalinclude:: %(src_name)s
    :lines: %(end_row)s-
    """

plot_rst_template = """

.. _example_%(short_filename)s:

%(docstring)s

%(image_list)s

**Python source code:** :download:`%(src_name)s <%(src_name)s>`
(generated using ``mpltools`` |version|)

.. literalinclude:: %(src_name)s
    :lines: %(end_row)s-
    """


CLEAR_SECTION = """
.. raw:: html

    <div style="clear: both"></div>
"""


# The following strings are used when we have several pictures: we use
# an html div tag that our CSS uses to turn the lists into horizontal
# lists.


HLIST_HEADER = """
.. rst-class:: horizontal

"""

HLIST_IMAGE_TEMPLATE = """
    *

      .. image:: images/%s
            :scale: 50
"""

SINGLE_IMAGE = """
.. image:: images/%s
    :align: center
"""

GALLERY_HEADER = """

.. raw:: html

    <style type="text/css">
    .figure {
        float: left;
        margin: 1em;
    }

    .figure img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 200px;
    }

    .figure .caption {
        width: 200px;
        text-align: center !important;
    }
    </style>

Examples
========

.. _examples-index:
"""


def setup(app):
    app.connect('builder-inited', generate_rst_gallery)
    app.add_config_value('plot2rst_add_gallery', True, True)
    app.add_config_value('plot2rst_rcparams', {}, True)


def generate_rst_gallery(app):
    """Add list of examples and gallery to Sphinx app."""
    rst_dir = os.path.join(app.builder.srcdir, GEN_RST_PATH)
    example_dir = os.path.abspath(app.builder.srcdir + '/' + PY_GALLERY_PATH)

    cfg = app.builder.config

    if not os.path.exists(example_dir):
        os.makedirs(example_dir)
    if not os.path.exists(rst_dir):
        os.makedirs(rst_dir)

    # we create an index.rst with all examples
    gallery_index = file(os.path.join(rst_dir, INDEX), 'w')
    gallery_index.write(GALLERY_HEADER)
    # Here we don't use an os.walk, but we recurse only twice: flat is
    # better than nested.
    write_gallery(gallery_index, example_dir, rst_dir, cfg)
    for d in sorted(os.listdir(example_dir)):
        if os.path.isdir(os.path.join(example_dir, d)):
            write_gallery(d, gallery_index, example_dir, rst_dir, cfg)
    gallery_index.flush()


def write_gallery(gallery_index, src_dir, rst_dir, cfg):
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
    if not os.path.exists(os.path.join(src_dir, INDEX)):
        print src_dir
        print 80*'_'
        print ('Example directory %s does not have a %s file'
                        % (src_dir, INDEX))
        print 'Skipping this directory'
        print 80*'_'
        return

    readme_file = file(os.path.join(src_dir, INDEX)).read()
    gallery_index.write("""\n\n\n%s\n\n\n""" % readme_file)

    if not os.path.exists(rst_dir):
        os.makedirs(rst_dir)

    def sort_key(a):
        # Elements that are not plots should be last.
        if not valid_plot_script(a):
            return 'zz' + a
        return a

    for src_name in sorted(os.listdir(src_dir), key=sort_key):
        if src_name.endswith('py'):
            rst_file_from_example(src_name, src_dir, rst_dir, cfg)
            thumb = os.path.join('images/thumb', src_name[:-3] + '.png')
            gallery_index.write('.. figure:: %s\n' % thumb)

            link_name = src_name.replace(os.path.sep, '_')
            if link_name.startswith('._'):
                link_name = link_name[2:]

            gallery_index.write('   :figclass: gallery\n')
            gallery_index.write('   :target: ./%s.html\n\n' % src_name[:-3])
            gallery_index.write('   :ref:`example_%s`\n\n' % link_name)
    gallery_index.write(CLEAR_SECTION) # clear at the end of the section


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

    this_template = rst_template
    last_dir = os.path.split(src_dir)[-1]
    # to avoid leading . in file names, and wrong names in links
    if last_dir == '.' or last_dir == 'examples':
        last_dir = ''
    else:
        last_dir += '_'
    short_filename = last_dir + src_name
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

    if cfg.plot2rst_add_gallery:
        figure_list = save_plot(src_path, image_path, thumb_path)
        this_template = plot_rst_template
    else:
        figure_list = []

    if not os.path.exists(thumb_path):
        # create something not to replace the thumbnail
        shutil.copy('source/auto_examples/images/blank_image.png', thumb_path)

    docstring, short_desc, end_row = extract_module_docstring(example_file)

    # Depending on whether we have one or more figures, we're using a
    # horizontal list or a single rst call to 'image'.

    if len(figure_list) == 1:
        figure_name = figure_list[0]
        image_list = SINGLE_IMAGE % figure_name.lstrip('/')
    else:
        image_list = HLIST_HEADER
        for figure_name in figure_list:
            image_list += HLIST_IMAGE_TEMPLATE % figure_name.lstrip('/')

    f = open(os.path.join(rst_dir, src_name[:-2] + EXT),'w')
    f.write(this_template % locals())
    f.flush()


def save_plot(src_path, image_path, thumb_path):
    """Save plots as images.

    Parameters
    ----------
    src_path : str
        Path to example file.
    image_path : str
        Path where plots are saved (format string with single string argument).
    thumbpath : str
        Path where thumbnails of plots are saved.

    Returns
    -------
    figure_list : list
        List of figure names saved by the example.
    """
    src_name = os.path.basename(src_path)
    image_dir, image_fmt_str = os.path.split(image_path)
    figure_list = []
    if src_name.startswith('plot'):
        # generate the plot as png image if file name starts with plot and if
        # it is more recent than an existing image.
        first_image_file = image_path % 1

        if (not os.path.exists(first_image_file) or
            mod_time(first_image_file) <= mod_time(src_path)):
            # We need to execute the code
            print 'plotting %s' % src_name
            import matplotlib.pyplot as plt
            plt.close('all')
            cwd = os.getcwd()
            try:
                # First CD in the original example dir, so that any file
                # created by the example get created in this directory
                os.chdir(os.path.dirname(src_path))
                execfile(os.path.basename(src_path), {'pl' : plt})
                os.chdir(cwd)

                fig_mngr = matplotlib._pylab_helpers.Gcf.get_all_fig_managers()
                # In order to save every figure we have two solutions :
                # * iterate from 1 to infinity and call plt.fignum_exists(n)
                #   (this requires the figures to be numbered
                #    incrementally: 1, 2, 3 and not 1, 2, 5)
                # * iterate over [fig_mngr.num for fig_mngr in
                #   matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
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
                            #for f in glob.glob(image_path % '*')]

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

