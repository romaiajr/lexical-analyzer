from iterator import MyIterator
class SymbolTable():

    def __init__(self, tokens:list) -> None:
        self.itr = MyIterator(tokens)
        self.id = 0
        self.category = {
            'var': self.variable, 
            'const':self.const, 
            'function': self.function, 
            'procedure': self.procedure, 
            'typedef':self.struct
        }
        

    def populateTable(self) -> None:
        try:
            # self.escopo = Scope(self.id) #repensar onde instanciar esse escopo
            if self.itr.cur.lexema in self.category:
                category = self.category[self.itr.cur.lexema]
                category()
            elif self.itr.cur.type == 'IDE':
                pass
            elif self.itr.cur.lexema == '{':
                self.escopo += 1
            else:
                self.itr.next()
            self.populateTable()
        except StopIteration:
            pass


class Scope():

    def __init__(self, id:int)-> None:
        self.id = id
        self.childs = []

    def insert(self, item) -> None:
        self.childs.append(item)


class DataToken():
    pass
        

   procedure start(){
       while(a = b){
           a++
       }
       if(a < b){
           var{a = 0}
       }
       else{

       }
   }