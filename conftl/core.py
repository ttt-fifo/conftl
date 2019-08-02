class Delimiters:
    def __init__(self, string):
        start, end = string.split(' ')
        self.start = tuple(start)
        self.end = tuple(end)


class PythonBlock:
    def __init__(self):
        self.block = ''

    def __iadd__(self, other):
        self.block += other
        return self


class TextBlock:
    def __init__(self):
        self.block = ''

    def __iadd__(self, other):
        self.block += other
        return self


class Template:

    def __init__(self, stream, delimiters=None):
        if delimiters:
            self.delimiters = Delimiters(delimiters)
        else:
            self.delimiters = Delimiters("{{ }}")

        method_map = {'unknown': self.regime_unknown,
                      'python': self.regime_python,
                      'python_end': self.regime_python_end,
                      'text': self.regime_text,
                      'text_end': self.regime_text_end}

        self.blocks = []
        regime = 'unknown'
        buf = ''
        block = None
        while True:
            c = stream.read(1)
            if not c:
                break
            regime, block, buf = method_map[regime](c, block, buf)

    def regime_unknown(self, c, block, buf):
        if c == self.delimiters.start[0]:
            regime = 'python'
            block = PythonBlock()
            block += c
            buf = ''
        else:
            regime = 'text'
            block = TextBlock()
            block += c
            buf = ''
        return regime, block, buf

    def regime_python(self, c, block, buf):
        if c == self.delimiters.end[0]:
            regime = 'python_end'
            buf = c
        else:
            regime = 'python'
            buf += c
            block += buf
            buf = ''
        return regime, block, buf

    def regime_python_end(self, c, block, buf):
        if c in self.delimiters.end:
            if c == self.delimiters.end[-1]:
                regime = 'text'
                buf += c
                block += buf
                self.blocks.append(block)
                block = TextBlock()
                buf = ''
            else:
                regime = 'python_end'
                buf += c
        else:
            regime = 'python'
            buf += c
            block += buf
            buf = ''
        return regime, block, buf

    def regime_text(self, c, block, buf):
        if c == self.delimiters.start[0]:
            regime = 'text_end'
            buf = c
        else:
            regime = 'text'
            block += c
        return regime, block, buf

    def regime_text_end(self, c, block, buf):
        if c in self.delimiters.start:
            if c == self.delimiters.start[-1]:
                regime = 'python'
                buf += c
                self.blocks.append(block)
                block = PythonBlock()
                block += buf
                buf = ''
            else:
                regime = 'text_end'
                buf += c
        else:
            regime = 'text'
            buf += c
            block += buf
            buf = ''
        return regime, block, buf

