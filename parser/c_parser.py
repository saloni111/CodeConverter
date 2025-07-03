from pycparser import c_parser

class CParser:
    def __init__(self):
        self.parser = c_parser.CParser()

    def parse(self, code: str):
        return self.parser.parse(code) 