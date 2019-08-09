#!/bin/env python3
import unittest
import os
from conftl.render_fn import render

TMP = '/tmp'


class TestRenderFunction(unittest.TestCase):

    def testContent(self):
        content = "X"
        self.assertEqual(render(content=content), "X")

    def testContext(self):
        content = "{{=i}}"
        context = dict(i=300)
        self.assertEqual(render(content=content, context=context), "300")

    def testDelimiters(self):
        content = "[[True]]"
        self.assertEqual(render(content=content, delimiters="[[ ]]"), "")

    def testInfile(self):
        tmpl = "X"
        expected_output = "X"

        infile = os.path.join(TMP, 'infile_%s.tmpl' % (os.getpid()))
        with open(infile, 'w') as f:
            f.write(tmpl)

        output = render(infile)

        os.remove(infile)

        self.assertEqual(output, expected_output)

    def testOutfile(self):
        tmpl = "X"
        expected_output = "X"
        outfile = os.path.join(TMP, 'outfile_%s.tmpl' % (os.getpid()))

        render(content=tmpl, outfile=outfile)

        with open(outfile, 'r') as f:
            output = f.read()

        os.remove(outfile)

        self.assertEqual(output, expected_output)

    def testEmptyInput(self):

        with self.assertRaises(RuntimeError):
            render()


if __name__ == '__main__':
    unittest.main()
