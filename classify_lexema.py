from token import *

class ClassifyLexema():
    
    reservedWords = ["var", "const", "typedef", "struct", "extends", "procedure",
    "function", "start", "return", "if", "else", "then", "while", "read","print", "int",
    "real", "boolean", "string", "true", "false",
    "global", "local"]
    delimitadores = [";",",","(",")","{","}","[","]","."]
    operadoresAritmeticos = ["+","-","*","/","++","--"]
    operadoresRelacionais = ["==","!=",">",">=","<","<=","="]
    operadoresLogicos = ["&&","||","!"]
    symbols_table = []
    
    def getToken(self,whole_file) -> list: 
        tokens = []
        lexema = ''
        counter = 0
        charList = self.splitWord(whole_file) # Transforma a linha em letras
        length = len(charList)
        
        while counter < length:
            if charList[counter].isascii():
                if charList[counter].isspace(): # Verifica se o caracter é um espaço
                    counter += 1
                elif charList[counter].isidentifier(): # Verifica se o caracter é um caracter
                    while charList[counter].isidentifier() or charList[counter].isnumeric():
                        lexema += charList[counter]
                        counter += 1
                        if counter==length:
                            break    
                    if not self.symbols_table.__contains__(lexema): # Insere o lexema na tabela de simbolos
                        self.symbols_table.append(lexema)
                    if self.reservedWords.__contains__(lexema): # Caso seja uma palavra reservada
                        tokens.append(Token(RW_TOKEN, lexema))
                    else: # Se não for uma palavra reservada, será um identificador
                        tokens.append(Token(ID_TOKEN, str(self.symbols_table.index(lexema))))
                    lexema = ''                                                                      
                elif charList[counter].isnumeric(): # Verifica se o caracter é um número
                    while charList[counter].isnumeric(): #TODO resolver problema de dígitos (ponto flutuante)
                        lexema += charList[counter]
                        counter += 1
                        if counter==length:
                            break
                    if lexema.isnumeric():
                        tokens.append(Token(NUMBER_TOKEN, lexema))
                    elif lexema.isdigit(): #REVIEW classificar como dígito (ponto flutuante)
                        tokens.append(Token(DIGIT_TOKEN), lexema)
                    lexema = '' 
                else: # Se não for número, letra ou espaço, será um simbolo
                    if charList[counter]=="\"":# String TODO ver caso de string quebrada em linhas #and charList[counter]!="\n"
                        lexema+=charList[counter]
                        counter+=1
                        while charList[counter]!="\"":
                            lexema += charList[counter]
                            counter += 1
                            if counter==length:
                                break
                        lexema+=charList[counter]
                        counter+=1
                        tokens.append(Token(STRING_TOKEN, lexema))
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
                        tokens.append(Token(DELIMITER_TOKEN, lexema))
                        counter += 1
                    elif charList[counter] in {"+","-","*","/"}:  # OP. Aritmético
                        if self.operadoresAritmeticos.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [++,--]
                            tokens.append(Token(OP_A_TOKEN, charList[counter] + charList[counter+1]))
                            counter += 2
                        else: # Contém os casos: [+, -, *, /]
                            tokens.append(Token(OP_A_TOKEN, charList[counter]))
                            counter += 1
                    elif charList[counter] in {"=","!",">","<"}: #OP. Relacional
                        if self.operadoresRelacionais.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [==, !=, >=, <=]
                            tokens.append(Token(OP_R_TOKEN, charList[counter] + charList[counter+1]))
                            counter += 2
                        elif self.operadoresRelacionais.__contains__(charList[counter]): # Contém os casos: [=, >, <]
                            tokens.append(Token(OP_R_TOKEN, charList[counter]))
                            counter += 1
                        else: # Contém o caso: [!], esse caso é classificado como OP. Lógico
                            tokens.append(Token(OP_L_TOKEN, charList[counter]))
                            counter += 1                  
                    elif charList[counter] in {"&","|"}: # OP. Lógico
                        if self.operadoresLogicos.__contains__(charList[counter] + charList[counter+1]): # Contém os casos: [&&, ||]
                            tokens.append("<Op. Logico, "+ charList[counter] + charList[counter+1] + ">")
                            counter += 2
                        else:
                            tokens.append("<Simbolo, "+charList[counter]+">")
                            counter += 1
                    else: #Caso não se encaixe em nenhum dos padrões acima, é classificado como simbolo
                        tokens.append(Token(SYMBOL_TOKEN, charList[counter]))
                        counter += 1
                    lexema = ''
            else:
                print("Erro no caracter [" + charList[counter] + "] - Caracter não pertence ao alfabeto")
                counter += 1
        return tokens
    
    def getSymbolsTable(self) -> list:
        return self.symbols_table
    
    def splitWord(self,whole_file)  -> list:
        return list(whole_file)

if __name__ == "__main__": 
    cl = ClassifyLexema()
    arquivo = '''/* 
	teste08 - sem erros
*/
+9"HELOU MUNDO"ü
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
    