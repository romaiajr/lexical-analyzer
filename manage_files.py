import os
from lexema_maker import LexemaMaker
from classify_lexema import ClassifyLexema
files = os.listdir("./input/")
lex = LexemaMaker()
clex = ClassifyLexema()
counter = 0
for file in files:
    # lexemas = [] 
    pathName = open(f"./input/{file}", "r")
    codigoFonte = pathName.read()
    out = open("./output/"+file.replace("entrada", "saida"), "w")
    # lexemas = lex.makeLexema(codigoFonte)
    # for lexema in lexemas:
    #     # CHAMADA DO AUTOMATO PRINCIPAL, PASSANDO LEXEMA POR LEXEMA PARA LEITURA POR CARACTER
    #     out.write(lexema.strip() +"\n")#
    out.write("--------------------------\nTOKENS\n--------------------------\n")
    for token in clex.getToken(codigoFonte):
        out.write(str(token) + "\n")
    out.write("--------------------------\n\n\n--------------------------\nTABELA DE SIMBOLOS\n--------------------------\n")
    for idx, item in enumerate(clex.getSymbolsTable()):
        out.write("[" + str(idx)+"] " + item + "\n")
    out.write("--------------------------")