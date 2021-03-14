from lexical_token import *
from iterator import MyIterator

class GenerateTokens():
    
    reservedWords = {"var", "const", "typedef", "struct", "extends", "procedure",
    "function", "start", "return", "if", "else", "then", "while", "read","print", "int",
    "real", "boolean", "string", "true", "false",
    "global", "local"}
    delimitadores = {";",",","(",")","{","}","[","]","."}
    operadoresAritmeticos = {"+","-","*","/","++","--"}
    operadoresRelacionais = {"==","!=",">",">=","<","<=","="}
    operadoresLogicos = {"&&","||","!"}
    
    def __init__(self, whole_file):
        self.tokens, self.error_tokens, self.symbols_table = [],[],[]
        self.line = 1
        self.lexema = ''
        self.itr = MyIterator(whole_file)
            
    def initialState(self): #NOTE Funcionando
        self.lexema = ''
        if self.itr.cur == None:
            return self.tokens
        elif self.itr.cur.isspace():
            if self.itr.cur == "\n":
                self.line+=1
            self.itr.next()
            return self.initialState() 
        elif self.isAscii(self.itr.cur):
            if self.itr.cur.isidentifier():
                return self.ideState()
            elif self.itr.cur.isnumeric():
                return self.numberStateA()
            else:
                return self.symbolState()
        else:
            self.error_tokens.append(Error_Token(OUT_ASCII_ERROR, self.itr.cur, self.line))
            self.itr.next()
            return self.initialState()
            
    def ideState(self): #NOTE Funcionando
        while self.itr.cur.isidentifier() or self.itr.cur.isnumeric() or self.itr.cur == "_":
            self.lexema+=self.itr.cur
            self.itr.next()
            if self.itr.cur == None:
                break
        if not self.symbols_table.__contains__(self.lexema): # Insere o na tabela de simbolos
            self.symbols_table.append(self.lexema)
        if self.reservedWords.__contains__(self.lexema): # Caso seja uma palavra reservada
            self.tokens.append(Token(RW_TOKEN, self.lexema, self.line))
        else: # Se não for uma palavra reservada, será um identificador
            self.tokens.append(Token(ID_TOKEN, self.lexema, self.line))
        return self.initialState()                                         

    def numberStateA(self): #NOTE Funcionando
        while self.itr.cur.isnumeric():
            self.lexema+=self.itr.cur
            self.itr.next()
            if self.itr.cur == None:
                break
        if self.itr.cur == ".":
            self.lexema+=self.itr.cur
            return self.numberStateB()
        else:
            self.tokens.append(Token(NUMBER_TOKEN, self.lexema, self.line))
            return self.initialState()

    def numberStateB(self): #NOTE Funcionando
        self.itr.next()
        if self.itr.cur.isnumeric():
            while self.itr.cur.isnumeric():
                self.lexema+=self.itr.cur
                self.itr.next()
                if self.itr.cur == None:
                    break
            self.tokens.append(Token(NUMBER_TOKEN, self.lexema, self.line))
        else:
            self.error_tokens.append(Error_Token(NUMBER_ERROR, self.lexema, self.line))
        return self.initialState()

    def symbolState(self): #NOTE Funcionando
        if self.itr.cur == "\"":
            self.lexema += self.itr.cur
            return self.stringState()  
        elif self.itr.cur == "/":
            return self.commentState()
        elif self.delimitadores.__contains__(self.itr.cur):
            return self.delimiterState()
        elif self.operadoresAritmeticos.__contains__(self.itr.cur):
            return self.opaState()
        elif self.itr.cur in {"=", "!", ">", "<"}:
            return self.oprState()
        elif self.itr.cur in {"&","|"}: # OP.
            return self.oplState()
        else:
            self.error_tokens.append(Error_Token(SYMBOL_ERROR, self.itr.cur, self.line))
            self.itr.next()
        return self.initialState()

    def stringState(self): #NOTE Funcionando
        self.itr.next()
        while self.itr.cur != "\"" and self.itr.cur != "\n":
            self.lexema+=self.itr.cur
            self.itr.next()
            if self.itr.cur == None:
                break
        if self.itr.cur == "\"":
            self.lexema+=self.itr.cur
            self.tokens.append(Token(STRING_TOKEN, self.lexema, self.line))
            self.itr.next()
        else:
            self.error_tokens.append(Error_Token(STRING_ERROR, self.lexema, self.line))
            self.line+=1
            self.itr.next()
        return self.initialState()
    
    def commentState(self): #NOTE Funcionando
        self.itr.next()
        if self.itr.cur == "/":
            while self.itr.cur != "\n":
                self.itr.next()
                if self.itr.cur == None:
                    break
            if self.itr.cur == "\n":
                self.line+=1
                self.itr.next()
            return self.initialState()
        elif self.itr.cur == "*":
            skipped_lines = 0
            self.lexema += self.itr.prv + self.itr.cur
            self.itr.next()
            while self.itr.cur != "*" and self.itr.nxt != "/":
                if self.itr.cur == "\n":
                    skipped_lines+=1
                else:
                    self.lexema += self.itr.cur
                self.itr.next()
                if self.itr.cur == None:
                    break
            if self.itr.nxt == None:
                self.error_tokens.append(Error_Token(COMMENT_ERROR, self.lexema, self.line))
            self.itr.next() # Para pular o */ final
            self.itr.next()
            self.line += skipped_lines     
            return self.initialState()
        else:
            self.tokens.append(Token(OP_A_TOKEN, self.itr.prv, self.line))
            return self.initialState()
            
    def delimiterState(self): #NOTE Funcionando
        self.tokens.append(Token(DELIMITER_TOKEN, self.itr.cur, self.line))
        self.itr.next()
        return self.initialState()

    def opaState(self): # NOTE Funcionando Operador Aritmético
        if self.itr.cur in {"*","/"}: #REVIEW / já é pego no comentário
            self.tokens.append(Token(OP_A_TOKEN, self.itr.cur, self.line))
            self.itr.next()
        else:
            if self.itr.cur == self.itr.nxt:
                self.tokens.append(Token(OP_A_TOKEN, self.itr.cur + self.itr.nxt, self.line))
                self.itr.next() # Pulando os 2 elementos de ++ ou -- e indo para o próximo
                self.itr.next()
            else:
                self.tokens.append(Token(OP_A_TOKEN, self.itr.cur, self.line))
                self.itr.next()
        return self.initialState()

    def oprState(self):
        if self.itr.nxt == "=":
            self.tokens.append(Token(OP_R_TOKEN, self.itr.cur + self.itr.nxt, self.line))
            self.itr.next()
            self.itr.next()
        else:
            if self.itr.cur == "!":
                self.tokens.append(Token(OP_L_TOKEN, self.itr.cur, self.line))
            else:
                self.tokens.append(Token(OP_R_TOKEN, self.itr.cur, self.line))
            self.itr.next()
        return self.initialState()

    def oplState(self):
        if self.itr.cur == self.itr.nxt:
            self.tokens.append(Token(OP_L_TOKEN, self.itr.cur + self.itr.nxt, self.line))
            self.itr.next()
        else:
            self.error_tokens.append(Error_Token(OP_ERROR, self.itr.cur, self.line))
        self.itr.next()
        return self.initialState()

    def isAscii(self, char):
        return 32 <= ord(char) <= 126

    def getErrorTokens(self):
        return self.error_tokens

if __name__ == "__main__":
    gt = GenerateTokens("10ü")
    item = gt.initialState()
    for i in gt.initialState():
        print(i)
    for i in gt.getErrorTokens():
        print(i)