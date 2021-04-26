from iterator import MyIterator
from sintaxError import sintaxError
from generate_tokens import GenerateTokens

class Parser():
    type = {"int", "real", "string", "boolean"}
    terminalSymbols = {';', '}'}

    def __init__(self, tokens:list):
        self.tokens = tokens
        self.itr = MyIterator(tokens)
        self.current = 0
        self.sintaxErrors = []

    def sintaxParser(self) -> list:
            try:
                if self.itr.cur == None:
                    return self.getSintaxErrors()
                self.initProduction()
            except StopIteration:
                return self.getSintaxErrors()

    def initProduction(self) -> None:
        if (self.itr.cur.lexema) == "procedure": 
            self.itr.next()
            if self.itr.cur.lexema == "start":
                self.itr.next()
                if self.itr.cur.lexema == "{":
                    self.itr.next()
                    self.startProduction()
                else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, "start"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "procedure"))

    def startProduction(self) -> None:
        # print("startProduction")
        self.programProduction()
        if self.itr.cur != None:
            if self.itr.cur.lexema == "}":
                self.itr.next()
                return
            else:
                self.startProduction()

    def programProduction(self) -> None:
        # print("programProduction")
        self.statementProduction()

    def statementProduction(self) -> None:
        # print("statementProduction")
        if self.itr.cur.lexema == "typedef":
            self.itr.next()
            if self.itr.cur.lexema == "struct":
                self.itr.next()
                self.structProduction()
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, "struct"))
        else:
            self.itr.next()

    def structProduction(self) -> None:
        if self.itr.cur.lexema == "{":
            self.itr.next()
            self.varProduction()
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))
    
    def varProduction(self) -> None:
        if self.itr.cur.lexema == "var" or self.itr.cur.lexema == "const":
            self.itr.next()
            self.varDeclaration()
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "var or const"))


    def varDeclaration(self) -> None:
        if self.itr.cur.lexema == "{":
            self.itr.next()
            if self.type.__contains__(self.itr.cur.lexema):
                self.itr.next()
                self.ideVar()
                if self.itr.cur.lexema == "}":
                    self.itr.next()
                    if self.itr.cur.type == "IDE":
                        self.itr.next()
                        if self.itr.cur.lexema == ";":
                            self.itr.next()
                            return
                        else:
                            self.sintaxErrors.append(sintaxError(self.itr.cur, ";"))
                    else:
                        self.sintaxErrors.append(sintaxError(self.itr.cur, "IDE"))
                else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "}"))
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, str(self.type)))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))
                

    def ideVar(self) -> None:
        if self.itr.cur.type == "IDE":
            self.itr.next()
            if self.itr.cur.lexema == ",":
                self.itr.next()
                self.ideVar()
            elif self.itr.cur.lexema == ";":
                self.itr.next()
                return
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, ", ou ;"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "IDE"))

    def getSintaxErrors(self) -> list:
        return self.sintaxErrors

if __name__ == "__main__":
    codigoFonte = '''  procedure start { typedef struct { var { int roberto, daniel;} teste;  }} '''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = Parser(tokens)
    sintaxParser.sintaxParser()
    sErrors = sintaxParser.getSintaxErrors()
    for i in sErrors:
        print(i)
    print("Análise sintática finalizada!")
