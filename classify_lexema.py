class ClassifyLexema():
    reservedWords = ["var", "const", "typedef", "struct", "extends", "procedure",
    "function", "start", "return", "if", "else", "then", "while", "read","print", "int",
    "real", "boolean", "string", "true", "false",
    "global", "local"]
    delimitadores = [";",",","(",")","{","}","[","]","."]
    operadoresAritmeticos = ["+","-","*","/","++","--"]
    operadoresRelacionais = ["==","!=",">",">=","<","<=","="]
    operadoresLogicos = ["&&","||","!"]
    symbolsTable = []
    
    def getToken(self,whole_file) -> list: 
        tokens = []
        word = ''
        counter = 0
        charList = self.splitWord(whole_file)#Transforma a linha em letras
        length = len(charList)
        
        while counter < length:
            if charList[counter].isspace(): # Verifica se o caracter é um espaço
                counter += 1
            elif charList[counter].isidentifier(): # Verifica se o caracter é um caracter
                while charList[counter].isidentifier() or charList[counter].isnumeric():
                    word += charList[counter]
                    counter += 1
                    if counter==length:
                        break    
                if not self.symbolsTable.__contains__(word): # Insere o lexema na tabela de simbolos
                    self.symbolsTable.append(word)
                if self.reservedWords.__contains__(word): # Caso seja uma palavra reservada
                    tokens.append("<Palavra Reservada, "+word+" >")
                else: # Se não for uma palavra reservada, será um identificador
                    tokens.append("<ID, "+word+" [" + str(self.symbolsTable.index(word))+"]>") # REVIEW estrutura do token
                word = ''                                                                      
            elif charList[counter].isnumeric(): # Verifica se o caracter é um número
                while charList[counter].isnumeric(): #TODO resolver problema de dígitos (ponto flutuante)
                    word += charList[counter]
                    counter += 1
                    if counter==length:
                        break
                if word.isnumeric():
                    tokens.append("<Numero, "+word+">")
                elif word.isdigit(): #REVIEW classificar como dígito (ponto flutuante)
                    tokens.append("<Digito, "+word+">")
                word = '' 
            else: # Se não for número, letra ou espaço, será um simbolo
                if charList[counter]=="\"":# String TODO ver caso de string quebrada em linhas #and charList[counter]!="\n"
                    word+=charList[counter]
                    counter+=1
                    while charList[counter]!="\"":
                        word += charList[counter]
                        counter += 1
                        if counter==length:
                            break
                    word+=charList[counter]
                    counter+=1
                    tokens.append("<Cadeia de Caracteres>, "+word+">")
                elif charList[counter]=="/" and charList[counter+1]=="/": # Comentário em Linha
                    while charList[counter]!="\n":
                        counter+=1
                        if counter==length:
                            break
                elif charList[counter]=="/" and charList[counter+1]=="*": # Comentário em Bloco TODO rever pq o */ estava bugando
                    counter+=2
                    while charList[counter]!="*" and charList[counter+1]!="/":
                        counter+=1
                        if counter==length:
                            break
                    counter+=2
                elif self.delimitadores.__contains__(charList[counter]): # Delimitadores
                    tokens.append("<Delimitador, "+charList[counter]+">")
                    counter += 1
                elif charList[counter] in {"+","-","*","/"}:  # OP. Aritmético
                    if self.operadoresAritmeticos.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [++,--]
                        tokens.append("<Op. Aritmetico, "+ charList[counter] + charList[counter+1] + ">")
                        counter += 2
                    else: # Contém os casos: [+, -, *, /]
                        tokens.append("<Op. Aritmetico, "+ charList[counter] +">")
                        counter += 1
                elif charList[counter] in {"=","!",">","<"}: #OP. Relacional
                    if self.operadoresRelacionais.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [==, !=, >=, <=]
                        tokens.append("<Op. Relacional, "+ charList[counter] + charList[counter+1] + ">")
                        counter += 2
                    elif self.operadoresRelacionais.__contains__(charList[counter]): # Contém os casos: [=, >, <]
                        tokens.append("<Op. Relacional, "+ charList[counter] +">")
                        counter += 1
                    else: # Contém o caso: [!], esse caso é classificado como OP. Lógico
                        tokens.append("<Op. Lógico, "+charList[counter]+">")
                        counter += 1                  
                elif charList[counter] in {"&","|"}: # OP. Lógico
                    if self.operadoresLogicos.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [&&, ||]
                        tokens.append("<Op. Logico, "+ charList[counter] + charList[counter+1] + ">")
                        counter += 2
                    else:
                        tokens.append("<Simbolo, "+charList[counter]+">")
                        counter += 1
                else: #Caso não se encaixe em nenhum dos padrões acima, é classificado como simbolo
                    word+=charList[counter]
                    tokens.append("<Simbolo, "+word+">")
                    counter += 1
                word = ''
        return tokens
    
    def getSymbolsTable(self) -> list:
        return self.symbolsTable
    
    def splitWord(self,whole_file)  -> list:
        return list(whole_file)

if __name__ == "__main__": 
    cl = ClassifyLexema()
    arquivo = '''/* 
	teste08 - sem erros
*/
+9"HELOU MUNDO"
const int MAX = 10, MAX2 = 50;
	
string Mensagem = "Hello world";

procedure start {  // comeca aqui o programa principal 

	int idade; 
	real salario;
	string nome;

	print("Digite o nome");
	read(nome);
	print("Digite a idade");
	read(idade);
	
	if (idade >= 150) print("pode aposentar kkkk");
	else {
		print("vai trabalhar");
		salario = salario; // hehehe
	}	
 
} // fim start
	'''
    cl.getToken(arquivo)
    # for linha in arquivo.splitlines():
    #     cl.getToken(linha)
    