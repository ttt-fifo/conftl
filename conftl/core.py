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
    def __init__(self):
        pass


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
                    if self.buf[0:1] == self.delimiters.start:
                        del self.buf[0:1]
                        return 'incode', 'tag'
                    else:
                        self.out_text += self.buf
                        self.buf = ''
            else:
                self.out_text += self.buf
                self.buf = ''

    def incode_tag(self):
        pass

    def incode_text(self):
        pass
