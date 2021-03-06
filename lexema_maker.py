class LexemaMaker():
   
    def makeLexema(self,code):
        lexemas = code.splitlines()
        # for line in code.splitlines(): # Dividir código fonte em linhas
        #     lexemas+= self.__splitSpaces(line)
        return lexemas
        
    # def __splitSpaces(self,line):
    #     withoutSpaces = line.replace(" ", "\s") # Substituir espaços por \s
    #     return withoutSpaces.split("\s")# Separar em lexemas de acordo com o \s

if __name__ == "__main__": 
    lex = LexemaMaker()
    print(lex.makeLexema("\"teste de string \n Roberto"))