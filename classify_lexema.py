class ClassifyLexema():
    reservedWords = ["var", "const", "typedef", "struct", "extends", "procedure",
    "function", "start", "return", "if", "else", "then", "while", "read","print", "int",
    "real", "boolean", "string", "true", "false",
    "global", "local"]
    operadorAritmetico = ["+","-","*","/","++","--"]
    operadoresRelacionais = ["==","!=",">",">=","<","<=","="]
    operadorLogico = ["&&","||","!"]
    delimitadores = [";",",","(",")","{","}","[","]","."]
    symbolsTable = []
    
    def getToken(self,lexema): 
        tokens = []
        word = ''
        counter = 0
        charList = self.splitWord(lexema)#Transforma a linha em letras
        length = len(charList)
        
        while counter < length:
            if charList[counter].isspace(): # Verifica se é um espaço
                counter += 1
            elif charList[counter].isidentifier(): # Verifica se é um caracter
                while charList[counter].isidentifier():
                    word += charList[counter]
                    counter += 1
                    if counter==length:
                        break    
                if self.reservedWords.__contains__(word):
                    tokens.append("<Palavra Reservada, "+word+">")
                else:
                    tokens.append("<ID, "+word+">")
                if not self.symbolsTable.__contains__(word):
                    self.symbolsTable.append(word)
                word = ''                  
            elif charList[counter].isnumeric(): # Verifica se é um número
                while charList[counter].isnumeric():
                    word += charList[counter]
                    counter += 1
                    if counter==length:
                        break
                if word.isnumeric():
                    tokens.append("<Número, "+word+">")
                elif word.isdigit():
                    tokens.append("<Digito, "+word+">")
                word = '' 
            else: # Se não for número, letra ou espaço, será um simbolo
                if charList[counter]=="\"":#FALTA VER STRINGS DE VARIAS LINHAS
                    word+=charList[counter]
                    counter+=1
                    #and charList[counter]!="\n"
                    while charList[counter]!="\"":
                        word += charList[counter]
                        counter += 1
                        if counter==length:
                            break
                    word+=charList[counter]
                    counter+=1
                    tokens.append("<Cadeia de Caracteres>, "+word+">")
                elif charList[counter]=="/" and charList[counter+1]=="/":
                    while charList[counter]!="\n":
                        counter+=1
                elif charList[counter]=="/" and charList[counter+1]=="*":
                    while charList[counter]!="*" and charList[counter+1]!="/":
                        counter+=1
                else:
                    word+=charList[counter]
                    tokens.append("<Simbolo, "+word+">")
                    counter += 1
                word = ''
        for token in tokens:
            print(token)
        print(self.symbolsTable)
        return tokens
           
    def splitWord(self,lexema)->str:
        return [char for char in lexema]
        # return list(lexema)

if __name__ == "__main__": 
    cl = ClassifyLexema()
    arquivo = '''if (idade >= 150) print("pode aposenta
    r kkkk");
	else {
		print("vai trabalhar");
		salario = salario; // hehehe
        /* 
        asfasfasf
        */
	}
	'''
    cl.getToken(arquivo)
    # for linha in arquivo.splitlines():
    #     cl.getToken(linha)
    