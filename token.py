RW_TOKEN = "Palavra Reservada"
ID_TOKEN = "Identificador"
NUMBER_TOKEN = "Numero"
DIGIT_TOKEN = "Digito"
STRING_TOKEN = "Cadeia de Caracteres"
DELIMITER_TOKEN = "Delimitador"
OP_A_TOKEN = "Operador Aritmetico"
OP_R_TOKEN = "Operador Relacional"
OP_L_TOKEN = "Operador Logico"
SYMBOL_TOKEN = "Simbolo"


class Token():
    
    def __init__(self,type, lexema):
        self.type = type
        self.lexema = lexema
        
    def __str__(self):
        return f"<{self.type}, {self.lexema}>"