import functools
import warnings

from . import layout


__all__ = ['deprecated', 'figure', 'figaspect', 'figsize']


class deprecated(object):
    """Decorator to mark deprecated functions with warning.

    Adapted from <http://wiki.python.org/moin/PythonDecoratorLibrary>.

    Parameters
    ----------
    alt_func : str
        If given, tell user what function to use instead.
    behavior : {'warn', 'raise'}
        Behavior during call to deprecated function: 'warn' = warn user that
        function is deprecated; 'raise' = raise error.
    """

    def __init__(self, alt_func=None, behavior='warn'):
        self.alt_func = alt_func
        self.behavior = behavior

    def __call__(self, func):

        msg = "Call to deprecated function `%s`." % func.__name__
        if self.alt_func is not None:
            msg = msg + " Use `%s` instead." % self.alt_func

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if self.behavior == 'warn':
                warnings.warn_explicit(msg,
                    category=DeprecationWarning,
                    filename=func.func_code.co_filename,
                    lineno=func.func_code.co_firstlineno + 1)
            elif self.behavior == 'raise':
                raise DeprecationWarning(msg)
            return func(*args, **kwargs)

        return wrapped


@deprecated('layout.figure')
def figure(aspect_ratio=1.3, **kwargs):
    print "NOTE: `layout.figure` uses inverse definition of `aspect_ratio`."
    aspect_ratio = 1.0 / aspect_ratio
    return layout.figure(aspect_ratio, **kwargs)


@deprecated('layout.figaspect')
def figaspect(*args, **kwargs):
    return layout.figaspect(*args, **kwargs)


@deprecated('layout.figaspect')
def figsize(aspect_ratio=1.3, **kwargs):
    print "NOTE: `layout.figaspect` uses inverse definition of `aspect_ratio`."
    return layout.figaspect(1./aspect_ratio, **kwargs)

