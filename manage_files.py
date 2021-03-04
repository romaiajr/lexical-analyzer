import os
from lexema_maker import LexemaMaker
files = os.listdir("./input/")
lex = LexemaMaker()
for file in files:
    lexemas = [] 
    pathName = open(f"./input/{file}", "r")
    codigoFonte = pathName.read()
    out = open("./output/"+file.replace("entrada", "saida"), "w")
    lexemas = lex.makeLexema(codigoFonte)
    for lexema in lexemas:#
        # CHAMADA DO AUTOMATO PRINCIPAL, PASSANDO LEXEMA POR LEXEMA PARA LEITURA POR CARACTER
        out.write(lexema.strip() +"\n")#