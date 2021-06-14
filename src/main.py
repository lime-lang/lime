from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


while True:
    lexer = Lexer(input("lime > ")).lex()
    parser = Parser(lexer).parse()
    interpreter = Interpreter(parser)
    result = interpreter.interpret()

    if result != None:
        print(result)