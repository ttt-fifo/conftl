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
        self.rm_trail_eol = False
        if self.data.startswith('='):
            self.data = self.data[1:]
            self.typ = 'variable'
        elif self.data.endswith(':'):
            self.indent_delta = 1
            self.rm_trail_eol = True
            self.typ = 'blockstart'
        elif self.data == 'pass':
            self.data = ''
            self.indent_delta = -1
            self.rm_trail_eol = True
            self.typ = 'blockend'
        else:
            self.rm_trail_eol = True
            self.typ = 'code'

    def execstr(self):
        if self.typ == 'variable':
            return self.execstr_variable()
        if self.typ == 'code':
            return self.execstr_code()
        elif self.typ == 'blockstart':
            return self.execstr_blockstart()
        elif self.typ == 'blockend':
            return self.execstr_blockend()

    def execstr_variable(self):
        return ' ' * 4 * self.indent + \
               f'_outstream.write(str({self.data}))' + '\n'

    def execstr_code(self):
        return ' ' * 4 * self.indent + str(self.data) + '\n'

    def execstr_blockstart(self):
        return ' ' * 4 * self.indent + str(self.data) + '\n'

    def execstr_blockend(self):
        return ''


class Text:
    def __init__(self, string, indent, rm_first_eol):
        self.data = string
        self.indent = int(indent)
        if rm_first_eol:
            self.data = re.sub('^\n{1}', '', self.data)

    def execstr(self):
        return ' ' * 4 * self.indent + \
               f'_outstream.write("""{self.data}""")' + '\n'


class Render:

    def __init__(self, instream, outstream, context=None, delimiters=None):
        if context:
            self.context = context
        else:
            self.context = {}

        self.context['_outstream'] = outstream

        if delimiters:
            self.delimiters = delimiters
        else:
            self.delimiters = Delimiters()

        self.instream = instream
        self.outstream = outstream

        self.buf = []
        for val in re.split(r"({{.*?}})", instream.read()):
            if val != '':
                self.buf.append(val)

        self.indent = 0
        self.rm_trail_eol = False
        for i, val in enumerate(self.buf):
            self.buf[i] = self.objectify(self.buf[i])

        self.execstr = ''.join([o.execstr() for o in self.buf])
        # print(self.execstr)
        exec(self.execstr, self.context)

    def objectify(self, element):
        m = re.match(r"({{.*}})", element)
        if m:
            obj = Tag(element, self.indent)
            self.indent = max(0, self.indent + obj.indent_delta)
            self.rm_trail_eol = bool(obj.rm_trail_eol)
            return obj
        else:
            return Text(element, self.indent, self.rm_trail_eol)
