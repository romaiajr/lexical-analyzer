import os
from generate_tokens import GenerateTokens
files = os.listdir("./input/")
for file in files:
    # Abrindo arquivo de entrada e criando arquivo de saída
    pathName = open(f"./input/{file}", "r")
    codigoFonte = pathName.read()
    out = open("./output/"+file.replace("entrada", "saida"), "w")

    # Gerando e armazenando tokens e erros
    gtokens = GenerateTokens(codigoFonte)
    tokens = gtokens.initialState()
    errors = gtokens.getErrorTokens()

    # Escrevendo no arquivo
    for token in tokens:
        out.write(str(token) + "\n")
    out.write("\n")
    for error in errors:
        out.write(str(error) + "\n")

# Item fora do alfabeto sendo pego na string, como fazer? #REVIEW   VERIFICAR DENTRO DO WHILE
# string n pode fechar com \" #REVIEW