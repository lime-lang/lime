from error import RuntimeError
import decimal
import fractions

NUMBER, EXP, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, VAR = (
    "NUMBER", "EXP", "PLUS", "MINUS", "MUL", "DIV", "(", ")", "EOF", "VAR"
)


class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryOperation(self, node):
        if node.operation.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.operation.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.operation.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.operation.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.operation.type == EXP:
            return self.visit(node.left) ** self.visit(node.right)

    def visit_Number(self, node):
        return node.value

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name)

        return fractions.Fraction(visitor(node)).limit_denominator(1000000000)

    def interpret(self):
        return self.visit(self.parser[0])

    def error(self, node):
        raise RuntimeError(f"No 'visit_{type(node).__name__}' method.")