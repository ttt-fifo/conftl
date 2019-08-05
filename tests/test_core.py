#!/bin/env python3
from conftl.core import Render
from io import StringIO

instream = StringIO("{{True}}")
outstream = StringIO()
render = Render(instream, outstream, context=dict(i=1, j=2))
print(render.buf)
print([b.data for b in render.buf])
print(render.execstr, end='')
print(outstream.getvalue(), end='')
