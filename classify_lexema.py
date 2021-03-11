from token import *

class ClassifyLexema():
    
    reservedWords = ["var", "const", "typedef", "struct", "extends", "procedure",
    "function", "start", "return", "if", "else", "then", "while", "read","print", "int",
    "real", "boolean", "string", "true", "false",
    "global", "local"]
    delimitadores = [";",",","(",")","{","}","[","]","."]
    operadoresAritmeticos = ["+","-","*","/","++","--"]
    operadoresRelacionais = ["==","!=",">",">=","<","<=","="]
    operadoresLogicos = ["&&","||","!"]
    
    def __init__(self):
        self.symbols_table = []
        self.error_tokens = []
        self.tokens = []

    def getToken(self,whole_file) -> list: 
        
        lexema = ''
        counter = 0
        charList = self.splitWord(whole_file) # Transforma a linha em letras
        length = len(charList)
        line = 1
        
        while counter < length:
            if charList[counter].isascii(): # Caso de aspas simples sozinha
                if charList[counter].isspace(): # Verifica se o caracter é um espaço
                    if charList[counter] == "\n":
                        line+=1
                    counter += 1
                elif charList[counter].isidentifier(): # Verifica se o caracter é uma letra
                    while charList[counter].isidentifier() or charList[counter].isnumeric():
                        if charList[counter].isascii():
                            lexema += charList[counter]
                            counter += 1
                            if counter==length:
                                break
                        else:
                            break    
                    if not self.symbols_table.__contains__(lexema): # Insere o lexema na tabela de simbolos
                        self.symbols_table.append(lexema)
                    if self.reservedWords.__contains__(lexema): # Caso seja uma palavra reservada
                        self.tokens.append(Token(RW_TOKEN, lexema, line))
                    else: # Se não for uma palavra reservada, será um identificador
                        self.tokens.append(Token(ID_TOKEN, str(self.symbols_table.index(lexema)), line))
                    lexema = ''                                                                      
                elif charList[counter].isnumeric(): # Verifica se o caracter é um número
                    while charList[counter].isnumeric(): #TODO resolver problema de dígitos (ponto flutuante)
                        lexema += charList[counter]
                        counter += 1
                        if counter==length:
                            break
                    if charList[counter] == ".":
                        lexema += charList[counter]
                        counter += 1
                        if not charList[counter].isnumeric():
                            self.error_tokens.append(Error_Token(NUMBER_ERROR, lexema, line))
                            lexema = ""
                        while charList[counter].isnumeric(): #TODO resolver problema de dígitos (ponto flutuante)
                            lexema += charList[counter]
                            counter += 1
                            if counter==length:
                                break
                    if lexema != "":
                        self.tokens.append(Token(NUMBER_TOKEN, lexema, line))
                    # elif lexema.isdigit(): #REVIEW classificar como dígito (ponto flutuante) # Achar segundo ponto classs como delimitador
                    #     self.tokens.append(Token(DIGIT_TOKEN), lexema)
                    lexema = '' 
                else: # Se não for número, letra ou espaço, será um simbolo
                    if charList[counter]=="\"":# String
                        lexema+=charList[counter]
                        counter+=1
                        while charList[counter]!="\"" and charList[counter]!="\n":
                            lexema += charList[counter]
                            counter += 1
                            # if counter==length: #REVIEW Provalvelmente desnecessario graças ao \n
                            #     break
                        if charList[counter] == "\"":
                            lexema+=charList[counter]
                            self.tokens.append(Token(STRING_TOKEN, lexema, line))
                        else:
                            self.error_tokens.append(Error_Token(STRING_ERROR, lexema, line))
                            line+=1
                        counter+=1
                    elif charList[counter]=="/" and charList[counter+1]=="/": # Comentário em Linha
                        while charList[counter]!="\n":
                            counter+=1
                            if counter==length:
                                break
                    elif charList[counter]=="/" and charList[counter+1]=="*": # Comentário em Bloco TODO rever pq o */ estava bugando
                        lexema += charList[counter] + charList[counter+1]
                        counter+=2
                        while charList[counter]!="*" and charList[counter+1]!="/":
                            lexema += charList[counter]
                            if charList[counter] == "\n":
                                line+=1
                            counter+=1
                            if counter==length:
                                break
                        counter+=2
                    elif self.delimitadores.__contains__(charList[counter]): # Delimitadores
                        self.tokens.append(Token(DELIMITER_TOKEN, charList[counter],line))
                        counter += 1
                    elif charList[counter] in {"+","-","*","/"}:  # OP. Aritmético
                        if self.operadoresAritmeticos.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [++,--]
                            self.tokens.append(Token(OP_A_TOKEN, charList[counter] + charList[counter+1], line))
                            counter += 2
                        else: # Contém os casos: [+, -, *, /]
                            self.tokens.append(Token(OP_A_TOKEN, charList[counter], line))
                            counter += 1
                    elif charList[counter] in {"=","!",">","<"}: #OP. Relacional
                        if self.operadoresRelacionais.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [==, !=, >=, <=]
                            self.tokens.append(Token(OP_R_TOKEN, charList[counter] + charList[counter+1], line))
                            counter += 2
                        elif self.operadoresRelacionais.__contains__(charList[counter]): # Contém os casos: [=, >, <]
                            self.tokens.append(Token(OP_R_TOKEN, charList[counter], line))
                            counter += 1
                        else: # Contém o caso: [!], esse caso é classificado como OP. Lógico
                            self.tokens.append(Token(OP_L_TOKEN, charList[counter], line))
                            counter += 1                  
                    elif charList[counter] in {"&","|"}: # OP. Lógico
                        if self.operadoresLogicos.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [&&, ||]
                            self.tokens.append(Token(OP_L_TOKEN, charList[counter] + charList[counter+1], line))
                            counter += 2
                        else:
                            self.tokens.append(Error_Token(SYMBOL_ERROR, charList[counter], line))
                            counter += 1
                    else: #Caso não se encaixe em nenhum dos padrões acima, é classificado como simbolo
                        self.error_tokens.append(Error_Token(SYMBOL_ERROR, charList[counter], line))
                        counter += 1
                    lexema = ''
            else:
                self.error_tokens.append(Error_Token(OUT_ASCII_ERROR, charList[counter], line))
                counter += 1
        return self.tokens
    
    def getSymbolsTable(self) -> list:
        return self.symbols_table
    
    def getErrorTokens(self) -> list:
        return self.error_tokens
    
    def splitWord(self,whole_file)  -> list:
        return list(whole_file)
    
if __name__ == "__main__": 
    cl = ClassifyLexema()
    arquivo = ''' $
	'''
    cl.getToken(arquivo)
    for error in cl.getErrorTokens():
        print(error)
    