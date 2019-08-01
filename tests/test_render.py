from yatlex.template import render
import unittest


class TestRender(unittest.TestCase):

    def test_xmlescape(self):
        """
        The normal behavior of the original yatl is to escape xml tags
        """
        content = "{{=myvar}}"
        context = dict(myvar="<>")
        self.assertEqual(render(content=content, context=context),
                         "&lt;&gt;")

    def test_no_xmlescape(self):
        """
        yatlex can suspend this behavior with xmlescape=False
        """
        content = "{{=myvar}}"
        context = dict(myvar="<>")
        self.assertEqual(render(content=content, context=context,
                                xmlescape=False),
                         "<>")

    def test_no_sanitizeeol(self):
        """
        The normal behaviour of original yatl
        puts some more \n if you embed clear python code in template
        """
        content = """
{{for i in range(0, 3):}}
{{=i}}
{{pass}}
"""
        expected_result = """

0

1

2

"""
        self.assertEqual(render(content=content), expected_result)

    def test_sanitizeeol(self):
        """
        With sanitizeeol=True yatlex improves writing code in template
        """
        content = """
{{for i in range(0, 3):}}
{{=i}}
{{pass}}
"""
        expected_result = """
0
1
2
"""
        self.assertEqual(render(content=content, sanitizeeol=True),
                         expected_result)


if __name__ == '__main__':
    unittest.main()
