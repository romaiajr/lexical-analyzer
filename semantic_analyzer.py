from os import error
from iterator import MyIterator

#Checklist barema:
#Duplicidade Global OK
#Duplicidade Local OK
#Duplicidade Funções OK
#Identificador não declarado (Verificar se ele foi instanciado)
#Chamada de função e procedures (verificar se existe e tals)
#Atribuições à constantes (Não pode atribuir dps de instanciado)
#Verificação de Tipos (atribuição, comparação, retornos)
#Vetores Matrizes e Structs (deixar struct pra depois) (matriz e vetor é aquela questão onde os indices são inteiros [1] ou [i] onde i é inteiro)


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
        
    def symbolTable(self) -> None:
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
            
        print('VAR TABLE')
        for item in self.var_table:
            print(f"{item.ide} {item.type} {item.scope} {item.initialized}")
        print('\nCONST TABLE')
        for item in self.const_table:
            print(f"{item.ide} {item.type} {item.scope} {item.initialized}")
        print('\nPROCEDURE TABLE')
        for item in self.procedure_table:
            print(f"{item.ide} {item.returnType} {item.scope} {item.params}")
        print('\nFUNCTION TABLE')
        for item in self.function_table:
            print(f"{item.ide} {item.returnType} {item.scope} {item.params}")
        print('\nERROS')
        for item in self.errors:
            print(item)
            
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
                        if item.ide == var_info['ide'] and item.scope == var_info['scope']:
                            raise OSError
                    for item in self.const_table:
                        if item.ide == var_info['ide'] and item.scope == var_info['scope']:
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