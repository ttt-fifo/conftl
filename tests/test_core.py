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
        incode = InCode(outstream, {}, Delimiters("{{ }}"))
        incode.tagstart()
        incode += "{{True"
        self.assertEqual(incode.buf, "{{True")

        incode += "}}"
        incode.tagend()
        self.assertEqual(outstream.getvalue(), '')

        incode = InCode(outstream, dict(i=10), Delimiters("{{ }}"))
        incode.tagstart()
        incode += '{{=i}}'
        incode.tagend()
        self.assertEqual(outstream.getvalue(), '10')

    def testRender(self):
        instream = StringIO("lorem ipsum dolor sim amet")
        outstream = StringIO()
        Render(instream, outstream)
        self.assertEqual(outstream.getvalue(), "lorem ipsum dolor sim amet")

        instream = StringIO("{{=i}}")
        outstream = StringIO()
        Render(instream, outstream, context=dict(i=100))
        self.assertEqual(outstream.getvalue(), "100")


if __name__ == '__main__':
    unittest.main()
