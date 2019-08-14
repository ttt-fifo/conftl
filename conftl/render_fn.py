"""
render function
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
from .core import Render
from ._compat import _unicod
from ._compat import StringIO
# from ._compat import _open
standard_library.install_aliases()


def render(infile=None, outfile=None, context=None, content=None,
           delimiters=None):
    """
    Function to render a template
    Arguments:
        infile: input template file, if not given arg content= should present
        outfile: output file, if not given the function returns a string
        context: execution context, e.g. variables exported to the template
        content: string with the template, if not given infile= should be given
        delimiters: the tag delimiters, default "{{ }}"
    Returns:
        returns a string only if outfile=None
        returns None if outfile= is given
    """

    if infile:
        instream = open(infile, 'r')
    elif content:
        content = _unicod(content)
        instream = StringIO(content)
        del content
    else:
        raise RuntimeError("infile or content is needed to render")

    if outfile:
        outstream = open(outfile, 'w')
    else:
        outstream = StringIO()

    Render(instream, outstream, context, delimiters)()

    if infile:
        instream.close()

    if outfile:
        outstream.close()
    else:
        return outstream.getvalue()
