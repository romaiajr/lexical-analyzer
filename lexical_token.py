RW_TOKEN = "PRE" # Palavra Reservada
ID_TOKEN = "IDE" # Identificador
NUMBER_TOKEN = "NRO" # Número
STRING_TOKEN = "CAD" # Cadeia de Caracteres
DELIMITER_TOKEN = "DEL" # Delimitador
OP_A_TOKEN = "ART" # Op. Aritmético
OP_R_TOKEN = "REL" # Op. Relacional
OP_L_TOKEN = "LOG" # Op. Lógico

SYMBOL_ERROR = "SIB" # Simbolo Invalido
STRING_ERROR = "CMF" # Cadeia Mal Formada
NUMBER_ERROR = "NMF" # Número Mal Formado
COMMENT_ERROR = "CoMF" # Comentário Mal Formado
OP_ERROR = "OpMF" # Operador Mal Formado
OUT_ASCII_ERROR = "CNPA" # Caracter Não Pertence ao Alfabeto
STRING_NO_ASCII = "CCNA" # Cadeia com Caracter Não pertencente ao Alfabeto

class Token():
    '''
    Classe que representa os Tokens
    '''
    def __init__(self,type:str, lexema:str, line:int):
        '''
        Params:
        type: Tipo de Token
        lexema: Lexema do Token
        line: Linha em que o lexema começa
        '''
        self.type = type
        self.lexema = lexema
        self.line = line
        
    def __str__(self):
        if self.line <= 9:
            return f"0{self.line} {self.type} {self.lexema}"
        else:
            return f"{self.line} {self.type} {self.lexema}"

    def getLexema(self):
        return self.lexema
    
    def getLine(self):
        return self.line

    def getType(self):
        return self.type
         
class Error_Token(Token):
    '''
    Classe que representa os Tokens de erros
    '''
    def __init__(self,type, lexema, line):
        '''
        Params:
        type: Tipo de Token
        lexema: Lexema do Token
        line: Linha em que o lexema começa
        '''
        self.type = type
        self.lexema = lexema
        self.line = line
        
    def __str__(self):
        if self.line <= 9:
            return f"0{self.line} {self.type} {self.lexema}"
        else:
            return f"{self.line} {self.type} {self.lexema}"
        