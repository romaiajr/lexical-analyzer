import os
from classify_lexema import ClassifyLexema
files = os.listdir("./input/")
counter = 0
for file in files:
    clex = ClassifyLexema()
    pathName = open(f"./input/{file}", "r")
    codigoFonte = pathName.read()
    print(codigoFonte)
    out = open("./output/"+file.replace("entrada", "saida"), "w")
    #out.write("--------------------------\nTOKENS\n--------------------------\n")
    for token in clex.getToken(codigoFonte):
        out.write(str(token) + "\n")
    #out.write("\n\n")
    out.write("\n")
    for error in clex.getErrorTokens():
        out.write(str(error) + "\n")
    out.write("--------------------------\n\n\n--------------------------\nTABELA DE SIMBOLOS\n--------------------------\n")
    for idx, item in enumerate(clex.getSymbolsTable()):
        out.write("[" + str(idx)+"] " + item + "\n")
    out.write("--------------------------")
    
# Rever todas as condições que envolvem [counter+1] #REVIEW
# Item fora do alfabeto sendo pego na string, como fazer?    #REVIEW   VERIFICAR DENTRO DO WHILE 
# /* quebrado tá pegando da mesma forma quando encontra um /    #REVIEW
#verificar em todos os whiles se o caracter faz parte da tabela ascii #REVIEW isascii não serve já que tem que estar num intervalo
# cadeia de caracteres até achar o " \n, cadeia de caracter só pega a linha #NOTE
# simbolo apenas em cadeia de caracteres #NOTE
# string n pode fechar com \" #REVIEW
# 3.5 while dps do ponto #NOTE
# Token tem que guardar a Linha #NOTE
# Token de ERRO é Possível #NOTE