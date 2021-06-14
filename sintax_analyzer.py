from typing import List
from iterator import MyIterator
from sintax_error import SintaxError
from generate_tokens import GenerateTokens
from data_token import DataToken

class Parser():
    typeOf = {"int", "real", "string", "boolean"}
    variable = {"const", "var"}
    def __init__(self, tokens: list):
        self.itr = MyIterator(tokens)
        self.sintax_analisys = [] # guarda os erros e sucessos do analisador sintático
        self.brackets_stack = [] # balanceamento de { }
        self.notDeclaration = False
        self.statement_dict = {
            "read": self.readProduction,
            "print": self.printStatement,
            "read":self.readStatement,
            "local": self.varScoped,
            "global": self.varScoped,
            "typedef": self.structProduction,
            "if": self.ifProduction,
            "while": self.whileProduction,
        }
        self.global_dict = {
            "var": self.varProduction,  #
            "const": self.varProduction, #
            "function": self.functionProcedure, #
            "procedure": self.functionProcedure, #
        }
        self.main = False
        self.scope = 0 
        self.var_tree = []
        self.const_tree = []
        self.function_tree = []
        self.procedure_tree = []
        self.struct_tree = []
        self.data ={"lexema": "-", "type":"-", "initialized":"-", "scope":"-", "params":"-"}
        
    def sintaxParser(self) -> list:
        self.initProduction()
        return self.getSintaxAnalisys()

    def initProduction(self) -> None: # Funcionando corretamente
        while self.itr.cur.lexema in self.global_dict:
            statement = self.global_dict[self.itr.cur.lexema]
            statement()
            if self.itr.cur == None:
                break
        if self.main == False:
            self.sintax_analisys.append("Erro de sintaxe no final do arquivo: Missing procedure start.")


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
                    self.scope += 1
                    self.varProduction()
                    self.nextToken('}')
                    if self.itr.cur.type == 'IDE':
                        self.data['lexema'] = self.itr.cur.lexema
                        self.data['scope'] = f"local {self.scope}"
                        self.nextToken()
                    else:
                        self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
                    self.nextToken(';')
                    try:
                         self.data['type'] = '-'
                         self.data['initialized'] = '-'
                         for item in self.struct_tree:
                             if item.ide == self.data['lexema']:
                                 raise OSError 
                         self.struct_tree.append(DataToken(self.data))
                    except OSError:
                         pass
                    

                    
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
        self.data['initialized'] = '-'
        if self.itr.cur.lexema == 'procedure':
            self.nextToken()
            self.procedureBody()
        elif self.itr.cur.lexema == 'function':
            self.nextToken()
            if self.itr.cur.lexema in self.typeOf:
                self.data['type'] = self.itr.cur.lexema
                self.nextToken()
                self.functionBody()
            else:
                self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid Type"))
        self.data ={"lexema": "-", "type":"-", "initialized":"-", "scope":"-", "params":"-"}

            
    def procedureBody(self) -> None: # Funcionando corretamente
        self.notDeclaration = True
        if self.itr.cur.lexema == "start":
            self.main = True
            self.nextToken()
            if self.nextToken('{'):
                self.scope += 1
                while self.itr.cur.lexema in {'var','const'}:
                    statement = self.global_dict[self.itr.cur.lexema]
                    statement()
                self.statementProduction()
                self.nextToken('}')
                self.notDeclaration = False
        elif self.itr.cur.type == "IDE":
            self.data['lexema'] = self.itr.cur.lexema
            self.nextToken()
            self.paramsProduction()
            try:
                self.data['scope'] = f"local {self.scope + 1}"
                for item in self.procedure_tree:
                    if item.ide == self.data['lexema']:
                        raise OSError 
                self.procedure_tree.append(DataToken(self.data))
            except OSError:
                pass
            if self.nextToken('{'):
                self.scope += 1
                while self.itr.cur.lexema in {'var','const'}:
                    statement = self.global_dict[self.itr.cur.lexema]
                    statement()
                self.statementProduction()
                self.nextToken('}')
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier or start"))
            self.itr.next()
        self.notDeclaration = False
        
    
    def functionBody(self) -> None: # Funcionando corretamente
        self.notDeclaration = True
        if self.itr.cur.type == "IDE":
            self.data['lexema'] = self.itr.cur.lexema
            self.nextToken()
            self.paramsProduction()
            try:
                self.data['scope'] = f"local {self.scope + 1}"
                for item in self.function_tree:
                    if item.ide == self.data['lexema']:
                        raise OSError 
                self.function_tree.append(DataToken(self.data))
            except OSError:
                pass
            if self.nextToken('{'):
                self.scope += 1
                while self.itr.cur.lexema in {'var','const'}:
                    statement = self.global_dict[self.itr.cur.lexema]
                    statement()
                self.statementProduction()
                self.returnProduction()
                self.nextToken('}')
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Identifier"))
            self.itr.next()
        self.notDeclaration = False

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
        elif self.itr.cur.type in {'global','local'}:
            self.nextToken()
            self.nextToken('.')
            if self.itr.cur.type == 'IDE':
                self.nextToken()
                self.expressionProduction()
            
        else:
            self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid expression"))
            self.itr.next()
                   
    def paramsProduction(self) -> None: # Funcionando corretamente
        if self.nextToken('('):
            self.data['params'] = []
            self.params()
            self.nextToken(')')

    def params(self) -> None: # Funcionando corretamente
        if self.itr.cur.lexema in self.typeOf:
            self.data['params'].append(self.itr.cur.lexema)
            self.nextToken()
            if self.itr.cur.type == 'IDE':
                self.nextToken()
                if self.itr.cur.lexema == ',':
                    self.nextToken()
                    self.params()

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
                self.nextToken(';')
            elif self.itr.cur.type == 'IDE':
                if self.itr.nxt.lexema == "(":
                    self.callFunction()
                else:
                    self.expressionProduction()
                self.nextToken(';')
            elif self.itr.cur.lexema == '(':
                self.nextToken()
                self.expressionProduction()
                self.nextToken(')')
                self.nextToken(';')
            elif self.itr.cur.lexema in {'global','local'}:
                self.varScoped()
            else:
                self.sintax_analisys.append(SintaxError(self.itr.cur,"Valid return"))
                self.itr.next()

    
    def varProduction(self) -> None: # Funcionando corretamente
        if self.itr.cur == None:
            return
        elif self.itr.cur.lexema == 'var':
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
            self.data["type"] = self.itr.cur.lexema #pegamos o tipo
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
            self.data["lexema"] = self.itr.cur.lexema #pegamos o token
            self.nextToken()
            if self.itr.cur.lexema == '=':
                self.data["t"] = True
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
                            if self.itr.cur.lexema == '[':
                                self.nextToken()
                                self.arrayUsage()
                            else:
                                self.expressionProduction()  
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
            if self.notDeclaration == False:
                self.data["scope"] = "global"
            else:
                self.data["scope"] = f"local {self.scope}"
            self.data["params"] = '-'
            if self.data['initialized'] == '-':
                self.data['initialized'] = False
            try:
                for item in self.var_tree:
                    if item.scope == self.data['scope'] and item.ide == self.data['lexema']:
                        raise OSError 
                self.var_tree.append(DataToken(self.data))
            except OSError:
                pass
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
                            if self.itr.cur.lexema == '[':
                                self.nextToken()
                                self.arrayUsage()
                            else:
                                self.expressionProduction()  
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
            self.data["type"] = self.itr.cur.lexema #pegamos o tipo
            self.nextToken()
            self.constants()
            self.nextToken(';')
            self.constDeclaration()
    
    def constants(self) -> None: # Funcionando corretamente       
        exp = {'IDE','NRO','CAD','true','false'}
        if self.itr.cur.type == 'IDE':
            self.data["lexema"] = self.itr.cur.lexema #pegamos o token
            self.nextToken()
            if self.nextToken('='):
                self.data["t"] = True
                if self.itr.cur.type in exp or self.itr.cur.lexema in exp:
                    self.nextToken()
            if self.notDeclaration == False:
                self.data["scope"] = "global"
            else:
                self.data["scope"] = f"local {self.scope}"
            self.data["params"] = '-'
            try:
                for item in self.const_tree:
                    if item.scope == self.data['scope'] and item.ide == self.data['lexema']:
                        raise OSError 
                self.const_tree.append(DataToken(self.data))
            except OSError:
                pass
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

    def getVarTree(self) -> list:
        return self.var_tree

    def getConstTree(self) -> list:
        return self.const_tree
        
    def getFunctionTree(self) -> list:
        return self.function_tree
    
    def getProcedureTree(self) -> list:
        return self.procedure_tree

    def getStructTree(self) -> list:
        return self.struct_tree
   

