"""
See docs/render_concepts.txt
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import int
from builtins import str
from future import standard_library
from builtins import object
import re
from ._compat import EOL
standard_library.install_aliases()


re_first_eol = re.compile(r'^\n|\r\n|\r{1}')
re_eol = re.compile(r'\n|\r\n|\r+')
re_three_quotes = re.compile(r'"""')


class Delimiters(object):

    def __init__(self, string="{{ }}"):
        start, stop = string.split(' ')

        self.start = start
        self.start_len = len(self.start)

        self.stop = stop
        self.stop_len = len(self.stop)

        start_escaped = re.escape(self.start)
        stop_escaped = re.escape(self.stop)
        regex_tag = r"(%s[\w\W\r\n]*?%s)" % (start_escaped, stop_escaped)
        self.re_tag = re.compile(regex_tag, re.MULTILINE)


class Tag(object):

    def __init__(self, string, indent, delimiters):
        self.data = string
        self.delimiters = delimiters
        self.data = \
            self.data[self.delimiters.start_len:-self.delimiters.stop_len]
        self.indent = int(indent)
        self.indent_delta = 0
        self.rm_trail_eol = True
        if self.data.startswith('='):
            self.data = self.data[1:]
            self.typ = 'variable'
            self.rm_trail_eol = False
        elif self.data.endswith(':'):
            self.indent_delta = 1
            self.typ = 'blockstart'
        elif self.data == 'pass':
            self.data = ''
            self.indent_delta = -1
            self.typ = 'blockend'
        else:
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
               '_outstream.write(unicode_(%s))' % (self.data) + EOL

    def execstr_code(self):
        result = ''
        for ln in re_eol.split(self.data):
            result += ' ' * 4 * self.indent + str(ln) + EOL
        return result

    def execstr_blockstart(self):
        return ' ' * 4 * self.indent + str(self.data) + EOL

    def execstr_blockend(self):
        return ''


class Text(object):

    def __init__(self, string, indent, rm_first_eol):
        self.data = string
        self.indent = int(indent)
        if rm_first_eol:
            self.data = re_first_eol.sub('', self.data, count=1)

    def execstr(self):
        if self.data:
            self.data = re_three_quotes.sub(r'\"\"\"', self.data, re.MULTILINE)
            return ' ' * 4 * self.indent + \
                   '_outstream.write("""%s""")' % (self.data) + EOL
        else:
            return ''


class Render(object):

    def __init__(self, instream=None, outstream=None, context=None,
                 delimiters=None):

        if context:
            self.context = context
        else:
            self.context = {}

        if delimiters:
            self.delimiters = Delimiters(delimiters)
        else:
            self.delimiters = Delimiters()

        self.instream = instream
        self.outstream = outstream

        self.indent = 0
        self.rm_trail_eol = False

    def __call__(self):
        self.context['_outstream'] = self.outstream

        buf = []
        for val in self.delimiters.re_tag.split(self.instream.read()):
            if val != '':
                buf.append(val)

        self.indent = 0
        self.rm_trail_eol = False
        for i, val in enumerate(buf):
            buf[i] = self.objectify(buf[i])

        execstr = 'from conftl._compat import unicode_' + EOL + \
                  ''.join([o.execstr() for o in buf])
        # print('execstr', execstr)
        exec(execstr, self.context)

    def objectify(self, element):
        m = self.delimiters.re_tag.match(element)
        if m:
            obj = Tag(element, self.indent, self.delimiters)
            self.indent = max(0, self.indent + obj.indent_delta)
            self.rm_trail_eol = bool(obj.rm_trail_eol)
            return obj
        else:
            return Text(element, self.indent, self.rm_trail_eol)
