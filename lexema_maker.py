class LexemaMaker():
   
    def makeLexema(self,code):
        lexemas = []
        for line in code.splitlines(): # Dividir código fonte em linhas
            lexemas+= self.__splitSpaces(line)
        return lexemas
        
    def __splitSpaces(self,line):
        withoutSpaces = line.replace(" ", "\s") # Substituir espaços por \s
        return withoutSpaces.split("\s")# Separar em lexemas de acordo com o \s

if __name__ == "__main__": 
    lex = LexemaMaker()
    print(lex.makeLexema("Para Testar o Objeto"))

# # import re
# # code = re.sub(' +', ' ', code)
# code = "test for    this \"test for    this\""
# print(code)
# def replace_space(text):
#     counter = 0
#     firstSpace = ''
#     openedString = False
#     for i in range(len(code)):
#         character = code[i]
#         isAspas = character == "\""
#         if isAspas:
#             if openedString:
#                 openedString = False
#             openedString = True
#         elif character.isspace():
#             if firstSpace == '':
#                 firstSpace = i
#             elif openedString:
#                 firstSpace = ''
#             else:
#                 newCode = code[:firstSpace] + code[i:]
#                 counter+=1
#                 firstSpace = i-counter
#         elif not character.isspace():
#             # if firstSpace != '':
#             #     if not openedString:
#             #         newCode = code[:firstSpace] +"\s"+ code[i:]
#             firstSpace = ''
#     return newCode

# code = replace_space(code)
# print(code)
#lexemas = []