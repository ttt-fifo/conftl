#!/bin/env python3
import unittest
from conftl.core import Delimiters
from conftl.core import PythonBlock


class TestCore(unittest.TestCase):

    def testDelimiters(self):
        delimiters = Delimiters("{{ }}")
        self.assertEqual(delimiters.start, tuple('{{'))
        self.assertEqual(delimiters.end, tuple('}}'))

    def testPythonBlock(self):
        block = PythonBlock(0, Delimiters("{{ }}"))
        block += '{{pass}}'
        self.assertEqual(str(block), '{{pass}}')


if __name__ == '__main__':
    unittest.main()
