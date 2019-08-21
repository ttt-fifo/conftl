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
from .defaults import TEMPLATE_PATH
import os
import os.path
standard_library.install_aliases()


def _open_infile(infile, path):
    """
    Searches template file in path and tries to open it
    """

    try:
        return open(infile, 'r')
    except Exception:
        pass

    for p in path:
        try:
            return open(os.path.join(p, infile), 'r')
        except Exception:
            pass

    raise RuntimeError("Cannot find template '%s' in path '%s'" %
                       (infile, ':'.join(path)))


def render(infile=None, outfile=None, context=None, content=None,
           delimiters=None, path=None):
    """
    Function to render a template
    Arguments:
        infile: input template file, if not given arg content= should present
        outfile: output file, if not given the function returns a string
        context: execution context, e.g. variables exported to the template
        content: string with the template, if not given infile= should be given
        delimiters: the tag delimiters, default "{{ }}"
        path: search path for templates. Type: list or str
              Default: ["%s/templates" % os.env["HOME"]].
              Can be changed globally from defaults.py
    Returns:
        returns a string only if outfile=None
        returns None if outfile= is given
    """

    if path:
        if isinstance(path, list):
            template_path = path + TEMPLATE_PATH
        else:
            template_path = path + [TEMPLATE_PATH]
    else:
        template_path = TEMPLATE_PATH

    if infile:
        instream = _open_infile(infile, template_path)
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
