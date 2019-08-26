"""
Function _open_infile(infile, path)
"""
import os
import os.path
from ._compat import _open


def _open_infile(infile, path):
    """
    Searches template file in path and tries to open it
    """

    try:
        return _open(infile, 'r')
    except FileNotFoundError:
        pass

    for p in path:
        try:
            return _open(os.path.join(p, infile), 'r')
        except FileNotFoundError:
            pass

    raise RuntimeError("Cannot find template '%s' in path '%s'" %
                       (infile, ':'.join(path)))
