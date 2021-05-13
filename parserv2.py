from typing import List
from iterator import MyIterator
from sintaxError import sintaxError
from generate_tokens import GenerateTokens

# Conjunto comum de tokens de sincronização
COMMOM_FOLLOW = {}

# Conjunto de sincronização específicos
IF_FOLLOW = {}
ELSE_FOLLOW = {}
STRUCT_FOLLOW = {}
WHILE_FOLLOW = {}

# olhar o próximo, se for o que se espera, consome, diz q deu erro ||

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
            "if": self.ifProduction,
            #  "print": self.printProduction,
            "function": self.functionProcedure,
            "var" or "const": self.varProduction,
            #  "}": self.nextToken,
        }
        

    def sintaxParser(self) -> list:
        self.initProduction()
        return self.getSintaxAnalisys()

    def initProduction(self) -> None:
        if self.nextToken('procedure'):
            if self.nextToken('start'):
                self.startProduction()
                   

    def startProduction(self) -> None:
        self.statementProduction()
    
    def statementProduction(self) -> None:
        if self.nextToken('{'):
            statement = self.statement_dict[self.itr.cur.lexema]
            statement()
            self.nextToken('}')
    
    def structProduction(self) -> None:
        self.nextToken('typedef')
        if self.nextToken('struct'):
            if self.nextToken('{'):
                self.varProduction()
                self.nextToken('}')
                    
    def whileProduction(self) -> None:
        self.nextToken('while')
        self.expressionProduction()
        self.statementProduction()

    def ifProduction(self) -> None:
        self.nextToken('if')           
        self.expressionProduction()      
        self.statementProduction()     
        if self.itr.cur.lexema == 'else':
            self.elseStatement()

    def elseStatement(self) -> None:
        self.nextToken('else')
        self.statementProduction()

    def functionProcedure(self) -> None:
        if self.itr.cur.lexema == 'procedure':
            self.nextToken('procedure')
            self.procedureBody()
        elif self.itr.cur.lexema == 'function':
            self.nextToken('function')
            if self.itr.cur.lexema in self.typeOf:
                self.nextToken(self.itr.cur.lexema)
                self.functionBody()
            
    def procedureBody(self) -> None:
        if self.itr.cur.type == "IDE":
            self.nextToken(self.itr.cur.lexema)
            self.paramsProduction()
            self.statementProduction()
    
    def functionBody(self) -> None:
        if self.itr.cur.type == "IDE":
            self.nextToken(self.itr.cur.lexema)
            self.paramsProduction()
            self.statementProduction()
            # self.returnProcedure()

    def expressionProduction(self) -> None:
        if self.nextToken('('):
            self.orExpression()
            self.nextToken(')') 

    def orExpression(self) -> None:
        self.andExpression()
        if self.itr.cur.lexema=="||":
            self.nextToken("||")
            self.orExpression()

    def andExpression(self) -> None:
        self.equalityExpression()
        if self.itr.cur.lexema=="&&":
            self.nextToken("&&")
            self.andExpression()
    
    def equalityExpression(self) -> None:
        equality = {"==", "!="}
        self.compareExpression()
        if self.itr.cur.lexema in equality:
            self.nextToken(self.itr.cur.lexema)
            self.equalityExpression()

    def compareExpression(self) -> None:
        compare = {">", "<",">=","<="}
        self.addExpression()
        if self.itr.cur.lexema in compare:
            self.nextToken(self.itr.cur.lexema)
            self.compareExpression()

    def addExpression(self) -> None:
        add = {"+", "-"}
        self.multiplicationExpression()
        if self.itr.cur.lexema in add:
            self.nextToken(self.itr.cur.lexema)
            self.addExpression()

    def multiplicationExpression(self) -> None:
        exp = {"*", "/"}
        self.notExpression()
        if self.itr.cur.lexema in exp:
            self.nextToken(self.itr.cur.lexema)
            self.multiplicationExpression() 

    def notExpression(self) -> None:
        exp = {"IDE","NRO","CAD","true","false"}
        if self.itr.cur.lexema == "!":
            self.nextToken(self.itr.cur.lexema)
            self.notExpression()
        elif self.itr.cur.lexema == "(":
            self.expressionProduction()
        elif self.itr.cur.type in exp:
            self.nextToken(self.itr.cur.lexema)
        else:
            self.sintax_analisys.append(sintaxError(self.itr.cur,"valid expression"))
            self.itr.next()
                   
    def paramsProduction(self) -> None: # Deveria retornar true ou false? caso de erro
        if self.nextToken('('):
            self.params()
            self.nextToken(')')

    def params(self) -> None:
        if self.itr.cur.lexema in self.typeOf:
            self.nextToken(self.itr.cur.lexema)
            if self.itr.cur.type == 'IDE':
                self.nextToken(self.itr.cur.lexema)
                if self.itr.cur.lexema == ',':
                    self.nextToken(',')
                    self.params()

    def varProduction(self) -> None:
        if self.itr.cur.lexema in self.variable:
            self.nextToken(self.itr.cur.lexema)
            if self.nextToken('{'):
                self.varDeclaration()

    def varDeclaration(self) -> None:
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
                if self.itr.cur.type == 'IDE':
                    self.sintax_analisys.append(sintaxError(self.itr.cur, ","))
                    self.itr.next()
                elif self.itr.cur.lexema == '}':
                    self.sintax_analisys.append(sintaxError(self.itr.cur, ";"))
                # elif self.itr.cur.lexema in self.typeOf:
                #     self.sintax_analisys.append(sintaxError(self.itr.cur, ";"))
                #     self.varDeclaration()

    def nextToken(self, lexema) -> bool:
        # balanceamento de {}, para indicar se ficou faltando fechar algo
        if self.itr.cur != None:
            self.bracketsBalance()
            if self.itr.cur.lexema == lexema:
                self.sintax_analisys.append(self.itr.cur)
                self.itr.next()
                return True
            else:
                self.sintax_analisys.append(sintaxError(self.itr.cur, lexema))
                self.itr.next()
                # self.panicState()
                return False
    
    def panicState(self, follow): # Follow é a variável global que guarda os tokens de sincronização
        while self.itr.cur.lexema not in follow:
            # balanceamento de {}, para indicar se ficou faltando fechar algo
            self.bracketsBalance()
            self.itr.next()
            if self.itr.cur == None:
                break
        if self.itr.cur == None:
            return
        else:  
            self.statementProduction()
    
    def bracketsBalance(self) -> None:
        if self.itr.cur.lexema == '{':
            self.brackets_stack.append(self.itr.cur)
        elif self.itr.cur.lexema == '}':
            self.brackets_stack.pop()

    def getSintaxAnalisys(self) -> list:
        return self.sintax_analisys

if __name__ == "__main__":
    codigoFonte = '''procedure start {
        if (a>b){
            var {
                int a; 
            }
        }    
    }'''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = ParserV2(tokens)
    result = sintaxParser.sintaxParser()
    for i in result:
        print(i)
    print("Análise sintática finalizada!")