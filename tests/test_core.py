#!/bin/env python3
import unittest
from io import StringIO
from conftl.core import Delimiters
from conftl.core import OutcodeText
from conftl.core import InCode
from conftl.core import Render


class TestCore(unittest.TestCase):

    def testDelimiters(self):
        delimiters = Delimiters("{{ }}")
        self.assertEqual(delimiters.start, '{{')
        self.assertEqual(delimiters.end, '}}')

    def testOutcodeText(self):
        outstream = StringIO()
        otxt = OutcodeText(outstream)
        otxt += "lorem ipsum dolor sim amet"
        self.assertEqual(outstream.getvalue(), "lorem ipsum dolor sim amet")

    def testInCode(self):
        outstream = StringIO()
        incode = InCode(outstream, Delimiters("{{ }}"))
        incode += "{{True"
        self.assertEqual(incode.buf, "{{True")
        incode += "}}"
        self.assertEqual(outstream.getvalue(), '')

    def testRender(self):
        instream = StringIO("lorem ipsum dolor sim amet")
        outstream = StringIO()
        Render(instream, outstream)
        self.assertEqual(outstream.getvalue(), "lorem ipsum dolor sim amet")


if __name__ == '__main__':
    unittest.main()
