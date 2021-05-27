from iterator import MyIterator
class SymbolTable():

    def __init__(self, tokens:list) -> None:
        self.itr = MyIterator(tokens)
        self.escopo = 0
        self.table = []
        self.scopeTree = []

    def constructTable(self):
        categories = {
        'var':self.variable, 
        'const':self.constant,
        'function':self.function, 
        'procedure':self.procedure}
        try:
            if self.itr.cur.lexema in categories:
                statement = self.statement_dict[self.itr.cur.lexema]
                statement()
            elif self.itr.cur.lexema in {'{','}'}:
                self.bracketsCounter()
            self.itr.next()
            self.constructTable()
        except StopIteration:
            pass

    def bracketsCounter(self):
        if self.itr.cur.lexema == '{':
            self.escopo += 1
            self.scopeTree.append(Node(self.escopo, self.escopo-1))
        
        else:
            self.escopo -= 1

    def variable(self):
        pass
    
    def constant(self):
        pass

    def function(self):
        pass

    def procedure(self):
        pass

class Node():
    def __init__(self,escopo,escopoPai) -> None:
        self.escopo = escopo
        self.pai = escopoPai
        