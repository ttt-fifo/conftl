"""
Configuration Templating Language Core
"""
# See docs/render_concepts.txt
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from builtins import object
import re
from ._compat import EOL
from ._compat import _unicod
standard_library.install_aliases()


re_first_eol = re.compile(r'^\n|\r\n|\r{1}')
re_eol = re.compile(r'\n|\r\n|\r+', re.MULTILINE)
re_three_quotes = re.compile(r'"""', re.MULTILINE)
re_blockmiddle = re.compile('^else:|elif |except:|except |finally:.*$')


class Delimiters(object):
    """
    Represents the tag delimiters
    """

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
    """
    Represents one tag {{...}}
    """
    # See docs/codeblock_concepts.txt

    def __init__(self, string, indent, blockindent, delimiters):
        self.data = string
        self.indent = indent
        self.blockindent = blockindent

        self.data = self.data[delimiters.start_len:-delimiters.stop_len]

        self.typ = 'unknown'
        self.indent_next = self.indent
        self.rm_trail_eol = True

        if self.data.endswith(':'):
            m = re_blockmiddle.match(self.data)
            if m:
                self.typ = 'blockmiddle'
                self.indent = self.blockindent
            else:
                self.typ = 'blockstart'
                self.blockindent = self.indent
                self.indent_next = self.indent + 1
        elif self.data.startswith('='):
            self.typ = 'variable'
            self.data = self.data[1:]
            self.rm_trail_eol = False
        elif self.data == 'pass':
            self.typ = 'blockend'
            self.indent_next = max(0, self.indent - 1)
            self.blockindent = max(0, self.blockindent - 1)
        else:
            self.typ = 'code'

    def execstr(self):
        """
        Returns the python string to execute
        """

        # conditionally execute a method, based on current type
        return getattr(self, 'execstr_%s' % (self.typ))()

    def execstr_blockstart(self):
        return ' ' * 4 * self.indent + self.data + EOL

    def execstr_blockend(self):
        return ''

    def execstr_blockmiddle(self):
        return ' ' * 4 * self.indent + self.data + EOL

    def execstr_variable(self):
        # _unicod is from _compat: the unicode value for the current
        # python version
        return ' ' * 4 * self.indent + \
               '_outstream.write(_unicod(%s))' % (self.data) + EOL

    def execstr_code(self):
        # only code is processed line by line
        result = ''
        for ln in re_eol.split(self.data):
            result += ' ' * 4 * self.indent + ln + EOL
        return result

    def execstr_unknown(self):
        # this should never happen
        raise RuntimeError("Tag.typ = 'unknown'!")


class Text(object):
    """
    Represents clear text
    """

    def __init__(self, string, indent, rm_first_eol):
        self.data = string
        self.indent = indent
        # the previous code block controls if we remove first eol in text
        # (this is sanitize eol feature)
        if rm_first_eol:
            self.data = re_first_eol.sub('', self.data, count=1)

    def execstr(self):
        """
        Returns the python string to execute
        """

        if self.data:
            # three double quotes are escaped
            self.data = re_three_quotes.sub(r'\"\"\"', self.data)
            return ' ' * self.indent * 4 + \
                   '_outstream.write(_unicod("""%s"""))' % (self.data) + EOL
        else:
            return ''


class Render(object):
    """
    Class for rendering a template

    Arguments:
        instream: input stream, should be file handle like object
        outstream: output stream, should be file handle like object
        context: execution context, e.g. variables exported to template
        delimiters: tag delimiters, defaulting to "{{ }}"

    Usage:
        # create the object once
        rndr = Render()

        # repeat this code to template multiple files
        rndr.instream = open('template.tmpl')
        rndr.outstream = open('outfile.conf')
        rndr.context = {...}
        rndr()
        rndr.instream.close()
        rndr.outstream.close()
        # --------------------------------------------

    Alternative Usage:
        instream = StringIO("{{=a}}")
        outstream = StringIO()
        context = dict(a=5)
        Render(instream=instream, outstream=outstream, context=context)()
        output = outstream.getvalue()
    """

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

    def __call__(self):
        """
        The code may be executed multiple times
        """

        # these are needed in context
        # _unicod is the unicode representation for the current python version
        self.context['_outstream'] = self.outstream
        self.context['_unicod'] = _unicod

        # split tags from text in the buffer
        buf = []
        for val in self.delimiters.re_tag.split(self.instream.read()):
            if val != '':
                buf.append(val)

        # every buffer value is converted to object
        self.indent = 0
        self.blockindent = 0
        self.rm_trail_eol = False
        for i, val in enumerate(buf):
            buf[i] = self.objectify(buf[i])

        # execute the resulting python code
        execstr = ''.join([o.execstr() for o in buf])
        # print('==================')
        # print(execstr)
        exec(execstr, self.context)

    def objectify(self, element):
        """
        Creates the correct object from the given string
        """

        m = self.delimiters.re_tag.match(element)
        if m:
            obj = Tag(element, self.indent, self.blockindent, self.delimiters)
            self.indent = obj.indent_next
            self.blockindent = obj.blockindent
            self.rm_trail_eol = obj.rm_trail_eol
            return obj
        else:
            return Text(element, self.indent, self.rm_trail_eol)
