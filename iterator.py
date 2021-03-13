class MyIterator():

    def __init__(self, file):
        self.file = file
        self.__iterator = iter(file)
        self.__prv = None
        self.__cur = self.__create_next()
        self.__nxt = self.__create_next()

    @property
    def prv(self):
        return self.__prv

    @property
    def cur(self):
        return self.__cur

    @property
    def nxt(self):
        return self.__nxt

    def next(self):
        self.__prv = self.__cur
        self.__cur = self.__nxt
        try:
            self.__nxt = self.__create_next()
        except StopIteration:
            self.__nxt = None

    def __create_next(self):
        return str(next(self.__iterator))


if __name__ == '__main__':
    myIterator = MyIterator("Samuel")
    print(myIterator.cur)
    print(myIterator.nxt)
    myIterator.next()
    print(myIterator.nxt)
    myIterator.next()
    print(myIterator.nxt)