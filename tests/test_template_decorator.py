#!/bin/env python3
import unittest
from conftl.template_decorator import template


class TestTemplateDecorator(unittest.TestCase):

    def testTemplate(self):

        @template(content="{{=i}}")
        def templateme():
            return dict(i=28)

        self.assertEqual(templateme(), "28")

    def testEmptyInput(self):

        with self.assertRaises(RuntimeError):
            @template()
            def templateme():
                return dict(i=76)

    def testContextNonDict(self):

        @template(content="{{=i}}")
        def templateme():
            return None

        with self.assertRaises(RuntimeError):
            templateme()


if __name__ == '__main__':
    unittest.main()
