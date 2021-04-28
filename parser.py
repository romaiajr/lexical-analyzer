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
                self.nextToken()
                self.startProduction()

    # def programProduction(self) -> None:
    #     self.statementProduction()

    def statementProduction(self) -> None:
        if self.itr.cur.lexema == "typedef": # STRUCT
            self.nextToken()
            self.structProduction()
        elif self.itr.cur.lexema == "while": # WHILE
            self.nextToken()
            self.whileProduction()
        elif self.itr.cur.lexema == "if": # IF - THEN - ELSE
            self.nextToken()
            self.ifProduction()
        elif self.itr.cur.lexema == "print": # PRINT
            self.nextToken()
            self.printProduction()
        elif self.itr.cur.lexema == "function": # FUNCTION or PROCEDURE DECL
            self.nextToken()
            self.functionDeclProduction()
        elif self.itr.cur.type == "IDE": # VAR ATR or FUNCTION CALL
            self.nextToken()
        elif self.itr.cur.lexema == "const" or self.itr.cur.lexema == "var": # VAR DECL
            self.nextToken()
            self.varProduction()
        elif self.itr.cur.lexema == "}":
            self.nextToken()
            return

    def structProduction(self) -> None:
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
                            self.sintaxErrors.append(sintaxError(self.itr.cur, ";"))
                    else:
                        self.sintaxErrors.append(sintaxError(self.itr.cur, "IDE"))
                else:
                    self.sintaxErrors.append(sintaxError(self.itr.cur, "}"))
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, "{"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "struct"))
    
    def whileProduction(self) -> None:
        if self.itr.cur.lexema == "(":
            self.nextToken()
            #self.expressionProduction()
            if self.itr.cur.lexema == ")":
                self.nextToken()
                self.statementProduction()
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, ")"))
        else:
            self.sintaxErrors.append(sintaxError(self.itr.cur, "("))
       
    
    def varProduction(self) -> None:
        if self.itr.cur.lexema == "const" or self.itr.cur.lexema == "var":
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
                        if self.itr.cur.lexema == "const" or self.itr.cur.lexema == "var":
                            self.varProduction()
            else:
                self.sintaxErrors.append(sintaxError(self.itr.cur, str(self.type)))
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

if __name__ == "__main__":
    codigoFonte = '''
    procedure start { 
        while()
        typedef struct { 
            var { int roberto, daniel; boolean teste;} 
            const { int teste;} 
        }teste;
    } '''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = Parser(tokens)
    sintaxParser.sintaxParser()
    sErrors = sintaxParser.getSintaxErrors()
    for i in sErrors:
        print(i)
    print("Análise sintática finalizada!")
