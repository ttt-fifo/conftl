"""
Compatibility layer for OS and Python versions
"""
import os
import sys

EOL = os.linesep
PY2 = sys.version_info[0] == 2

if PY2:
    # cStringIO gives unicode error
    # from cStringIO import StringIO
    from StringIO import StringIO

    def _unicod(data):
        typ = type(data)
        if typ == unicode:
            return data
        elif typ == str:
            return data.decode('utf-8')
        else:
            return str(data).decode('utf-8')

else:
    from io import StringIO

    def _unicod(data):
        typ = type(data)
        if typ == str:
            return data
        else:
            return str(data)
