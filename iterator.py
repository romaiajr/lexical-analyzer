class MyIterator():
    '''
    Classe responsável por iterar o conteúdo do arquivo
    '''
    def __init__(self, file:str):
        '''
        Params:
        file: Contéudo do arquivo lido
        '''
        self.file = file
        self.__iterator = iter(file)
        self.__prv = None
        self.__cur = self.__create_next()
        self.__nxt = self.__create_next()

    @property
    def prv(self):
        '''
        Método para retornar o item anterior do iterador
        
        Returns:
        self.__prv: Item anterior do iterador
        '''
        return self.__prv

    @property
    def cur(self):
        '''
        Método para retornar o item atual do iterador
        
        Returns:
        self.__cur: Item atual do iterador
        '''
        return self.__cur

    @property
    def nxt(self):
        '''
        Método para retornar o próximo item do iterador
        
        Returns:
        self.__prv: Próximo item do iterador
        '''
        return self.__nxt

    def next(self):
        '''
        Método para mover o iterador para o próximo item e atribuir novos valores
        às variáveis __prv, __cur, __nxt
        '''
        self.__prv = self.__cur
        self.__cur = self.__nxt
        try:
            self.__nxt = self.__create_next()
        except StopIteration:
            self.__nxt = None

    def __create_next(self):
        '''
        Método para mover o iterador para o próximo item
        '''
        try:
            return (next(self.__iterator))
        except StopIteration:
            return None

if __name__ == '__main__':
    myIterator = MyIterator("Works")
    print(myIterator.cur)
    print(myIterator.nxt)
    myIterator.next()
    print(myIterator.nxt)
    myIterator.next()
    print(myIterator.nxt)