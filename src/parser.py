from error import RuntimeError
import fractions


NUMBER, EXP, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, VAR = (
    "NUMBER", "EXP", "PLUS", "MINUS", "MUL", "DIV", "(", ")", "EOF", "VAR"
)

class AST:
    pass


class BinaryOperation(AST):
    def __init__(self, left, operation, right):
        self.left = left
        self.token = operation
        self.operation = operation
        self.right = right


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.pos = 0
        self.current = self.lexer[self.pos]

    def error(self):
        raise RuntimeError(f"Invalid syntax: '{self.current}'")

    def compare(self, token_type):
        if self.current.type == token_type:
            self.pos += 1
            self.current = self.lexer[self.pos]
        else:
            self.error()

    def factor(self):
        token = self.current

        if token.type == NUMBER:
            self.compare(NUMBER)
            return Number(token)
        elif token.type == VAR:
            self.compare(VAR)
            return Variable(token)
        elif token.type == LPAREN:
            self.compare(LPAREN)
            node = self.expr()
            self.compare(RPAREN)

            return node

    def term(self):
        node = self.factor()

        while self.current.type in (MUL, DIV):
            token = self.current

            self.compare(token.type)

            node = BinaryOperation(node, token, self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current.type in (PLUS, MINUS):
            token = self.current

            self.compare(token.type)

            node = BinaryOperation(node, token, self.term())

        return node

    def parse(self):
        ast = []

        while self.pos < len(self.lexer):
            self.current = self.current = self.lexer[self.pos]
            
            ast.append(self.expr())

            self.pos += 1

        return ast