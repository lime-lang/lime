from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


lexer = Lexer(input()).lex()
parser = Parser(lexer).parse()
interpreter = Interpreter(parser)
result = interpreter.interpret()


print(result)