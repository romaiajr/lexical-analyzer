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

class Token():
    
    def __init__(self,type, lexema, line):
        self.type = type
        self.lexema = lexema
        self.line = line
        
    def __str__(self):
        if self.line <= 9:
            return f"0{self.line} {self.type} {self.lexema}"
        else:
            return f"{self.line} {self.type} {self.lexema}"
        
    
class Error_Token(Token):

    def __init__(self,type, lexema, line):
        self.type = type
        self.lexema = lexema
        self.line = line
        
    def __str__(self):
        if self.line <= 9:
            return f"0{self.line} {self.type} {self.lexema}"
        else:
            return f"{self.line} {self.type} {self.lexema}"
        