from enum import Enum

class TokenType(Enum):
    UNKNOWN = 0
    KEYWORD = 1
    IDENT = 2
    EQUAL = 3
    OPENSET = 4
    ELEMENT = 5
    CLOSESET = 6

class Token:
    def __init__(self, typ, value):
        self.type = typ
        self.value = value

    def __repr__(self):
        return f"{self.type}: {self.value}"

keywords = [
    "let"
]

def keyword(which):
    return Token(TokenType.KEYWORD, which)

def ident(symbol):
    return Token(TokenType.IDENT, symbol)

def equal():
    return Token(TokenType.EQUAL, "=")

def begin_set():
    return Token(TokenType.OPENSET, "{")

def end_set():
    return Token(TokenType.CLOSESET, "}")

def element(value):
    return Token(TokenType.ELEMENT, value)

class Lexer:
    def __init__(self, source):
        self.source = source
        self.source_len = len(self.source) - 1
        self.current = 0
        self.char = self.source[self.current]

    def next(self):
        if self.current < self.source_len:
            self.current += 1

        self.char = self.source[self.current]

    def tokenize(self):
        tokens = []

        while self.current < self.source_len:
            # Ignore whitespaces
            while self.char.isspace():
                self.next()

            # Construct a word. There can be some possibilities for "words":
            # - keyword: special things such as let
            # - identifier: comes ONLY after let. determine later
            # - element: any alphanumeric thing is an element
            if self.char.isalnum():
                word = ""
                while self.char.isalnum():
                    word += self.char
                    self.next()

                if word in keywords:
                    tokens.append(keyword(word))
                else:
                    tokens.append(element(word))

            # Find =
            if self.char == "=":
                tokens.append(equal())

            # Find opening and closing brackets
            if self.char == "{":
                tokens.append(begin_set())

            if self.char == "}":
                tokens.append(end_set())

            self.next()

        return tokens

source = "let A = {1 2 3}"
lexer = Lexer(source)

tokens = lexer.tokenize()
for tok in tokens:
    print(tok.value)
