codigoFonte = "\"codigo fonte teste\"b    #$89893128+=-'  fonte  '  '  \"roberto\""
lexema = ""
tokens = []
foundAspas = False
notString = []
for caractere in codigoFonte: #Leitura Caractere por Caractere no código fonte
    if caractere!=" ":# Caso o caractere não seja um espaço em branco, avançamos
        isAspas = caractere == "\"" #Verifica se o caractere é aspas
        if foundAspas==False: #Buscando início da String com "
            if not isAspas:
                lexema+=caractere
            else: #Encontrou o início Início da String
                foundAspas = True
                if lexema != "":
                    notString.append(lexema) #Salva tudo aquilo que não era uma string
                lexema = ''
                lexema+=caractere
        else: #Já encontrou o início da String, agora vai procurar o corpo
            lexema+=caractere  
            if isAspas: #Caso seja aspas, finaliza a string "..."
                tokens.append(lexema)
                # print(lexema+" é uma String")
                lexema=""
                foundAspas = False
    elif caractere == " " and foundAspas: #Caso o caractere seja um espaço em branco e a string já tenha começado
        lexema+=caractere
for token in tokens:
    print("<String,"+token+">", "Lexema: " + token);
for i in notString:
    print(i +" Não é classificado como String")
    
        
    
