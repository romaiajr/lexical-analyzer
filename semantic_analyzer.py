from os import error
import os
from iterator import MyIterator

class SemanticAnalyzer():
    typeOf = {"int", "real", "string", "boolean"}
    def __init__(self, tokens: list):
        self.tokens=tokens
        self.itr = MyIterator(tokens)
        self.var_table=[]
        self.const_table=[]
        self.function_table=[]
        self.procedure_table=[]
        self.struct_table=[]
        self.errors=[]
        self.notGlobal = False
        self.scope = 0
        
    def symbolTable(self) -> list:
        variables = {'var','const'}
        methods = {'function','procedure'}
        indice = 0
        while indice < len(self.tokens):
            if self.tokens[indice].getLexema() in variables:
                indice = self.varTable(indice)
            elif self.tokens[indice].getLexema() in methods:
                indice = self.methodsTable(indice)
            else:
                indice += 1
        self.lookForErrors()
        return self.errors

    def lookForErrors(self):
        indice=0
        escopo=0
        while indice < len(self.tokens):
            if self.tokens[indice].getType() == 'IDE':
                if self.tokens[indice+1].getLexema()=="(":
                    try:
                        if not self.findMethod(indice):
                            raise OSError
                        #Função(chamada)
                    except OSError:
                        self.errors.append(f"Método [{self.tokens[indice].getLexema()}] presente na linha {self.tokens[indice].line} não foi declarado")
                else:#Se for variável ou constante
                    try:
                        if not self.findVariable(indice,escopo):
                            raise OSError
                        else:
                            if self.tokens[indice + 1].getLexema() == '[':
                                indice += 2
                                try:
                                    if self.tokens[indice].getType() == 'IDE':
                                        if self.lookType(indice, escopo) != 'int':
                                            raise OSError  
                                    elif self.tokens[indice].getType() == 'NRO':
                                        if str(self.tokens[indice].getLexema()).__contains__('.'):
                                            raise OSError  
                                    indice+=2
                                    if self.tokens[indice].getLexema() == '[':
                                        indice += 1
                                        try:
                                            if self.tokens[indice].getType() == 'IDE':
                                                if self.lookType(indice, escopo) != 'int':
                                                    raise OSError  
                                            elif self.tokens[indice].getType() == 'NRO':
                                                if str(self.tokens[indice].getLexema()).__contains__('.'):
                                                    raise OSError  
                                        except OSError:
                                            self.errors.append(f"Indice [{self.tokens[indice].getLexema()}] inválido na linha {self.tokens[indice].getLine()}! O indice deve ser um número inteiro.")     
                                except OSError:
                                    self.errors.append(f"Indice [{self.tokens[indice].getLexema()}] inválido na linha {self.tokens[indice].getLine()}! O indice deve ser um número inteiro.")                       
                    except OSError:
                        self.errors.append(f"Variavel [{self.tokens[indice].getLexema()}] presente na linha {self.tokens[indice].line} não foi declarado")
            elif self.tokens[indice].getLexema() in {"function","procedure"}:
                escopo+=1
                while self.tokens[indice].getLexema() != "{":
                    indice+=1
            elif self.tokens[indice].getLexema() in {'var','const'}:
                while self.tokens[indice].getLexema() != '}':
                    indice +=1
            indice+=1
    
    def findMethod(self,indice):
        existe=False
        for item in self.function_table:
            if item.ide==self.tokens[indice].getLexema():
                existe=True
            if existe == True:
                break
        for item in self.procedure_table:
            if item.ide==self.tokens[indice].getLexema():
                existe=True
            if existe == True:
                break
        return existe

    def findVariable(self,indice,escopo):
        existe=False
        for item in self.var_table:
            if item.ide==self.tokens[indice].getLexema() and item.scope==escopo:
                existe=True
            elif item.ide==self.tokens[indice].getLexema() and item.scope=="global":
                existe=True
            if existe == True:
                break
        for item in self.const_table:
            if item.ide==self.tokens[indice].getLexema() and item.scope==escopo:
                existe=True
            elif item.ide==self.tokens[indice].getLexema() and item.scope=="global":
                existe=True
            if existe == True:
                token = self.tokens[indice]
                while self.tokens[indice].getLexema() != ';':
                    if self.tokens[indice].getLexema() == '=' and self.tokens[indice + 1].getLexema() not in {'>','<','='}:
                        self.errors.append(f"Não é possível atribuir um valor à constante [{token.lexema}] na linha {token.line}")
                    indice += 1
                break
        return existe

    def lookType(self,indice,escopo):
        for item in self.var_table:
            if item.ide==self.tokens[indice].getLexema() and item.scope==escopo:
                return item.type
            elif item.ide==self.tokens[indice].getLexema() and item.scope=="global":
                return item.type
        for item in self.const_table:
            if item.ide==self.tokens[indice].getLexema() and item.scope==escopo:
                return item.type
            elif item.ide==self.tokens[indice].getLexema() and item.scope=="global":
                return item.type

    def varTable(self, indice) -> None:
        var_info = {'type': None, 'ide': None, 'initialized':False, 'scope': None}
        var_or_const = self.tokens[indice].getLexema()     
        while self.tokens[indice].getLexema() != '}':
            if self.tokens[indice].getLexema() in self.typeOf:
                var_info['type'] = self.tokens[indice].getLexema()
            elif self.tokens[indice].getType() == 'IDE':
                var_info['ide'] = self.tokens[indice].getLexema()
                while self.tokens[indice].getLexema() not in {',', ';'}:
                    if self.tokens[indice].getLexema() == '=':
                        var_info['initialized'] = True
                    indice += 1
                try:
                    if self.notGlobal == False:
                        var_info['scope'] = 'global'
                    else:
                        var_info['scope'] = self.scope
                    for item in self.var_table:
                        if item.ide == var_info['ide'] and item.scope == var_info['scope']:#Verifica se já está na tabela
                            raise OSError
                    for item in self.const_table:
                        if item.ide == var_info['ide'] and item.scope == var_info['scope']:#Verifica se já está na tabela
                            raise OSError  
                    if var_or_const == 'var':
                        self.var_table.append(VarToken(var_info))
                    else:
                        self.const_table.append(VarToken(var_info))
                except OSError:
                    self.errors.append(f"Identificador [{var_info['ide']}] duplicado na linha {self.tokens[indice].line}")     
            indice+=1
        return indice

    def methodsTable(self, indice) -> None:
        method_info = {'scope': None, 'ide': None, 'returnType':None, 'params': []}
        procedure_or_function = self.tokens[indice].getLexema()
        self.scope += 1
        self.notGlobal = True
        indice += 1
        brackets = 0
        method_info['scope'] = self.scope
        if procedure_or_function == 'procedure':
            method_info['returnType'] = None
            if self.tokens[indice].getType() == 'IDE':
                method_info['ide'] = self.tokens[indice].getLexema()
                indice += 1
                while self.tokens[indice].getLexema() != ')':
                    if self.tokens[indice].getLexema() in self.typeOf:
                        method_info['params'].append(self.tokens[indice].getLexema())
                    indice += 1
                while self.tokens[indice].getLexema() not in {'const','var'}:
                    if self.tokens[indice].getLexema() == '{':
                        brackets += 1
                    elif self.tokens[indice].getLexema() == '}':
                        brackets -= 1
                        if brackets == 0:
                            break
                    indice += 1
                     
        elif procedure_or_function == 'function':
              if self.tokens[indice].getLexema() in self.typeOf:
                method_info['returnType'] = self.tokens[indice].getLexema()
                indice += 1
                if self.tokens[indice].getType() == 'IDE':
                    method_info['ide'] = self.tokens[indice].getLexema()
                    indice += 1
                    while self.tokens[indice].getLexema() != ')':
                        if self.tokens[indice].getLexema() in self.typeOf:
                            method_info['params'].append(self.tokens[indice].getLexema())
                        indice += 1
                    while self.tokens[indice].getLexema() not in {'const','var'}:
                        if self.tokens[indice].getLexema() == '{':
                            brackets += 1
                        elif self.tokens[indice].getLexema() == '}':
                            brackets -= 1
                            if brackets == 0:
                                break
                        indice += 1
        
        if self.tokens[indice].getLexema() in { 'const', 'var'}:
            indice = self.varTable(indice)
        try:
            for item in self.function_table:
                if item.ide == method_info['ide'] and item.params == method_info['params']:
                    raise OSError
            for item in self.procedure_table:
                if item.ide == method_info['ide'] and item.params == method_info['params']:
                    raise OSError  
            if procedure_or_function == 'procedure':
                self.procedure_table.append(MethodToken(method_info))
            else:
                self.function_table.append(MethodToken(method_info))
        except OSError:
            self.errors.append(f"Metodo [{method_info['ide']}] duplicado com parâmetros iguais {method_info['params']} na linha {self.tokens[indice].line}")
        return indice
                
class VarToken ():

    def __init__(self, obj):
        self.ide = obj['ide']
        self.type = obj['type']
        self.initialized = obj["initialized"]
        self.scope = obj["scope"]

class MethodToken ():

    def __init__(self, obj):
        self.scope = obj['scope']
        self.ide = obj['ide']
        self.returnType = obj['returnType']
        self.params = obj['params']