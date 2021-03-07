class ClassifyLexema():
    reservedWords = ["var", "const", "typedef", "struct", "extends", "procedure",
    "function", "start", "return", "if", "else", "then", "while", "read","print", "int",
    "real", "boolean", "string", "true", "false",
    "global", "local"]
    symbolsTable = []
    
    def getToken(self,lexema): 
        tokens = []
        word = ''
        counter = 0
        charList = self.splitWord(lexema)
        length = len(charList)
        
        while counter < length:
            if charList[counter].isspace(): # Verifica se é um espaço
                counter += 1
            elif charList[counter].isidentifier(): # Verifica se é um caracter
                while charList[counter].isidentifier():
                    word += charList[counter]
                    counter += 1
                # for rw in reservedWords:
                #     if word == rw:
                #         tokens.append(word + " é uma palavra reservada")
                tokens.append(word + " é um identificador")
                self.symbolsTable.append(word)
                word = ''                  
            elif charList[counter].isnumeric(): # Verifica se é um número
                while charList[counter].isnumeric() and counter < length:
                    word += charList[counter]
                    counter += 1
                if word.isnumeric():
                    tokens.append(word + " é um número")
                elif word.isdigit():
                    tokens.append(word + " é um digíto")
                word = '' 
            else: # Se não for número, letra ou espaço, será um simbolo
                # //, /* ou "
                word += charList[counter]
                tokens.append(charList[counter] + " é um simbolo")
                counter += 1
                word = ''
        print(tokens)
        return tokens
           
    def splitWord(self,lexema)->str:
        return [char for char in lexema]
        # return list(lexema)

if __name__ == "__main__": 
    cl = ClassifyLexema()
    cl.getToken("Roberto maia \" % $ 324")