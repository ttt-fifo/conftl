"""
template decorator
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from functools import wraps
from .render_fn import render
standard_library.install_aliases()


class template(object):
    """
    Templating Decorator

    Arguments:
        infile:     input template file, if not given content= should be given
        outfile:    output file, if not given, the decorated function will
                    return string
        content:    string with the template, if not given infile=
                    should be given
        delimiters: the tag delimiters, defaulting to "{{ }}"

    Templated function returns:
        string if outfile=None
        None if outfile= is given
    """

    def __init__(self, infile=None, outfile=None, content=None,
                 delimiters=None):

        if not infile and not content:
            raise RuntimeError("infile or content is needed to template")

        self.infile = infile
        self.outfile = outfile
        self.content = content
        self.delimiters = delimiters

    def __call__(self, func):
        @wraps(func)
        def wrapper(*arg, **kwarg):

            context = func(*arg, **kwarg)

            if not isinstance(context, dict):
                raise RuntimeError("Templated function must return dict")

            return render(infile=self.infile,
                          outfile=self.outfile,
                          context=context,
                          content=self.content,
                          delimiters=self.delimiters)
        return wrapper
