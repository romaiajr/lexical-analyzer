import os
files = os.listdir("./input/")
for file in files:
    pathName = open("./input/"+file, "r")
    out = open("./output/"+file.replace("entrada", "saida"), "w")
    codigoFonte = pathName.read()
    lexemas = codigoFonte.split(" ")
    lexema = ""
    tokens = []
    foundAspas = False
    notString = []
    for caractere in codigoFonte:  # Leitura Caractere por Caractere no código fonte
        isSpace = caractere == " "
        if not isSpace:  # Caso o caractere não seja um espaço em branco, avançamos
            isAspas = caractere == "\""  # Verifica se o caractere é aspas
            if not foundAspas:  # Buscando início da String com "
                if not isAspas:
                    lexema += caractere
                else:  # Encontrou o início Início da String
                    foundAspas = True
                    if lexema != "":
                        # Salva tudo aquilo que não era uma string
                        notString.append(lexema)
                    lexema = ''
                    lexema += caractere
            else:  # Já encontrou o início da String, agora vai procurar o corpo
                lexema += caractere
                if isAspas:  # Caso seja aspas, finaliza a string "..."
                    tokens.append(lexema)
                    # print(lexema+" é uma String")
                    lexema = ""
                    foundAspas = False
        elif isSpace and foundAspas:  # Caso o caractere seja um espaço em branco e a string já tenha começado
            lexema += caractere
    for token in tokens:
        out.write(token+"\n")
    # for i in notString:
    #     print(i + " Não é classificado como String")
