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
    def __init__(self, typ, value, bracket_level):
        self.type = typ
        self.value = value
        self.bracket_level = bracket_level

    def __repr__(self):
        return f"{self.type}: {self.value}" + (f", BracketLevel: {self.bracket_level}" if self.bracket_level >= 0 else "")

keywords = [
    "let"
]

def keyword(which):
    return Token(TokenType.KEYWORD, which, -1)

def ident(symbol):
    return Token(TokenType.IDENT, symbol, -1)

def equal():
    return Token(TokenType.EQUAL, "=", -1)

def begin_set():
    return Token(TokenType.OPENSET, "{", 0)

def end_set():
    return Token(TokenType.CLOSESET, "}", 0)

def element(value):
    return Token(TokenType.ELEMENT, value, 0)

class Lexer:
    def __init__(self, source):
        self.source = source
        self.source_len = len(self.source)
        self.current = 0
        self.char = self.source[self.current]

    def next(self):
        self.current += 1
        if self.current < self.source_len:
            self.char = self.source[self.current]

    def tokenize(self):
        tokens = []

        while self.current < self.source_len:
            # Ignore whitespaces
            while self.char.isspace():
                self.next()

            # Construct a word. There can be some possibilities for "words":
            # - keyword: special things such as let
            # - identifier: all uppercase
            # - element: any alphanumeric thing is an element
            if self.char.isalnum():
                word = ""
                while self.char.isalnum():
                    word += self.char
                    self.next()

                if word in keywords:
                    tokens.append(keyword(word))
                elif word.isupper():
                    tokens.append(ident(word))
                else:
                    elem = int(word) if word.isnumeric() else word
                    tokens.append(element(elem))

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

def reference_brackets(tokens):
    count = 0
    toks = tokens

    for (i, tok) in enumerate(toks):
        if tok.type == TokenType.OPENSET:
            toks[i].bracket_level = count
            count += 1
        if tok.type == TokenType.CLOSESET:
            count -= 1
            toks[i].bracket_level = count

        if tok.type == TokenType.ELEMENT:
            toks[i].bracket_level = count - 1

    return toks

def construct_set(tokens):
    s = set()
    current = 0
    len_toks = len(tokens)
    elements = []

    while current < len_toks - 1:
        current += 1

        if tokens[current].type == TokenType.CLOSESET:
            print("end_set")

            # Once done parsing a set, add its elements to the set we're building
            for elem in elements:
                s.add(elem)

        if tokens[current].type == TokenType.OPENSET:
            print("begin_set")

        if tokens[current].type == TokenType.ELEMENT:
            print(f"element: {tokens[current].value}")
            elements.append(tokens[current].value)

    return s

source = "let A = {1 2 3 4 5 6 7 8 9 10}"
lexer = Lexer(source)

print(source)
tokens = reference_brackets(lexer.tokenize())
#for tok in tokens:
#    print(tok)

print(construct_set(tokens))
