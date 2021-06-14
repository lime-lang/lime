from error import RuntimeError
import decimal
import fractions
import operator as op

operators = {
    "PLUS": op.add,
    "MINUS": op.sub, 
    "MUL": op.mul,
    "DIV": op.truediv,
    "EXP": op.pow,
    "EQ": op.eq
}


class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryOperation(self, node):
        return fractions.Fraction(operators[node.operation.type](self.visit(node.left), self.visit(node.right))).limit_denominator(1000000000)

    def visit_Comparison(self, node):
        return operators[node.operation.type](self.visit(node.left), self.visit(node.right))

    def visit_Number(self, node):
        return node.value

    def visit_Variable(self, node):
        return node.value

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name)

        return visitor(node)

    def interpret(self):
        return self.visit(self.parser[0])

    def error(self, node):
        raise RuntimeError(f"No 'visit_{type(node).__name__}' method.")