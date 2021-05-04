# faz o if else, criação de função
from iterator import MyIterator
from sintaxError import sintaxError
from generate_tokens import GenerateTokens


class Parser():
    type = {"int", "real", "string", "boolean"}
    # Eu não sabia pra que servia esse Type ai de cima e usei uma cópia chamada typeOf
    typeOf = {"int", "real", "string", "boolean"}
    variable = {"const", "var"}

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.itr = MyIterator(tokens)
        self.current = 0
        self.sintaxErrors = []
        self.statement_dict = {
            "typedef": self.structProduction,
            "while": self.whileProduction,
            "if": self.ifProduction,
            "else": self.elseProduction,
            "print": self.printProduction,
            "function": self.functionDeclProduction,
            "var" or "const": self.varProduction,
            "}": self.nextToken,
        }

    def sintaxParser(self) -> list:
        try:
            if self.itr.cur == None:
                return self.getSintaxErrors()
            self.initProduction()
        except StopIteration:
            return self.getSintaxErrors()

    def initProduction(self) -> None:
        if (self.itr.cur.lexema) == "procedure":
            self.nextToken()
            if self.itr.cur.lexema == "start":
                self.nextToken()
                if self.itr.cur.lexema == "{":
                    self.nextToken()
                    self.startProduction()
                else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, "start"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "procedure"))

    def startProduction(self) -> None:
        self.statementProduction()
        if self.itr.cur != None:
            if self.itr.cur.lexema == "}":
                self.nextToken()
                return
            else:
                # self.nextToken()
                self.startProduction()

    def statementProduction(self) -> None:
        if self.itr.cur.type == "IDE":
            self.nextToken()
        else:
            statement = self.statement_dict[self.itr.cur.lexema]
            statement()

    def structProduction(self) -> None:
        self.nextToken()
        if self.itr.cur.lexema == "struct":
            self.nextToken()
            if self.itr.cur.lexema == "{":
                self.nextToken()
                self.varProduction()
                if self.itr.cur.lexema == "}":
                    self.nextToken()
                    if self.itr.cur.type == "IDE":
                        self.nextToken()
                        if self.itr.cur.lexema == ";":
                            self.nextToken()
                            self.statementProduction()
                        else:
                            self.sintaxErrors.append(
                                sintaxError(self.itr.cur, ";"))
                    else:
                        self.sintaxErrors.append(
                            sintaxError(self.itr.cur, "IDE"))
                else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "}"))
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "struct"))

    def whileProduction(self) -> None:
        self.nextToken()
        if self.itr.cur.lexema == "(":
            self.nextToken()
            # self.expressionProduction()
            if self.itr.cur.lexema == ")":
                self.nextToken()
                self.statementProduction()
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, ")"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "("))

    def varProduction(self) -> None:
        # self.nextToken()
        if self.itr.cur.lexema in self.variable:
            self.nextToken()
            self.varDeclaration()
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "const ou var"))

    def varDeclaration(self) -> None:
        if self.itr.cur.lexema == "{":
            self.nextToken()
            if self.type.__contains__(self.itr.cur.lexema):
                while self.type.__contains__(self.itr.cur.lexema):
                    self.nextToken()
                    self.ideVar()
                    if self.itr.cur.lexema == "}":
                        self.nextToken()
                        if self.itr.cur.lexema in self.variable:
                            self.varProduction()
            else:
                self.sintaxErrors.append(
                    sintaxError(self.itr.cur, str(self.type)))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))

    def ideVar(self) -> None:
        if self.itr.cur.type == "IDE":
            self.nextToken()
            if self.itr.cur.lexema == ",":
                self.nextToken()
                self.ideVar()
            elif self.itr.cur.lexema == ";":
                self.nextToken()
                return
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, ", ou ;"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "IDE"))

    def getSintaxErrors(self) -> list:
        return self.sintaxErrors

    def nextToken(self) -> None:
        self.sintaxErrors.append(self.itr.cur)
        self.itr.next()

    def ifProduction(self) -> None:
        self.nextToken()
        if self.itr.cur.lexema == "(":
            self.nextToken()
            if self.itr.cur.lexema == ")":
                self.nextToken()
                if self.itr.cur.lexema == "{":
                    self.nextToken()
                    self.statementProduction()
                    self.nextToken()
                    if self.itr.cur.lexema == "}":
                        self.nextToken()
                    else:
                        self.sintaxErrors.append(sintaxError(self.itr.cur, "}"))
                        self.nextToken()
                else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))     
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, ")"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "("))

    def elseProduction(self) -> None:
        self.nextToken()
        self.statementProduction()                    # self.nextToken()

    def printProduction(self) -> None:
        pass

    def functionDeclProduction(self) -> None:
        self.nextToken()
        if self.itr.cur.lexema in self.typeOf:
            self.nextToken()
            if self.itr.cur.type == "IDE":
                self.nextToken()
                if self.itr.cur.lexema == "(":
                    self.nextToken()
                    if self.itr.cur.lexema == ")":
                        self.nextToken()
                        self.statementProduction()                    # self.nextToken()
                    else:
                        self.sintaxErrors.append(sintaxError(self.itr.cur, ")"))
                else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "("))
            else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "IDE"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "Type"))


if __name__ == "__main__":
    codigoFonte = '''
    procedure start { 
        function real algo()
        if(){
            
        
        else
    } '''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = Parser(tokens)
    sintaxParser.sintaxParser()
    sErrors = sintaxParser.getSintaxErrors()
    for i in sErrors:
        print(i)
    print("Análise sintática finalizada!")
