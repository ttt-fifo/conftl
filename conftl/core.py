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


class TextBlock:
    def __init__(self):
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
        block = None
        while True:
            c = instream.read(1)
            if not c:
                break
            regime, block, buf = method_map[regime](c, block, buf)

    def regime_unknown(self, c, block, buf):
        if c == self.delimiters.start[0]:
            regime = REGIME_PYTHON
            block = PythonBlock(self.delimiters)
            block += c
            buf.clear()
        else:
            regime = REGIME_TEXT
            block = TextBlock()
            block += c
            buf.clear()
        return regime, block, buf

    def regime_python(self, c, block, buf):
        if c == self.delimiters.end[0]:
            regime = REGIME_PYTHON_END
            buf.append(c)
        else:
            regime = REGIME_PYTHON
            buf.append(c)
            block += buf
            buf.clear()
        return regime, block, buf

    def regime_python_end(self, c, block, buf):
        if c in self.delimiters.end:
            if c == self.delimiters.end[-1]:
                regime = REGIME_TEXT
                buf.append(c)
                block += buf
                self.outstream.write(str(block))
                block = TextBlock()
                buf.clear()
            else:
                regime = REGIME_PYTHON_END
                buf.append(c)
        else:
            regime = REGIME_PYTHON
            buf.append(c)
            block += buf
            buf.clear()
        return regime, block, buf

    def regime_text(self, c, block, buf):
        if c == self.delimiters.start[0]:
            regime = REGIME_TEXT_END
            buf = deque(c)
        else:
            regime = REGIME_TEXT
            block += c
        return regime, block, buf

    def regime_text_end(self, c, block, buf):
        if c in self.delimiters.start:
            if c == self.delimiters.start[-1]:
                regime = REGIME_PYTHON
                buf.append(c)
                self.outstream.write(str(block))
                block = PythonBlock(self.delimiters)
                block += buf
                buf.clear()
            else:
                regime = REGIME_TEXT_END
                buf.append(c)
        else:
            regime = REGIME_TEXT
            buf.append(c)
            block += buf
            buf.clear()
        return regime, block, buf
