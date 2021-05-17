from typing import List
from iterator import MyIterator
from sintax_error import SintaxError
from generate_tokens import GenerateTokens

class Parser():
    typeOf = {"int", "real", "string", "boolean"}
    variable = {"const", "var"}
    def __init__(self, tokens: list):
        self.itr = MyIterator(tokens)
        self.sintax_analisys = [] # guarda os erros e sucessos do analisador sintático
        self.brackets_stack = [] # balanceamento de { }
        self.statement_dict = {
            "read": self.readProduction,
            "print": self.printStatement,
            "read":self.readStatement,
            "local": self.varScoped,
            "global": self.varScoped,
            "function": self.functionProcedure,
            "procedure": self.functionProcedure,
            "typedef": self.structProduction,
            "var": self.varProduction,
            "const": self.varProduction,
            "if": self.ifProduction,
            "while": self.whileProduction,
        }
        
    def sintaxParser(self) -> list:
        self.initProduction()
        return self.getSintaxAnalisys()

    def initProduction(self) -> None: # Funcionando corretamente
        if self.nextToken('procedure'):
            if self.nextToken('start'):
                if self.nextToken('{'):
                    self.statementProduction()
                    self.nextToken('}')
                   
    def statementProduction(self) -> None: # Funcionando corretamente
        self.statementList()
    
    def statementList(self) -> None: # Funcionando corretamente
        if self.itr.cur != None:
            if self.itr.cur.type == 'IDE':
                if self.itr.nxt.lexema == '(':
                    self.callFunction()
                    self.nextToken(';')
                else:
                    self.varUsage()
                self.statementList()
            elif self.itr.cur.lexema in self.statement_dict:
                statement = self.statement_dict[self.itr.cur.lexema]
                statement()
                self.statementList()

    def structProduction(self) -> None: # Funcionando corretamente
            self.nextToken('typedef')
            if self.nextToken('struct'):
                if self.itr.cur.lexema == 'extends':
                    self.nextToken()
                    if self.itr.cur.type == "IDE":
                        self.nextToken()
                    else:
                        self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
                if self.nextToken('{'):
                    self.varProduction()
                    self.nextToken('}')
                    if self.itr.cur.type == 'IDE':
                        self.nextToken()
                    else:
                        self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
                    self.nextToken(';')
                    

                    
    def whileProduction(self) -> None: # Funcionando corretamente
        self.nextToken('while')
        if self.nextToken('('):
            self.expressionProduction()
            self.nextToken(')')
        if self.nextToken('{'):
            self.statementProduction()
            self.nextToken('}')

    def printStatement(self)->None: # Funcionando corretamente
        self.nextToken('print')           
        if self.nextToken('('):
            self.printProduction()
            self.nextToken(')')
        self.nextToken(";")

    def printProduction(self)->None: # Funcionando corretamente
        if self.itr.cur.type == "IDE":
            self.nextToken()
            if self.itr.cur.lexema == '.':
                self.structUsage()
                self.moreExpressions()
            elif self.itr.cur.lexema == '[':
                self.arrayUsage()
                self.moreExpressions()
            else:
                self.moreExpressions()
        elif self.itr.cur.type == "CAD":
            self.nextToken()
            self.moreExpressions()
        elif self.itr.cur.lexema ==")":
            return
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid arguments"))
            self.itr.next()

    def moreExpressions(self)->None: # Funcionando corretamente
        if self.itr.cur.lexema==",":
            self.nextToken()
            self.printProduction()

    def structUsage(self)-> None: # Funcionando corretamente
        if self.itr.cur.lexema == '.':
            self.nextToken()
            if self.itr.cur.type == "IDE":
                self.nextToken()

    def arrayUsage(self)-> None: # Funcionando corretamente
        exp = {"IDE","NRO","CAD","true","false"}
        if self.nextToken('['):
            if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                self.nextToken()
                self.nextToken(']')
                if self.itr.cur.lexema == '[':
                    self.nextToken()
                    if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                        self.nextToken()
                        self.nextToken(']')
                    else:
                        self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid expressions"))
                        self.itr.next()
            else:
                self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid expressions"))
                self.itr.next()
               
    def readStatement(self)->None: # Funcionando corretamente
        self.nextToken('read')           
        if self.nextToken('('):
            self.readProduction()
            self.nextToken(')')
        self.nextToken(";")

    def readProduction(self)->None: # Funcionando corretamente
        if self.itr.cur.type == "IDE":
            self.nextToken()
            if self.itr.cur.lexema == '.':
                self.structUsage()
                self.moreReadings()
            elif self.itr.cur.lexema == '[':
                self.arrayUsage()
                self.moreReadings()
            else:
                self.moreReadings()
        elif self.itr.cur.lexema ==")":
            return
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid read"))
            self.itr.next()

    def moreReadings(self)->None: # Funcionando corretamente
        if self.itr.cur.lexema==",":
            self.nextToken()
            self.readProduction()

    def ifProduction(self) -> None: # Funcionando corretamente
        self.nextToken('if')           
        if self.nextToken('('):
            self.expressionProduction()
            self.nextToken(')')
        self.nextToken('then')      
        if self.nextToken('{'):
            self.statementProduction()
            self.nextToken('}')    
        if self.itr.cur.lexema == 'else':
            self.elseStatement()

    def elseStatement(self) -> None: # Funcionando corretamente
        self.nextToken()
        if self.nextToken('{'):
            self.statementProduction()
            self.nextToken('}')

    def functionProcedure(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema == 'procedure':
            self.nextToken()
            self.procedureBody()
        elif self.itr.cur.lexema == 'function':
            self.nextToken()
            if self.itr.cur.lexema in self.typeOf:
                self.nextToken()
                self.functionBody()
            
    def procedureBody(self) -> None: # Funcionando corretamente
        if self.itr.cur.type == "IDE":
            self.nextToken()
            self.paramsProduction()
            if self.nextToken('{'):
                self.statementProduction()
                self.nextToken('}')
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
            self.itr.next()
        
    
    def functionBody(self) -> None: # Funcionando corretamente
        if self.itr.cur.type == "IDE":
            self.nextToken()
            self.paramsProduction()
            if self.nextToken('{'):
                self.statementProduction()
                self.returnProduction()
                self.nextToken('}')
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
            self.itr.next()

    def expressionProduction(self) -> None: 
        self.orExpression()

    def orExpression(self) -> None:
        self.andExpression()
        if self.itr.cur.lexema=="||":
            self.nextToken()
            self.orExpression()

    def andExpression(self) -> None:
        self.equalityExpression()
        if self.itr.cur.lexema=="&&":
            self.nextToken()
            self.andExpression()
    
    def equalityExpression(self) -> None:
        equality = {"==", "!="}
        self.compareExpression()
        if self.itr.cur.lexema in equality:
            self.nextToken()
            self.equalityExpression()

    def compareExpression(self) -> None:
        compare = {">", "<",">=","<="}
        self.addExpression()
        if self.itr.cur.lexema in compare:
            self.nextToken()
            self.compareExpression()

    def addExpression(self) -> None:
        add = {"+", "-"}
        self.multiplicationExpression()
        if self.itr.cur.lexema in add:
            self.nextToken()
            self.addExpression()

    def multiplicationExpression(self) -> None:
        exp = {"*", "/"}
        self.notExpression()
        if self.itr.cur.lexema in exp:
            self.nextToken()
            self.multiplicationExpression() 

    def notExpression(self) -> None:
        exp = {"IDE","NRO","CAD","true","false"}
        if self.itr.cur.lexema == "!":
            self.nextToken()
            self.notExpression()
        elif self.itr.cur.lexema == "(":
            self.nextToken()
            self.expressionProduction()
            self.nextToken(')')
        elif self.itr.cur.type in exp or self.itr.cur.lexema in exp:
            self.nextToken()
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid expression"))
            self.itr.next()
                   
    def paramsProduction(self) -> None: # Funcionando corretamente
        if self.nextToken('('):
            self.params()
            self.nextToken(')')

    def params(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema in self.typeOf:
            self.nextToken()
            if self.itr.cur.type == 'IDE':
                self.nextToken()
                if self.itr.cur.lexema == ',':
                    self.nextToken()
                    self.params()
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid param"))
            self.itr.next()

    def callFunction(self) -> None: # Funcionando corretamente
        if self.itr.cur.type == 'IDE':
            self.nextToken()
            if self.nextToken('('):
                self.args()
                self.nextToken(')')
                

    def args(self) -> None: # Funcionado corretamente
        exp = {"IDE","NRO","CAD","true","false"}
        if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
            self.nextToken()
            if self.itr.cur.lexema == ",":
                self.nextToken()
                self.args()

    def returnProduction(self) -> None:  # Funcionando corretamente
        exp = {"NRO","CAD","true","false"}
        if self.nextToken('return'):
            if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                self.nextToken()
            elif self.itr.cur.type == 'IDE':
                if self.itr.nxt.lexema == "(":
                    self.callFunction()
                else:
                    self.expressionProduction()
            elif self.itr.cur.lexema == '(':
                self.nextToken()
                self.expressionProduction()
                self.nextToken(')')
            else:
                self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid return"))
                self.itr.next()
            self.nextToken(';')

    
    def varProduction(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema == 'var':
            self.nextToken()
            if self.nextToken('{'):
                self.varDeclaration()
                self.nextToken('}')
                self.varProduction()
        elif self.itr.cur.lexema == 'const':
            self.nextToken()
            if self.nextToken('{'):
                self.constDeclaration()
                self.nextToken('}')
                self.varProduction()
        

    def varDeclaration(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema in self.typeOf:
            self.nextToken()
            self.variables()
            self.nextToken(';')
            self.varDeclaration()
        elif self.itr.cur.lexema == '}':
            return
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid type"))

    def variables(self) -> None: # Funcionando corretamente
        if self.itr.cur.type == 'IDE':
            self.nextToken()
            if self.itr.cur.lexema == '=':
                self.nextToken()
                if self.itr.cur.type == 'IDE':
                    if self.itr.nxt.lexema == '(':
                        self.callFunction()
                    elif self.itr.nxt.lexema == '.':
                        self.nextToken()
                        self.structUsage()
                    elif self.itr.nxt.lexema == '[':
                        self.nextToken()
                        self.arrayUsage()
                    else:
                        self.expressionProduction()
                elif self.itr.cur.lexema in {'local','global'}:
                        self.nextToken()
                        self.nextToken('.')
                        if self.itr.cur.type == 'IDE':
                            self.nextToken()
                            if self.itr.cur.lexema == '[':
                                self.arrayUsage()
                else:
                    self.expressionProduction()
            elif self.itr.cur.lexema == '[':
                self.arrayUsage()
                if self.itr.cur.lexema == '=':
                    self.nextToken()
                    if self.itr.cur.lexema == '{':
                        self.nextToken()
                        self.varArg()
                        self.nextToken('}')
                    elif self.itr.cur.lexema in {'local','global'}:
                        self.nextToken()
                        self.nextToken('.')
                        if self.itr.cur.type == 'IDE':
                            self.nextToken()
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
            self.itr.next()
        if self.itr.cur.lexema == ',':
            self.nextToken()
            self.variables()

    def varArg(self) -> None: # Funcionando corretamente
        exp = {'IDE','NRO','CAD','true','false'}
        if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
            self.nextToken()
            if self.itr.cur.lexema == ',':
                self.nextToken()
                self.varArg()
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid values"))
            self.itr.next()

    
    def varUsage(self) -> None: # Funcionando corretamente
        exp = {'IDE','NRO','CAD','true','false'}
        if self.itr.cur.type == 'IDE':
            if self.itr.nxt.lexema == '.':
                self.nextToken()
                self.structUsage()
                if self.itr.cur.lexema == '=':
                    self.nextToken()
                    if self.itr.cur.type == 'IDE':
                        if self.itr.nxt.lexema == '(':
                            self.callFunction()
                        elif self.itr.nxt.lexema == '.':
                            self.nextToken()
                            self.structUsage()
                        elif self.itr.nxt.lexema == '[':
                            self.nextToken()
                            self.arrayUsage()
                        else:
                            self.expressionProduction()
                    elif self.itr.cur.lexema in {'global', 'local'}:
                        self.nextToken()
                        self.nextToken('.')
                        if self.itr.cur.type == 'IDE':
                            self.nextToken()
                            if self.itr.cur.lexema == '[':
                                self.arrayUsage()
                        else:
                            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
                    else:
                        self.expressionProduction()
            elif self.itr.nxt.lexema == '[':
                self.nextToken()
                self.arrayUsage()
                if self.itr.cur.lexema == '=':
                    self.nextToken()
                    if self.itr.cur.type == 'IDE':
                        if self.itr.nxt.lexema == '.':
                            self.nextToken()
                            self.structUsage()
                        elif self.itr.nxt.lexema == '[':
                            self.nextToken()
                            self.arrayUsage()
                    if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                        self.nextToken()
                    elif self.itr.cur.lexema in {'global', 'local'}:
                        self.nextToken()
                        self.nextToken('.')
                        if self.itr.cur.type == 'IDE':
                            self.nextToken()
                        else:
                            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
            else:
                self.variables()
            self.nextToken(';')

    def varScoped(self) -> None: # Funcionando corretamente
        self.nextToken()
        self.nextToken('.')
        self.variables()
        self.nextToken(';')

    def constDeclaration(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema in self.typeOf:
            self.nextToken()
            self.constants()
            self.nextToken(';')
            self.constDeclaration()
    
    def constants(self) -> None: # Funcionando corretamente
        exp = {'IDE','NRO','CAD','true','false'}
        if self.itr.cur.type == 'IDE':
            self.nextToken()
            if self.nextToken('='):
                if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                    self.nextToken()
                    if self.itr.cur.lexema == ',':
                        self.nextToken()
                        self.constants()
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))

    def nextToken(self, lexema = None) -> bool:
        # balanceamento de {}, para indicar se ficou faltando fechar algo
        if self.itr.cur != None:
            # self.bracketsBalance()
            if self.itr.cur.lexema == lexema or lexema == None:
                self.sintax_analisys.append(self.itr.cur)
                self.itr.next()
                return True
            else:
                self.sintax_analisys.append(SintaxError(self.itr.cur, lexema))
                self.itr.next()
                return False
        else:
            self.sintax_analisys.append(f'Erro de sintaxe no final do arquivo: Expected:"{lexema}", got "None"')

    def bracketsBalance(self) -> None:
        if self.itr.cur.lexema == '{':
            self.brackets_stack.append(self.itr.cur)
        elif self.itr.cur.lexema == '}':
            self.brackets_stack.pop()

    def getSintaxAnalisys(self) -> list:
        return self.sintax_analisys

if __name__ == "__main__":
    codigoFonte = '''procedure start {
        if(a*b == c) then{
            function int teste(string a, int b){
                return a;
            }
        }
        else{
            typedef struct extends pessoa{
                var { string nome = "roberto", sobrenome = "maia"; int idade = 17;}
                const { string sexo = "M";}
            }pessoa;
        }
        while(a < b){
            print("roberto");
            a = a+1;
        }
}'''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = Parser(tokens)
    result = sintaxParser.sintaxParser()
    for i in result:
        print(i)


# Testar todas possibilidades de variáveis | OKAY
# Testar todas as produções 
# Tentar modificar o nextToken
# Fazer erros para cada situação