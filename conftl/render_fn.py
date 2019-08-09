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
from ._compat import unicode_
from ._compat import StringIO
standard_library.install_aliases()


def render(infile=None, outfile=None, context=None, content=None,
           delimiters=None):

    if infile:
        instream = open(infile, 'r')
    elif content:
        content = unicode_(content)
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
