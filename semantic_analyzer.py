from os import error


class SemanticAnalyzer():
    def __init__(self, tokens: list, table:list):
        self.tokens=tokens
        self.table=table
        self.erros=[]
    def findInTable(self,table,ide,scope):
        try:
            for item in table:
                if item.ide==ide and item.scope==scope:
                    raise OSError
        except OSError:
            self.erros.append(f"Identificador {ide} Duplicado")


    def findErrors(self):
        for indice in range(0,len(self.tokens)):
            if self.tokens[indice].getLexema() in {"var","const"}:
                while self.tokens[indice].getLexema() != "}":
                    if self.tokens[indice].getType()=="IDE":
                        self.findInTable(self.table["varTree"],self.tokens[indice].getLexema(),"global")
                        self.findInTable(self.table["constTree"],self.tokens[indice].getLexema(),"global")
                    indice+=1
            indice+=1
        print(self.erros)

