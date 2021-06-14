from error import RuntimeError
import fractions


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, plaintext):
        self.plaintext = plaintext.replace(" ", "")
        self.pos = 0
        self.current = self.plaintext[self.pos]

    def error(self):
        raise RuntimeError(f"Invalid token: '{self.current}'")

    def increment(self):
        self.pos += 1

        if self.pos >= len(self.plaintext):
            self.current = None
        else:
            self.current = self.plaintext[self.pos]

    def number(self):
        temp = ""

        while self.current is not None and self.current.isdigit() or self.current == ".":
            temp += self.current
            self.increment()

        return fractions.Fraction(temp).limit_denominator(1000000000)

    def lex(self):
        tokens = []
        multipliable = False

        while self.current is not None:
            if self.current == "^":
                self.increment()
                tokens.append(Token("EXP", "^"))
                multipliable = False
                continue

            if self.current == "=":
                self.increment()
                tokens.append(Token("EQ", "="))
                multipliable = False
                continue

            if self.current == "+":
                self.increment()
                tokens.append(Token("PLUS", "+"))
                multipliable = False
                continue

            if self.current == "-":
                self.increment()
                tokens.append(Token("MINUS", "-"))
                multipliable = False
                continue

            if self.current == "*":
                self.increment()
                tokens.append(Token("MUL", "*"))
                multipliable = False
                continue

            if self.current == "/":
                self.increment()
                tokens.append(Token("DIV", "/"))
                multipliable = False
                continue

            if self.current == ")":
                self.increment()
                tokens.append(Token("RPAREN", ")"))
                multipliable = False
                continue

            if multipliable:
                tokens.append(Token("MUL", "*"))
                
            if self.current.isdigit():
                if multipliable:
                    tokens.append(Token("MUL", "*"))
                
                tokens.append(Token("NUMBER", self.number()))
                multipliable = True
                continue

            if self.current == "(":
                self.increment()
                tokens.append(Token("LPAREN", "("))
                multipliable = False
                continue


            tokens.append(Token("VAR", self.current))
            multipliable = True
            self.increment()
        
        tokens.append(Token("EOF", None))
        return tokens
