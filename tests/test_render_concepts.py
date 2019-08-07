#!/bin/env python3
import unittest
from io import StringIO
from conftl.core import Render


class TestRenderConcepts(unittest.TestCase):

    def testTag(self):
        tmpl = "{{True}}"
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)
        self.assertEqual(outstream.getvalue(), expected_output)

    def testUnindent(self):
        tmpl = "{{pass}}"
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)
        self.assertEqual(outstream.getvalue(), expected_output)

    def testUnindentNewLine(self):
        tmpl = """{{pass}}
"""
        context = dict(i=100)
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream, context=context)
        self.assertEqual(outstream.getvalue(), expected_output)

    def testIndentation(self):
        tmpl = """{{if True:}}
{{True}}
{{pass}}"""
        expected_output = ""
        instream = StringIO(tmpl)
        outstream = StringIO()
        Render(instream, outstream)
        self.assertEqual(outstream.getvalue(), expected_output)

#     def testClearText(self):
#         tmpl = """
# lorem ipsum dolor sim amet
# text lorem text ipsum text
# clear text clear text
# texting clearly
# """
#         expected_output = tmpl
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
# #    def testClearTextWithDelimiterStart(self):
# #        tmpl = """
# # lorem ipsum dolor sim amet
# # text lorem {{ ipsum text
# # clear text clear text
# # texting clearly
# # """
# #        expected_output = tmpl
# #        instream = StringIO(tmpl)
# #        outstream = StringIO()
# #        Render(instream, outstream)
# #        self.assertEqual(outstream.getvalue(), expected_output)
#
# #    def testClearTextWithDelimiterEnd(self):
# #        tmpl = """
# # lorem ipsum dolor sim amet
# # text lorem }} ipsum text
# # clear text clear text
# # texting clearly
# # """
# #        expected_output = tmpl
# #        instream = StringIO(tmpl)
# #        outstream = StringIO()
# #        Render(instream, outstream)
# #
#
#     def testCodeText(self):
#         tmpl = """{{for i in range(0, 2):}}
# X
# {{pass}}
# """
#         expected_output = """X
# X
# """
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testVariable(self):
#         tmpl = "{{=i}}"
#         context = dict(i=100)
#         expected_output = "100"
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream, context=context)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testVariableNewLine(self):
#         tmpl = """{{=i}}
# """
#         context = dict(i=100)
#         expected_output = """100
# """
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream, context=context)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testVariableAndClearText(self):
#         tmpl = "lorem ipsum {{=i}} text"
#         context = dict(i=100)
#         expected_output = "lorem ipsum 100 text"
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream, context=context)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testVariableIndented(self):
#         tmpl = """{{if True:}}
# {{=i}}{{pass}}"""
#         context = dict(i=100)
#         expected_output = "100"
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream, context=context)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testVariableIndentedNewLine(self):
#         tmpl = """{{if True:}}
# {{=i}}
# {{pass}}"""
#         context = dict(i=100)
#         expected_output = """100
# """
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream, context=context)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testVariableCodeText(self):
#         tmpl = """{{if True:}}
# lorem ipsum {{=i}} texting
# {{pass}}"""
#         context = dict(i=100)
#         expected_output = """lorem ipsum 100 texting
# """
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream, context=context)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testTwoIndentations(self):
#         tmpl = """{{if True:}}
# {{if True:}}
# X
# {{pass}}
# {{pass}}
# """
#         expected_output = """X
# """
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testMultilineCode(self):
#         tmpl = """{{
# import sys
# def one():
#     return 1
# }}
# """
#         expected_output = ""
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testMultilineCodeIndented(self):
#         tmpl = """{{if True:}}
# {{
# def one():
#     return 1
# }}
# {{pass}}
# {{=one()}}"""
#         expected_output = "1"
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream)
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testDelimitersChange(self):
#         tmpl = "[[True]]"
#         expected_output = ""
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         Render(instream, outstream, delimiters="[[ ]]")
#         self.assertEqual(outstream.getvalue(), expected_output)
#
#     def testException(self):
#         tmpl = "{{raise RuntimeError}}"
#         instream = StringIO(tmpl)
#         outstream = StringIO()
#         with self.assertRaises(RuntimeError):
#             Render(instream, outstream)


if __name__ == '__main__':
    unittest.main()
