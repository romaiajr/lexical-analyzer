def lexema_maker(whole_file):
    #Colocar \s em todo espaço que depois dele vem caracter, com exceção de comentarios e strings
    lexemas = []
    foundAspas = False
    for character in whole_file:
        isAspas = character=="\""

        if isAspas and foundAspas:
            foundAspas = False
        elif isAspas and not foundAspas:
            foundAspas = True
def automato_string(lexema):
    tokens = []
    lexema = '''/* 
        teste08 - sem erros
    */
    +9\"HELOU MUNDO\"
    const int MAX = 10, MAX2 = 50;
        
    string Mensagem = \"Hello world\";

    procedure start {  // comeca aqui o programa principal 

        int idade; 
        real salario;
        string nome;

        print(\"Digite o nome\");
        read(nome);
        print(\"Digite a idade\");
        read(idade);
        
        if (idade >= 150) print(\"pode aposentar kkkk\");
        else {
            print(\"vai trabalhar\");
            salario = salario; // hehehe
        }	
    
    } // fim start'''

    openedString = False
    startString,endString = 0,0
    for k in range(len(lexema)):
        porta = lexema[k]
        if lexema[k] == "\"" and not openedString:
            openedString = True
            startString=k   
        elif lexema[k] == "\"" and openedString:
            endString=k+1
            tokens.append("Isso é string"+lexema[startString:endString])
            openedString = False
            #print(lexema[startString:endString])
        #if lexema[k] == " " and k not in range(startString,endString):
            #lexema[k].replace(lexema[k],"\s")
            #s = s[:index] + newstring + s[index + 1:]
            #if character == " " and character+1.isD
    for lexema in tokens:
        print(lexema)
    # // asfasafsfafafas asfa sfasfa afa afasfa
    # /*  asfaf  fasf ass asss*/
    # "oi oi oi oi"
    # /**/