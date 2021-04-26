from lexical_token import *
class sintaxError():

    def __init__(self,token:Token, expected:str):
        self.token = token
        self.expected = expected

    def __str__(self):
            return f'Erro léxico na linha {self.token.line}: Expected "{self.expected}", got "{self.token.lexema}"'