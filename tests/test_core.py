#!/bin/env python3
from conftl.core import Render
from io import StringIO

instream = StringIO("lorem ipsum {{=i}} text {{=j}} a")
outstream = StringIO()
render = Render(instream, outstream)
print(render.buf)
print([b.data for b in render.buf])
print(render.execstr, end='')
print(outstream.getvalue(), end='')
