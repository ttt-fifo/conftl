#!/bin/env python3
import unittest
# from io import StringIO
from conftl.core import Render
import os

if not os.path.isfile('performance.tmpl'):
    with open('performance.tmpl', 'w') as f:
        f.write("""{{
i = 100
}}
""")
        for i in range(0, 30001):
            f.write("""{{if True:}}
{{if i == 100:}}
X text
{{pass}}
i = {{=i}}
{{pass}}
""")


class TestPerformance(unittest.TestCase):
    def testPerf(self):
        with open('performance.tmpl', 'r') as instream:
            with open('performance.out', 'w') as outstream:
                Render(instream, outstream)()


if __name__ == '__main__':
    unittest.main()
