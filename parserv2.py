from typing import List
from iterator import MyIterator
from sintaxError import sintaxError
from generate_tokens import GenerateTokens

class ParserV2():
    typeOf = {"int", "real", "string", "boolean"}
    variable = {"const", "var"}
    
    def __init__(self, tokens: list):
        self.itr = MyIterator(tokens)
        self.sintax_analisys = [] # guarda os erros e sucessos do analisador sintático
        self.brackets_stack = [] # balanceamento de { }
        self.statement_dict = {
            "typedef": self.structProduction,
            "while": self.whileProduction,
            #  "if": self.ifProduction,
            #  "else": self.elseProduction, # Não deveria estar aqui
            #  "print": self.printProduction,
            #  "function": self.functionDeclProduction,
            "var" or "const": self.varProduction,
            #  "}": self.nextToken,
        }

    def sintaxParser(self) -> list:
        self.initProduction()
        return self.getSintaxAnalisys()

    def initProduction(self) -> None:
        if self.nextToken('procedure'):
            if self.nextToken('start'):
                if self.nextToken('{'):
                    self.startProduction()
                    self.nextToken('}')
        else:
            self.panicState() # como fazer o loop e como onde usar o estado de pânico

    def startProduction(self) -> None:
        self.statementProduction()
    
    def statementProduction(self) -> None:
        statement = self.statement_dict[self.itr.cur.lexema]
        statement()
    
    def statementBody(self) -> None:
        if self.nextToken('('):
            self.paramsProduction()
            if self.nextToken(')'):
                if self.nextToken('{'):
                    self.statementProduction()
                    self.nextToken('}')

    def structProduction(self) -> None:
        self.nextToken('typedef')
        if self.nextToken('struct'):
            if self.nextToken('{'):
                self.varProduction()
                if self.nextToken('}'):
                    return

    def whileProduction(self) -> None:
        self.nextToken('while')
        if self.nextToken('('):
            #self.expressionProduction()
            if self.nextToken(')'):
                if self.nextToken('{'):
                    # self.statementProduction()
                    self.nextToken('}')
                    return

    def ifProduction(self) -> None:
        self.nextToken('if')
        if self.nextToken('('):             # Transformar
            # self.expressionProduction()   # em uma única
            if self.nextToken(')'):         # função
                if self.nextToken('{'):     #  podendo utilizar 
                    # self.statementProduction() # no while, no if e outros
                    if self.nextToken('}'): #
                        if self.itr.cur.lexema == 'else':
                            self.elseStatement()
                        else:
                            return

    def elseStatement(self) -> None:
        self.nextToken('else')
        if self.nextToken('{'):
            # self.statementProduction()
            self.nextToken('}')
            return
            

    def varProduction(self) -> None:
        if self.itr.cur.lexema in self.variable:
            self.nextToken(self.itr.cur.lexema)
            self.varDeclaration()

    def varDeclaration(self) -> None:
        if self.nextToken('{'):
            if self.itr.cur.lexema in self.typeOf:
                while self.typeOf.__contains__(self.itr.cur.lexema):
                    self.nextToken(self.itr.cur.lexema)
                    self.ideVar()
                    if self.nextToken('}'):
                        if self.itr.cur.lexema in self.variable:
                            self.varProduction()

    # com erro
    def ideVar(self) -> None:
        if self.itr.cur.type == "IDE":
            self.nextToken(self.itr.cur.lexema)
            if self.itr.cur.lexema == ',':
                self.nextToken(',')
                self.ideVar()
            elif self.itr.cur.lexema == ';':
                self.nextToken(';')
            else:
                self.sintax_analisys.append(sintaxError(self.itr.cur, ", ou ;"))
                self.panicState()

    def nextToken(self, lexema) -> bool:
        if self.itr.cur != None:
            if self.itr.cur.lexema == lexema:
                self.sintax_analisys.append(self.itr.cur)
                if self.itr.cur.lexema == '{':
                    self.brackets_stack.append(self.itr.cur)
                elif self.itr.cur.lexema == '}':
                    self.brackets_stack.pop()
                self.itr.next()
                return True
            else:
                self.sintax_analisys.append(sintaxError(self.itr.cur, lexema))
                self.itr.next()
                # self.panicState()
                return False
    
    def panicState(self):
        while self.itr.cur.lexema not in self.statement_dict:
            self.itr.next()
            if self.itr.cur == None:
                break
        if self.itr.cur == None:
            return
        else:  
            self.statementProduction()
    
    def getSintaxAnalisys(self) -> list:
        return self.sintax_analisys

if __name__ == "__main__":
    codigoFonte = '''procedure start {
         var{ int roberto }
        const { string teste, teste2;}
    }'''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = ParserV2(tokens)
    result = sintaxParser.sintaxParser()
    for i in result:
        print(i)
    print("Análise sintática finalizada!")