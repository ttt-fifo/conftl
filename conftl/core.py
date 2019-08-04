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

    def __init__(self, outstream, delimiters):
        self.outstream = outstream
        self.delimiters = delimiters
        self.buf = ''
        self.execbuf = ''
        self.indent = 0

    def __iadd__(self, other):
        if other == '':
            return self
        self.buf += other
        return self

    def tagstart(self):
        pass

    def tagend(self):
        self.tagstrip()

        if self.buf.startswith('='):
            self.buf = self.buf.lstrip('=')
            print(self.buf)
            self.buf = f'_outstream.write({self.buf})'
            self.indentbuf()
            self.execbuf += '\n' + self.buf + '\n'
        elif self.buf.endswith(':'):
            self.indentbuf()
            self.execbuf += '\n' + self.buf + '\n'
            self.indent += 1
        elif self.buf == 'pass':
            self.indent = max(0, self.indent - 1)
        else:
            self.indentbuf()
            self.execbuf += '\n' + self.buf + '\n'
        self.buf = ''

        if self.indent == 0:
            exec(self.execbuf, {})
            self.execbuf = ''

    def tagstrip(self):
        self.buf = self.buf[2:-2]
        # TODO: strip all \n, \r\n, ' ' from both ends

    def indentbuf(self):
        indentstr = ' ' * self.indent * 4
        self.buf = self.buf + indentstr
        # TODO:may end with \r\n
        self.buf.replace('\n', '\n' + indentstr)


class Render:
    def __init__(self, instream, outstream, delimiters=None):
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
        self.in_code = InCode(self.outstream, self.delimiters)
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
                    if self.buf[0:1] == self.delimiters.end:
                        self.in_code += self.buf
                        self.in_code.tagend()
                        self.buf = ''
                        return 'end'
                        # TODO
                    else:
                        self.in_code += self.buf
                        self.buf = ''
            else:
                self.in_code += self.buf
                self.buf = ''

    def incode_text(self):
        pass
