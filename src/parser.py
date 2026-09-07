import re
from ASTree import *


TOKEN_PRINT = "PRINT"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_INT = "INT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_VAR = "VAR"
TOKEN_ASSIGN = "ASSIGN"
TOKEN_NEWLINE = "NEWLINE"
TOKEN_EOF = "EOF"


token_spec = [(r'print', TOKEN_PRINT),
              (r'[a-zA-Z][a-zA-Z0-9]*', TOKEN_VAR),
              (r'=', TOKEN_ASSIGN),
              (r'\(', TOKEN_LPAREN),
              (r'\)', TOKEN_RPAREN),
              (r'\d+', TOKEN_INT),
              (r'\+', TOKEN_PLUS),
              (r'\-', TOKEN_MINUS),
              (r'\n', TOKEN_NEWLINE),
              (r'\s+', None)]


class Lexer:

    def __init__(self, text):
        self.text = self.strip_trailing_newlines(text)
        self.tokens = self.tokenize()
        self.token_idx = 0
        self.is_empty = False


    def strip_trailing_newlines(self, text):
        i = len(text) - 1
        while i > 0 and text[i] == "\n":
            text = text[:-1]
            i -= 1
        return text

    def tokenize(self):

        tokens = []
        i = 0

        while (i < len(self.text)):

            match = None

            for pattern, tag in token_spec:

                regex = re.compile(pattern)
                match = regex.match(self.text, i)

                if (match):
                    if tag:
                        tokens.append((tag, match.group(0)))
                    i = match.end()
                    break

            if not match:
                print(f"ERR: unexpected character {self.text[i]}")
                return
        
        tokens.append((TOKEN_EOF, None))
        return tokens

    def get_next_token(self):

        if self.token_idx == len(self.tokens):
            self.is_empty = True
            return None

        token = self.tokens[self.token_idx]
        self.token_idx += 1
        return token

    def look_ahead(self):

        if self.token_idx >= len(self.tokens) - 1:
            return None
            
        return self.tokens[self.token_idx]


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.valid_binops = [TOKEN_PLUS, TOKEN_MINUS]
        self.module_body = []

    def consume(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print(f"ERR : unexpected token {self.current_token} on consume({token_type})")
            exit(1)

    def strip_newlines(self):
        while self.current_token[0] == TOKEN_NEWLINE:
            self.consume(TOKEN_NEWLINE)

    def binop_obj(self, binop):
        if binop == TOKEN_PLUS:
            return Add()
        elif binop == TOKEN_MINUS:
            return Sub()

    def at_prog_end(self):
        return self.current_token[0] == TOKEN_EOF

    def factor(self):

        token = self.current_token

        if token[0] == TOKEN_INT:
            self.consume(TOKEN_INT)
            return Constant(value=int(token[1]))

        if token[0] == TOKEN_MINUS:
            self.consume(TOKEN_MINUS)
            return UnaryOp(op=USub(), operand=self.factor())
        
        if token[0] == TOKEN_VAR:
            self.consume(TOKEN_VAR)
            return Name(id=token[1], ctx=Load())

        if token[0] == TOKEN_LPAREN:
            self.consume(TOKEN_LPAREN)
            node = self.expr()
            self.consume(TOKEN_RPAREN)
            return node
        
    def term(self):
        return self.factor()    

    def get_next_statement(self):
        self.strip_newlines()
        return self.simple_statement()

    def expr(self):

        node = self.term()
        binop = self.current_token[0]

        while binop in self.valid_binops:
            
            self.consume(binop)
            node = BinOp(left = node, op = self.binop_obj(binop), right = self.term())
            binop = self.current_token[0]

        return node


    def simple_statement(self):

        if self.current_token[0] == TOKEN_PRINT:
            self.consume(TOKEN_PRINT)
            self.consume(TOKEN_LPAREN)
            node = Call(func=Name(id="print", ctx=Load()), args=[self.expr()])
            self.consume(TOKEN_RPAREN)
            return Expr(value=node)
        
        elif self.current_token[0] == TOKEN_VAR:
            next_token = self.lexer.look_ahead()
            if next_token:
                if next_token[0] == TOKEN_ASSIGN:
                    var_id = self.current_token[1]
                    self.consume(TOKEN_VAR)
                    self.consume(TOKEN_ASSIGN)
                    return Assign(targets=[Name(id=var_id, ctx=Store())], value=self.expr())
        
        return self.expr()

    def parse(self):
        
        while not self.at_prog_end():
            self.module_body.append(self.get_next_statement())

        return Module(
            body = self.module_body
        )


def lex(prog):
    L = Lexer(prog)
    return L.tokens


def parse(prog):
    L = Lexer(prog)
    prog_module = Parser(L).parse()
    return ASTree(prog_module)