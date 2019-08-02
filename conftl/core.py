from collections import deque


class Delimiters:
    def __init__(self, string):
        start, end = string.split(' ')
        self.start = tuple(start)
        self.end = tuple(end)


class PythonBlock:
    def __init__(self, delimiters):
        self.buf = deque()

    def __iadd__(self, other):
        [self.buf.append(c) for c in other]
        return self

    def __str__(self):
        return ''.join(self.buf)


REGIME_UNKNOWN = 0
REGIME_PYTHON = 1
REGIME_PYTHON_END = 2
REGIME_TEXT = 3
REGIME_TEXT_END = 4

# textual data textual data {{=myvar}} anoter text continues
# ^                         ^ ^     ^ ^
# |                         | |     | |
# |                         | |     | this is REGIME_TEXT
# |                         | |     this is REGIME_PYTHON_END
# |                         | this is REGIME_PYTHON
# this is REGIME_TEXT       this is REGIME_TEXT_END


class Template:

    def __init__(self, instream, outstream, delimiters=None):
        if delimiters:
            self.delimiters = Delimiters(delimiters)
        else:
            self.delimiters = Delimiters("{{ }}")

        self.outstream = outstream

        method_map = {REGIME_UNKNOWN: self.regime_unknown,
                      REGIME_PYTHON: self.regime_python,
                      REGIME_PYTHON_END: self.regime_python_end,
                      REGIME_TEXT: self.regime_text,
                      REGIME_TEXT_END: self.regime_text_end}

        regime = REGIME_UNKNOWN
        buf = deque()
        python_block = None
        while True:
            c = instream.read(1)
            if not c:
                break
            regime, python_block, buf = \
                method_map[regime](c, python_block, buf)

    def regime_unknown(self, c, python_block, buf):
        if c == self.delimiters.start[0]:
            python_block = PythonBlock(self.delimiters)
            python_block += c
            regime = REGIME_PYTHON
        else:
            self.outstream.write(c)
            regime = REGIME_TEXT
        return regime, python_block, buf

    def regime_python(self, c, python_block, buf):
        if c == self.delimiters.end[0]:
            buf.clear()
            buf.append(c)
            regime = REGIME_PYTHON_END
        else:
            python_block += c
            regime = REGIME_PYTHON
        return regime, python_block, buf

    def regime_python_end(self, c, python_block, buf):
        if c in self.delimiters.end:
            if c == self.delimiters.end[-1]:
                python_block += buf
                python_block += c
                self.outstream.write(str(python_block))
                python_block = None
                regime = REGIME_TEXT
            else:
                buf.append(c)
                regime = REGIME_PYTHON_END
        else:
            python_block += buf
            python_block += c
            regime = REGIME_PYTHON
        return regime, python_block, buf

    def regime_text(self, c, python_block, buf):
        if c == self.delimiters.start[0]:
            buf.clear()
            buf.append(c)
            regime = REGIME_TEXT_END
        else:
            self.outstream.write(c)
            regime = REGIME_TEXT
        return regime, python_block, buf

    def regime_text_end(self, c, python_block, buf):
        if c in self.delimiters.start:
            if c == self.delimiters.start[-1]:
                python_block = PythonBlock(self.delimiters)
                python_block += buf
                python_block += c
                regime = REGIME_PYTHON
            else:
                buf.append(c)
                regime = REGIME_TEXT_END
        else:
            self.outstream.write(''.join(buf))
            self.outstream.write(c)
            regime = REGIME_TEXT
        return regime, python_block, buf
