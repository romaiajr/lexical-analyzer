class ClassifyLexema():
    reservedWords = ["var", "const", "typedef", "struct", "extends", "procedure",
                     "function", "start", "return", "if", "else", "then", "while", "read", "print", "int",
                     "real", "boolean", "string", "true", "false",
                     "global", "local"]
    delimitadores = [";", ",", "(", ")", "{", "}", "[", "]", "."]
    operadorAritmetico = ["+", "-", "*", "/", "++", "--"]
    operadoresRelacionais = ["==", "!=", ">", ">=", "<", "<=", "="]
    operadorLogico = ["&&", "||", "!"]
    symbolsTable = []

    def getToken(self, lexema):
        tokens = []
        word = ''
        counter = 0
        charList = self.splitWord(lexema)  # Transforma a linha em letras
        length = len(charList)

        while counter < length:
            if charList[counter].isspace():  # Verifica se é um espaço
                counter += 1
            elif charList[counter].isidentifier():  # Verifica se é um caracter
                while charList[counter].isidentifier() or charList[counter].isnumeric():
                    word += charList[counter]
                    counter += 1
                    if counter == length:
                        break
                if not self.symbolsTable.__contains__(word):
                    self.symbolsTable.append(word)
                if self.reservedWords.__contains__(word):
                    tokens.append("<Palavra Reservada, "+word+" >")
                else:
                    # Token ID REVIEW
                    tokens.append(
                        "<ID, "+word+" [" + str(self.symbolsTable.index(word))+"]>")
                word = ''
            elif charList[counter].isnumeric():  # Verifica se é um número
                while charList[counter].isnumeric():  # TODO resolver problema de dígitos
                    word += charList[counter]
                    counter += 1
                    if counter == length:
                        break
                if word.isnumeric():
                    tokens.append("<Numero, "+word+">")
                elif word.isdigit():
                    tokens.append("<Digito, "+word+">")
                word = ''
            else:  # Se não for número, letra ou espaço, será um simbolo
                # String TODO ver caso de string quebrada em linhas #and charList[counter]!="\n"
                if charList[counter] == "\"":
                    word += charList[counter]
                    counter += 1
                    while charList[counter] != "\"":
                        word += charList[counter]
                        counter += 1
                        if counter == length:
                            break
                    word += charList[counter]
                    counter += 1
                    tokens.append("<Cadeia de Caracteres>, "+word+">")
                elif charList[counter] == "/" and charList[counter+1] == "/":  # Comentário em Linha
                    while charList[counter] != "\n":
                        counter += 1
                        if counter == length:
                            break
                # Comentário em Bloco TODO rever pq o */ estava bugando
                elif charList[counter] == "/" and charList[counter+1] == "*":
                    counter += 2
                    while charList[counter] != "*" and charList[counter+1] != "/":
                        counter += 1
                        if counter == length:
                            break
                    counter += 2
                # Delimitadores
                elif self.delimitadores.__contains__(charList[counter]):
                    tokens.append("<Delimitador, "+charList[counter]+">")
                    counter += 1
                elif charList[counter] == "+" or charList[counter] == "-" or charList[counter] == "*" or charList[counter] == "/":  # OP. Aritmético
                    if self.operadorAritmetico.__contains__(charList[counter] + charList[counter+1]):
                        tokens.append(
                            "<Op. Aritmetico, " + charList[counter] + charList[counter+1] + ">")
                        counter += 2
                    else:
                        tokens.append("<Op. Aritmetico, " +
                                      charList[counter] + ">")
                        counter += 1
                elif charList[counter] == "=" or charList[counter] == "!" or charList[counter] == ">" or charList[counter] == "<":  # OP. Relacional
                    if self.operadoresRelacionais.__contains__(charList[counter] + charList[counter+1]):
                        tokens.append(
                            "<Op. Relacional, " + charList[counter] + charList[counter+1] + ">")
                        counter += 2
                    elif self.operadoresRelacionais.__contains__(charList[counter]):
                        tokens.append("<Op. Relacional, " +
                                      charList[counter] + ">")
                        counter += 1
                    else:
                        tokens.append("<Op. Lógico, "+charList[counter]+">")
                        counter += 1
                # OP. Lógico #REVIEW Código mt extenso?
                elif charList[counter] == "&" or charList[counter] == "|":
                    if self.operadorLogico.__contains__(charList[counter] + charList[counter+1]):
                        tokens.append(
                            "<Op. Logico, " + charList[counter] + charList[counter+1] + ">")
                        counter += 2
                    # elif self.operadorLogico.__contains__(charList[counter]): # Equivale ao !, porém já foi chamado em Op. Relacionais
                    #     tokens.append("<Op. Lógico, "+ charList[counter] +">")
                    #     counter += 1
                    else:
                        tokens.append("<Simbolo, "+charList[counter]+">")
                        counter += 1
                else:
                    word += charList[counter]
                    tokens.append("<Simbolo, "+word+">")
                    counter += 1
                word = ''
        # for token in tokens:
        #     print(token)
        # print(self.symbolsTable)
        return tokens

    def getSymbolsTable(self):
        return self.symbolsTable

    def splitWord(self, lexema) -> str:
        return [char for char in lexema]
        # return list(lexema)


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
