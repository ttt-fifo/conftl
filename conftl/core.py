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


class Template:

    def __init__(self, instream, outstream, delimiters=None):
        if delimiters:
            self.delimiters = Delimiters(delimiters)
        else:
            self.delimiters = Delimiters("{{ }}")

        self.outstream = outstream

        method_map = {'unknown': self.regime_unknown,
                      'python': self.regime_python,
                      'python_end': self.regime_python_end,
                      'text': self.regime_text,
                      'text_end': self.regime_text_end}

        regime = 'unknown'
        buf = deque()
        block = None
        while True:
            c = instream.read(1)
            if not c:
                break
            regime, block, buf = method_map[regime](c, block, buf)

    def regime_unknown(self, c, block, buf):
        if c == self.delimiters.start[0]:
            regime = 'python'
            block = PythonBlock(self.delimiters)
            block += c
            buf.clear()
        else:
            regime = 'text'
            block = TextBlock()
            block += c
            buf.clear()
        return regime, block, buf

    def regime_python(self, c, block, buf):
        if c == self.delimiters.end[0]:
            regime = 'python_end'
            buf.append(c)
        else:
            regime = 'python'
            buf.append(c)
            block += buf
            buf.clear()
        return regime, block, buf

    def regime_python_end(self, c, block, buf):
        if c in self.delimiters.end:
            if c == self.delimiters.end[-1]:
                regime = 'text'
                buf.append(c)
                block += buf
                self.outstream.write(str(block))
                block = TextBlock()
                buf.clear()
            else:
                regime = 'python_end'
                buf.append(c)
        else:
            regime = 'python'
            buf.append(c)
            block += buf
            buf.clear()
        return regime, block, buf

    def regime_text(self, c, block, buf):
        if c == self.delimiters.start[0]:
            regime = 'text_end'
            buf = deque(c)
        else:
            regime = 'text'
            block += c
        return regime, block, buf

    def regime_text_end(self, c, block, buf):
        if c in self.delimiters.start:
            if c == self.delimiters.start[-1]:
                regime = 'python'
                buf.append(c)
                self.outstream.write(str(block))
                block = PythonBlock(self.delimiters)
                block += buf
                buf.clear()
            else:
                regime = 'text_end'
                buf.append(c)
        else:
            regime = 'text'
            buf.append(c)
            block += buf
            buf.clear()
        return regime, block, buf
