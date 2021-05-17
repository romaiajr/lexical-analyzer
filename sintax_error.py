from lexical_token import *
class SintaxError():

    def __init__(self,token:Token, expected:str):
        self.token = token
        self.expected = expected

    def __str__(self):
            return f'Erro de sintaxe na linha {self.token.line}: Expected "{self.expected}", got "{self.token.lexema}"'