import os
import sys

EOL = os.linesep
PY2 = sys.version_info[0] == 2

if PY2:
    from cStringIO import StringIO
    unicode_ = unicode
else:
    from io import StringIO
    unicode_ = str
