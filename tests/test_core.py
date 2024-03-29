#!/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from io import StringIO
from conftl.core import Render
from conftl._compat import _unicod
import os

TMP = '/tmp'


class TestRenderConcepts(unittest.TestCase):

    def testTag(self):
        tmpl = "{{True}}"
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testUnindent(self):
        tmpl = "{{pass}}"
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testUnindentNewLine(self):
        tmpl = """{{pass}}
"""
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testUnindentRelaxedSyntax(self):
        tmpl = "{{  pass   }}"
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testIndentation(self):
        tmpl = """{{if True:}}
{{True}}
{{pass}}"""
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testIndentationRelaxedSyntax(self):
        tmpl = """{{  if True :  }}
{{True}}
{{pass}}"""
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testClearText(self):
        tmpl = """
lorem ipsum dolor sim amet
text lorem text ipsum text
clear text clear text
texting clearly
"""
        tmpl = _unicod(tmpl)
        expected_output = tmpl
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testClearTextWithDelimiterStart(self):
        tmpl = """
lorem ipsum dolor sim amet
text lorem {{ ipsum text
clear text clear text
texting clearly
"""
        tmpl = _unicod(tmpl)
        expected_output = tmpl
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testClearTextWithDelimiterEnd(self):
        tmpl = """
lorem ipsum dolor sim amet
text lorem }} ipsum text
clear text clear text
texting clearly
"""
        tmpl = _unicod(tmpl)
        expected_output = tmpl
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testClearTextWithThreeQuotes(self):
        tmpl = '''
lorem ipsum dolor sim amet
text lorem """ ipsum text
clear text clear text
texting clearly
'''
        tmpl = _unicod(tmpl)
        expected_output = tmpl
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testClearTextWithUnicode(self):
        tmpl = '''
lorem ipsum dolor sim amet
Моето име е Тодор clear txt continues
lorem Здравей, свят!
clear text clear text
texting clearly
'''
        tmpl = _unicod(tmpl)
        expected_output = tmpl
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testCodeText(self):
        tmpl = """{{for i in range(0, 2):}}
X
{{pass}}
"""
        tmpl = _unicod(tmpl)
        expected_output = """X
X
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testCodeTextUnicode(self):
        tmpl = """{{for i in range(0, 2):}}
свят
{{pass}}
"""
        tmpl = _unicod(tmpl)
        expected_output = _unicod("""свят
свят
""")
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariable(self):
        tmpl = "{{=i}}"
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = "100"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableUnicode(self):
        tmpl = "{{=i}}"
        tmpl = _unicod(tmpl)
        context = dict(i="свят")
        # ??? python2 to convert to unicode output ???
        expected_output = _unicod("свят")
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableFunction(self):
        tmpl = """{{
def one():
     return 1
}}
{{=one()}}"""
        tmpl = _unicod(tmpl)
        context = dict(i=1)
        expected_output = "1"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableList(self):
        tmpl = "{{=[1, 2, 3]}}"
        tmpl = _unicod(tmpl)
        context = dict(i=1)
        expected_output = "[1, 2, 3]"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableDict(self):
        tmpl = "{{=dict(a=2, b=3)}}"
        tmpl = _unicod(tmpl)
        context = dict(i=1)
        expected_output = "{'a': 2, 'b': 3}"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableNewLine(self):
        tmpl = """{{=i}}
"""
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = """100
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableAndClearText(self):
        tmpl = "lorem ipsum {{=i}} text"
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = "lorem ipsum 100 text"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableIndented(self):
        tmpl = """{{if True:}}
{{=i}}{{pass}}"""
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = "100"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableIndentedNewLine(self):
        tmpl = """{{if True:}}
{{=i}}
{{pass}}"""
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = """100
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableCodeText(self):
        tmpl = """{{if True:}}
lorem ipsum {{=i}} texting
{{pass}}"""
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = """lorem ipsum 100 texting
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testVariableRelaxedSyntax(self):
        tmpl = "{{ = i }}"
        tmpl = _unicod(tmpl)
        context = dict(i=100)
        expected_output = "100"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testTwoIndentations(self):
        tmpl = """{{if True:}}
{{if True:}}
X
{{pass}}
{{pass}}
"""
        tmpl = _unicod(tmpl)
        expected_output = """X
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testIfElse(self):
        tmpl = """{{a = 1}}
{{if a == 0:}}
X
{{elif a == 1:}}
Y
{{else:}}
Z
{{pass}}
"""
        tmpl = _unicod(tmpl)
        expected_output = """Y
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testTryExcept(self):
        tmpl = """{{try:}}
{{True}}
{{except Exception as e:}}
X: {{=str(e)}}
{{finally:}}
Y
{{pass}}
"""
        tmpl = _unicod(tmpl)
        expected_output = """Y
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testWhileElse(self):
        tmpl = """{{i = 0}}
{{while i <= 2:}}
{{=i}}
{{i += 1}}
{{else:}}
X
{{pass}}
"""
        tmpl = _unicod(tmpl)
        expected_output = """0
1
2
X
"""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testMultilineCode(self):
        tmpl = """{{
import sys
def one():
    return 1
}}
"""
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testMultilineCodeAfterMultilineCode(self):
        tmpl = """{{
import sys
def one():
    return 1
}}
{{
import os
def two():
    return 2
}}
"""
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testMultilineCodeIndented(self):
        tmpl = """{{if True:}}
{{
def one():
    return 1
}}
{{pass}}
{{=one()}}"""
        tmpl = _unicod(tmpl)
        expected_output = "1"
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testDelimitersChange(self):
        tmpl = "[[True]]"
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, delimiters="[[ ]]")()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testDelimitersThreeChars(self):
        tmpl = "<<<True>>>"
        tmpl = _unicod(tmpl)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, delimiters="<<< >>>")()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testFiles(self):
        tmpl = "X"
        tmpl = _unicod(tmpl)
        expected_output = "X"
        infile = os.path.join(TMP, '%s.tmpl' % (os.getpid()))
        outfile = os.path.join(TMP, '%s.out' % (os.getpid()))

        with open(infile, 'w') as f:
            f.write(tmpl)

        with open(infile, 'r') as instream:
            with open(outfile, 'w') as outstream:
                Render(instream, outstream)()

        with open(outfile, 'r') as f:
            output = f.read()

        os.remove(infile)
        os.remove(outfile)

        self.assertEqual(output, expected_output)

    def testLazy(self):
        rndr = Render()

        tmpl = "X"
        tmpl = _unicod(tmpl)
        expected_output = "X"
        instream = StringIO(tmpl)
        outstream = StringIO()
        rndr.instream = instream
        rndr.outstream = outstream
        rndr()
        self.assertEqual(outstream.getvalue(), expected_output)

        tmpl = "Y"
        tmpl = _unicod(tmpl)
        expected_output = "Y"
        instream = StringIO(tmpl)
        outstream = StringIO()
        rndr.instream = instream
        rndr.outstream = outstream
        rndr()
        self.assertEqual(outstream.getvalue(), expected_output)

    def testException(self):
        tmpl = "{{raise RuntimeError}}"
        tmpl = _unicod(tmpl)
        instream = StringIO(tmpl)
        outstream = StringIO()
        with self.assertRaises(RuntimeError):
            Render(instream, outstream)()


if __name__ == '__main__':
    unittest.main()
