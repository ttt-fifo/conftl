"""
template decorator
"""
from functools import wraps
from .render_fn import render


class template(object):

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
