"""
See docs/render_concepts.txt
"""


class Delimiters:
    def __init__(self, string):
        start, end = string.split(' ')
        self.start = start
        self.end = end
        # TODO: error if not '2 symbols, space, 2 symbols'


class OutcodeText:
    def __init__(self, outstream):
        self.outstream = outstream

    def __iadd__(self, other):
        if other == '':
            return self
        self.outstream.write(other)
        return self


class InCode:

    def __init__(self, outstream, context, delimiters):
        self.context = context
        self.context['_outstream'] = outstream
        self.delimiters = delimiters
        self.buf = ''
        self.execbuf = ''
        self.indent = 0
        self.tagtype = 'unknown'

    def __iadd__(self, other):
        if other == '':
            return self
        self.buf += other
        return self

    def tagstart(self):
        self.tagtype = 'unknown'

    def tagend(self):
        self.tagstrip()

        if self.buf.startswith('='):
            self.buf = self.buf.lstrip('=')
            self.buf = f'_outstream.write(str({self.buf}))'
            self.indentbuf()
            self.execbuf += self.buf + '\n'
            self.tagtype = 'variable'
        elif self.buf.endswith(':'):
            self.indentbuf()
            self.execbuf += self.buf + '\n'
            self.indent += 1
            self.tagtype = 'codeblock'
        elif self.buf == 'pass':
            self.indent = max(0, self.indent - 1)
            self.tagtype = 'codeblockend'
        else:
            self.indentbuf()
            self.execbuf += self.buf + '\n'
            self.tagtype = 'code'
        self.buf = ''

        if self.indent == 0:
            exec(self.execbuf, self.context)
            self.execbuf = ''

    def tagstrip(self):
        self.buf = self.buf[2:-2]
        # TODO: strip all \n, \r\n, ' ' from both ends

    def indentbuf(self):
        indentstr = ' ' * self.indent * 4
        self.buf = indentstr + self.buf
        # TODO:may end with \r\n

    def txtstart(self):
        pass

    def txtend(self):
        if self.tagtype in ['codeblock', 'codeblockend']:
            self.buf = self.buf.lstrip('\n')
        if self.buf == "":
            return
        self.buf = self.buf.replace("\n", "\\n")
        self.buf = f'_outstream.write("{self.buf}")'
        self.indentbuf()
        self.execbuf += self.buf + '\n'
        self.buf = ''
        if self.indent == 0:
            exec(self.execbuf, self.context)
            self.execbuf = ''


class Render:
    def __init__(self, instream, outstream, context=None, delimiters=None):
        if context:
            self.context = context
        else:
            self.context = {}

        if delimiters:
            self.delimiters = Delimiters(delimiters)
        else:
            self.delimiters = Delimiters("{{ }}")

        self.instream = instream
        self.outstream = outstream

        self.method_map = {'outcode': {'text': self.outcode_text},
                           'incode': {'tag': self.incode_tag,
                                      'text': self.incode_text}}
        self.buf = ''
        regime = 'outcode'
        mode = 'text'
        self.out_text = OutcodeText(self.outstream)
        self.in_code = InCode(self.outstream, self.context, self.delimiters)
        while True:
            regime, mode = self.method_map[regime][mode]()
            if regime == 'end':
                break

    def getch(self, charcount):
        for n in range(0, charcount):
            c = self.instream.read(1)
            if not c:
                return False
            self.buf += c
        return True

    def outcode_text(self):
        self.out_text += self.buf
        self.buf = ''

        while True:
            if not self.getch(1):
                self.out_text += self.buf
                self.buf = ''
                return 'end', 'end'

            if self.buf[0] == self.delimiters.start[0]:
                if len(self.buf) >= 2:
                    if self.buf[0:2] == self.delimiters.start:
                        return 'incode', 'tag'
                    else:
                        self.out_text += self.buf
                        self.buf = ''
            else:
                self.out_text += self.buf
                self.buf = ''

    def incode_tag(self):
        self.in_code.tagstart()
        self.in_code += self.buf
        self.buf = ''

        while True:
            if not self.getch(1):
                self.in_code += self.buf
                self.in_code.tagend()
                self.buf = ''
                return 'end', 'end'

            if self.buf[0] == self.delimiters.end[0]:
                if len(self.buf) >= 2:
                    if self.buf[0:2] == self.delimiters.end:
                        self.in_code += self.buf
                        self.in_code.tagend()
                        self.buf = ''
                        if self.in_code.indent == 0:
                            return 'outcode', 'text'
                        else:
                            return 'incode', 'text'
                    else:
                        self.in_code += self.buf
                        self.buf = ''
            else:
                self.in_code += self.buf
                self.buf = ''

    def incode_text(self):
        self.in_code.txtstart()
        self.in_code += self.buf
        self.buf = ''

        while True:
            if not self.getch(1):
                self.in_code += self.buf
                self.in_code.txtend()
                self.buf = ''
                return 'end', 'end'

            if self.buf[0] == self.delimiters.start[0]:
                if len(self.buf) >= 2:
                    if self.buf[0:2] == self.delimiters.start:
                        self.in_code.txtend()
                        return 'incode', 'tag'
                    else:
                        self.in_code += self.buf
                        self.buf = ''
            else:
                self.in_code += self.buf
                self.buf = ''
