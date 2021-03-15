import os
import sys
sys.setrecursionlimit(20000)
from generate_tokens import GenerateTokens
files = os.listdir("./input/")
for file in files:
    # Seleciona todos os arquivos de entrada e, para cada um deles, gera um arquivo de saída
    pathName = open(f"./input/{file}", "r")
    codigoFonte = pathName.read()
    out = open("./output/"+file.replace("entrada", "saida"), "w")

    # Gerando e armazenando tokens e erros
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    errors = gtokens.getErrorTokens()

    # Escrevendo no arquivo de saída
    for token in gtokens.initialState():
        out.write(str(token) + "\n")
    out.write("\n")
    for error in errors:
        out.write(str(error) + "\n")

# Item fora do alfabeto sendo pego na string, como fazer? #REVIEW   VERIFICAR DENTRO DO WHILE
# string n pode fechar com \" #REVIEW