"""
See docs/render_concepts.txt
"""
import re


class Delimiters:
    def __init__(self, string="{{ }}"):
        start, stop = string.split(' ')
        self.start = start
        self.stop = stop


class Tag:

    def __init__(self, string, indent):
        self.data = string
        self.data = self.data[2:-2]
        self.indent = int(indent)
        self.indent_delta = 0
        if self.data.startswith('='):
            self.data = self.data[1:]
            self.typ = 'variable'
        elif self.data.endswith(':'):
            self.indent_delta = 1
            self.typ = 'code'
        elif self.data == 'pass':
            self.data = ''
            self.indent_delta = -1
            self.typ = 'unindent'
        else:
            self.typ = 'code'

    def execstr(self):
        if self.typ == 'variable':
            return self.execstr_variable()
        elif self.typ == 'code':
            return self.execstr_code()
        elif self.typ == 'unindent':
            return self.execstr_unindent()

    def execstr_variable(self):
        return ' ' * 4 * self.indent + \
               f'_outstream.write(str({self.data}))' + '\n'

    def execstr_code(self):
        return ' ' * 4 * self.indent + self.data

    def execstr_unindent(self):
        return ''


class Text:
    def __init__(self, string, indent):
        self.data = string
        self.indent = int(indent)

    def execstr(self):
        return ' ' * 4 * self.indent + \
               f'_outstream.write("""{self.data}""")' + '\n'


class Render:

    def __init__(self, instream, outstream, context=None, delimiters=None):
        if context:
            self.context = context
        else:
            self.context = {}

        if delimiters:
            self.delimiters = delimiters
        else:
            self.delimiters = Delimiters()

        self.instream = instream
        self.outstream = outstream

        self.indent = 0
        self.buf = re.split(r"({{.*?}})", instream.read())
        for i, val in enumerate(self.buf):
            self.buf[i] = self.objectify(self.buf[i])

        self.execstr = ''.join([o.execstr() for o in self.buf])

    def objectify(self, element):
        m = re.match(r"{{.*}}", element)
        if m:
            obj = Tag(element, self.indent)
            self.indent = max(0, self.indent + obj.indent_delta)
            return obj
        else:
            return Text(element, self.indent)
