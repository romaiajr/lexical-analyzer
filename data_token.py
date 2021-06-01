from lexical_token import Token

class DataToken ():

    def __init__(self, token:Token, categoria:str, escopo, tipo:str = '-', params:list = '-', valor = '-'):
        self.ide = token.lexema
        self.category = categoria #função, variavel, procedure, const
        self.type = tipo #int, bool, string
        self.params = params
        self.value = valor
        self.scope = escopo

        
