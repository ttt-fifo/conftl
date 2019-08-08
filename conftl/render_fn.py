"""
render function
"""
from io import StringIO
from .core import Render


def render(infile=None, outfile=None, context=None, content=None,
           delimiters=None):

    if infile:
        instream = open(infile, 'r')
    elif content:
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