if __name__ == "__main__":
    codigoFonte = '''var{
    int a;
    int b, c;
}

const{
    real PI = 3.14;
}

procedure start{
    var{
        int a;
        int b, c;
        int d = 0, e = 0;
    }

    const{
        boolean isNotTrue = false, isEmpty = false;
    }
    a = b;
    b = c + d;

    
    typedef struct {
        var {int teste;}
    } roberto;
}

function real decrementar (int param1, string param2){
    var { int a;}
    while(a < 5){
        global.a = global.a - 1;
    }
    return global.a;
}

procedure teste (){
    var {int escopo1 = 1;}
}
'''
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    sintaxParser = Parser(tokens)
    result = sintaxParser.sintaxParser()
    # for i in result:
    #     print(i)
    varTree = sintaxParser.getVarTree()
    for i in varTree:
        print(f"{i.ide} | {i.type} | {i.initialized} | {i.scope} | {i.params}")
    print("\n")
    constTree = sintaxParser.getConstTree()
    for i in constTree:
        print(f"{i.ide} | {i.type} | {i.initialized} | {i.scope} | {i.params}")
    print("\n")
    functionTree = sintaxParser.getFunctionTree()
    for i in functionTree:
        print(f"{i.ide} | {i.type} | {i.initialized} | {i.scope} | {i.params}")
    print("\n")
    procedureTree = sintaxParser.getProcedureTree()
    for i in procedureTree:
        print(f"{i.ide} | {i.type} | {i.initialized} | {i.scope} | {i.params}")
    print("\n")
    structTree = sintaxParser.getStructTree()
    for i in structTree:
        print(f"{i.ide} | {i.type} | {i.initialized} | {i.scope} | {i.params}")

