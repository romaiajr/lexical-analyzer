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
            # "read": self.readProduction,
            "print": self.printStatement,
            # var usage
            # var scope
            "function": self.functionProcedure,
            "procedure": self.functionProcedure,
            "typedef": self.structProduction,
            "var": self.varProduction,
            "const": self.varProduction,
            # "IDE": self.callFunction, foi feito como um if no statement
            "if": self.ifProduction,
            "while": self.whileProduction,
            
        }
        

    def sintaxParser(self) -> list:
        self.initProduction()
        return self.getSintaxAnalisys()

    def initProduction(self) -> None: # Funcionando corretamente
        if self.nextToken('procedure'):
            if self.nextToken('start'):
                self.startProduction()
                   
    def startProduction(self) -> None:
        self.statementProduction()
    
    def statementProduction(self) -> None:
        if self.nextToken('{'):
            self.statementList()
            self.nextToken('}') # Não tá chegando aqui
    
    def statementList(self) -> None:
        if self.itr.cur != None:
            if self.itr.cur.type == 'IDE':
                self.callFunction()
                self.statementList()
            elif self.itr.cur.lexema in self.statement_dict:
                statement = self.statement_dict[self.itr.cur.lexema]
                statement()
                self.statementList()
        
    def structProduction(self) -> None: # Revisar
            self.nextToken('typedef')
            if self.nextToken('struct'):
                if self.nextToken('{'):
                    self.varProduction()
                    self.nextToken('}')
                    
    def whileProduction(self) -> None: # Funcionando corretamente
        self.nextToken('while')
        self.expressionProduction()
        self.statementProduction()

    def printStatement(self)->None:
        self.nextToken('print')           
        if self.nextToken('('):
            self.printProduction()
            self.nextToken(')')
        self.nextToken(";")

    def printProduction(self)->None:
        self.structUsage()
        #self.arrayUsage()
        if self.itr.cur.type == "IDE" or self.itr.cur.type == "CAD":
            self.nextToken(self.itr.cur.lexema)
            self.moreExpressions()
        elif self.itr.cur.lexema ==")":
            return
        else:
            self.sintax_analisys.append(sintaxError(self.itr.cur,"Valid print"))
            self.itr.next()

    def structUsage(self)-> None:
        #print(self.itr.nxt)
        #and self.itr.nxt == '.'
        if self.itr.cur.type == "IDE" and self.itr.nxt.lexema == '.':
            self.nextToken(self.itr.cur.lexema)
            if self.itr.cur.lexema == '.':
                self.nextToken(self.itr.cur.lexema)
                if self.itr.cur.type == "IDE":
                    self.nextToken(self.itr.cur.lexema)
                    self.moreExpressions()

    def arrayUsage(self)-> None:
        #print(self.itr.nxt)
        exp = {"IDE","NRO","CAD","true","false"}
        if self.itr.cur.type == "IDE" and self.itr.nxt.lexema == '[':
            self.nextToken(self.itr.cur.lexema)
            if self.nextToken('['):
                if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                    self.nextToken(self.itr.cur.lexema)
                # else:
                #     self.sintax_analisys.append(sintaxError(self.itr.cur,"IDE"))
                self.nextToken(']')
                if self.nextToken('['):
                    if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                        self.nextToken(self.itr.cur.lexema)
                    # else:
                    #     self.sintax_analisys.append(sintaxError(self.itr.cur,"IDE"))
                self.nextToken(']')
            self.moreExpressions()
                
    def moreExpressions(self)->None:
        #print(self.itr.cur.lexema)
        if self.itr.cur.lexema==",":
            self.nextToken(self.itr.cur.lexema)
            self.printProduction()
        # elif self.itr.cur.lexema != ")":
        #     return

    def ifProduction(self) -> None: # Funcionando corretamente
        self.nextToken('if')           
        self.expressionProduction()      
        self.statementProduction()     
        if self.itr.cur.lexema == 'else':
            self.elseStatement()

    def elseStatement(self) -> None: # Funcionando corretamente
        self.nextToken('else')
        self.statementProduction()

    def functionProcedure(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema == 'procedure':
            self.nextToken('procedure')
            self.procedureBody()
        elif self.itr.cur.lexema == 'function':
            self.nextToken('function')
            if self.itr.cur.lexema in self.typeOf:
                self.nextToken(self.itr.cur.lexema)
                self.functionBody()
            
    def procedureBody(self) -> None: # Funcionando corretamente
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
        elif self.itr.cur.type in exp or self.itr.cur.lexema in exp:
            self.nextToken(self.itr.cur.lexema)
        else:
            self.sintax_analisys.append(sintaxError(self.itr.cur,"valid expression"))
            self.itr.next()
                   
    def paramsProduction(self) -> None: # Funcionando corretamente
        if self.nextToken('('):
            self.params()
            self.nextToken(')')

    def params(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema in self.typeOf:
            self.nextToken(self.itr.cur.lexema)
            if self.itr.cur.type == 'IDE':
                self.nextToken(self.itr.cur.lexema)
                if self.itr.cur.lexema == ',':
                    self.nextToken(',')
                    self.params()

    def callFunction(self) -> None: # Funcionando corretamente
        if self.itr.cur.type == 'IDE':
            self.nextToken(self.itr.cur.lexema)
            if self.nextToken('('):
                self.args()
                self.nextToken(')')

    def args(self) -> None: # Funcionado corretamente
        exp = {"IDE","NRO","CAD","true","false"}
        if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
            self.nextToken(self.itr.cur.lexema)
            if self.itr.cur.lexema == ",":
                self.nextToken(self.itr.cur.lexema)
                self.args()

    def returnProduction(self) -> None:  # Funcionando corretamente
        exp = {"NRO","CAD","true","false"}
        if self.nextToken('return'):
            if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                self.nextToken(self.itr.cur.lexema)
            elif self.itr.cur.type == 'IDE':
                if self.itr.nxt.lexema == "(":
                    self.callFunction()
                else:
                    self.nextToken(self.itr.cur.lexema)
            elif self.itr.cur.lexema == '(':
                self.expressionProduction()
            self.nextToken(';')

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
            # self.bracketsBalance()
            if self.itr.cur.lexema == lexema:
                self.sintax_analisys.append(self.itr.cur)
                self.itr.next()
                return True
            else:
                self.sintax_analisys.append(sintaxError(self.itr.cur, lexema))
                self.itr.next()
                # self.panicState()
                return False
        else:
            self.sintax_analisys.append(f'Erro Léxico no final do arquivo: Expected:"{lexema}", got "None"')
    
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
        print(a.b,a[2]);  
        }
    '''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = ParserV2(tokens)
    result = sintaxParser.sintaxParser()
    for i in result:
        print(i)