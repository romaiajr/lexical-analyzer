# import re
# code = re.sub(' +', ' ', code)
code = "test for    this \"test for    this\""
print(code)
def replace_space(text):
    counter = 0
    firstSpace = ''
    openedString = False
    for i in range(len(code)):
        character = code[i]
        isAspas = character == "\""
        if isAspas:
            if openedString:
                openedString = False
            openedString = True
        elif character.isspace():
            if firstSpace == '':
                firstSpace = i
            elif openedString:
                firstSpace = ''
            else:
                newCode = code[:firstSpace] + code[i:]
                counter+=1
                firstSpace = i-counter
        elif not character.isspace():
            # if firstSpace != '':
            #     if not openedString:
            #         newCode = code[:firstSpace] +"\s"+ code[i:]
            firstSpace = ''
    return newCode

code = replace_space(code)
print(code)
    