class ClassifyLexema():
    
    def getToken(self,lexema):
        word = ''
        counter = 0
        char = self.splitWord(lexema)
        length = len(char)
        while counter < length:
            if char[counter].isspace():
                counter += 1
            elif char[counter].isidentifier():
                while char[counter].isidentifier():
                    word += char[counter]
                    counter += 1
                print(word + " é um identificador")
                word = ''                  
            elif char[counter].isnumeric():
                while char[counter].isnumeric():
                    word += char[counter]
                    counter += 1
                if word.isnumeric():
                    print(word + " é um número")
                elif word.isdigit():
                    print(word + " é um digíto")
                word = '' 
            else:           
                word += char[counter]
                print(char[counter] + " é um simbolo")
                counter += 1
                word = ''
           
    def splitWord(self,lexema):
        return [char for char in lexema]

if __name__ == "__main__": 
    cl = ClassifyLexema()
    cl.getToken("Roberto maia \" % $ 324")