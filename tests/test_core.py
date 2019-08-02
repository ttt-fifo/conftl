#!/bin/env python3
import unittest
from conftl.core import Delimiters
from conftl.core import PythonBlock
from conftl.core import TextBlock


class TestCore(unittest.TestCase):

    def testDelimiters(self):
        delimiters = Delimiters("{{ }}")
        self.assertEqual(delimiters.start, tuple('{{'))
        self.assertEqual(delimiters.end, tuple('}}'))

    def testPythonBlock(self):
        block = PythonBlock(Delimiters("{{ }}"))
        block += '{{pass}}'
        self.assertEqual(str(block), '{{pass}}')

    def testTextBlock(self):
        block = TextBlock()
        block += 'test'
        self.assertEqual(str(block), 'test')



if __name__ == '__main__':
    unittest.main()
