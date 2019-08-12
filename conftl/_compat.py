"""
Compatibility layer for OS and Python versions
"""
import os
import sys

EOL = os.linesep
PY2 = sys.version_info[0] == 2

if PY2:
    from cStringIO import StringIO
    _unicd = unicode
else:
    from io import StringIO
    _unicd = str
