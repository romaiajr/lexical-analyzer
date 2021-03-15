from lexical_token import *
from iterator import MyIterator

class GenerateTokens():
    '''
    Classe responsável por criar os tokens
    '''
    reservedWords = {"var", "const", "typedef", "struct", "extends", "procedure",
    "function", "start", "return", "if", "else", "then", "while", "read","print", "int",
    "real", "boolean", "string", "true", "false",
    "global", "local"}
    delimitadores = {";",",","(",")","{","}","[","]","."}
    operadoresAritmeticos = {"+","-","*","/","++","--"}
    operadoresRelacionais = {"==","!=",">",">=","<","<=","="}
    operadoresLogicos = {"&&","||","!"}
    
    def __init__(self, whole_file:str):
        '''
        Construtor da classe GenerateTokens 
        whole_file: String contendo todo o conteúdo do arquivo de entrada
        '''
        self.tokens, self.error_tokens, self.symbols_table = [],[],[]
        self.line = 1
        self.lexema = ''
        self.itr = MyIterator(whole_file)
            
    def initialState(self) -> list:
        '''
        Estado inicial do autômato.
        Analisa o tipo do caractere atual e transiciona para o próximo estado equivalente.
        '''
        self.lexema = ''
        if self.itr.cur == None:
            return self.getTokens()
        elif self.itr.cur.isspace():
            if self.itr.cur == "\n":
                self.line+=1
            self.itr.next()
            self.initialState() 
        elif self.isAscii(self.itr.cur):
            if self.itr.cur.isidentifier():
                self.ideState()
            elif self.itr.cur.isnumeric():
                self.numberState()
            else:
                self.symbolState()
        else:
            self.error_tokens.append(Error_Token(OUT_ASCII_ERROR, self.itr.cur, self.line))
            self.itr.next()
            self.initialState()
            
    def ideState(self):
        '''
        Estado de Identificadores, responsável por criar 
        tokens de identificadores e palavras reservadas, transicionando para o estado
        inicial, pós-identificação de token


        Returns: 
        initialState(): Estado Inicial
        '''
        while (self.itr.cur.isidentifier() or self.itr.cur.isnumeric() or self.itr.cur == "_") and self.isAscii(self.itr.cur):
            self.lexema+=self.itr.cur
            self.itr.next()
            if self.itr.cur == None:
                break
        if not self.symbols_table.__contains__(self.lexema): # Insere o na tabela de simbolos
            self.symbols_table.append(self.lexema)
        if self.reservedWords.__contains__(self.lexema): # Caso seja uma palavra reservada
            self.tokens.append(Token(RW_TOKEN, self.lexema, self.line))
        else: # Se não for uma palavra reservada, será um identificador
            self.tokens.append(Token(ID_TOKEN, self.lexema, self.line))
        self.initialState()                                         

    def numberState(self):
        '''
        Estado inteiro dos Números, responsável por criar 
        tokens de números inteiros. Caso um "." seja encontrado
        ocorrerá uma transição para o estado B, se não, retornará o estado inicial
        pós-identificação de token


        Returns: 
        floatState(): Estado B de Números
        initialState(): Estado Inicial
        '''
        while self.itr.cur.isnumeric():
            self.lexema+=self.itr.cur
            self.itr.next()
            if self.itr.cur == None:
                break
        if self.itr.cur == ".":
            self.lexema+=self.itr.cur
            return self.floatState()
        else:
            self.tokens.append(Token(NUMBER_TOKEN, self.lexema, self.line))
        self.initialState()

    def floatState(self):
        '''
        Estado Decimal dos Números, responsável por criar tokens de números,
        retornando para o estado inicial pós-identificação de token.


        Returns: 
        initialState(): Estado Inicial
        '''
        self.itr.next()
        if self.itr.cur.isnumeric():
            while self.itr.cur.isnumeric():
                self.lexema+=self.itr.cur
                self.itr.next()
                if self.itr.cur == None:
                    break
            self.tokens.append(Token(NUMBER_TOKEN, self.lexema, self.line))
        else:
            self.error_tokens.append(Error_Token(NUMBER_ERROR, self.lexema, self.line))
        self.initialState()

    def symbolState(self):
        '''
        Estado de Símbolos, responsável por criar transições para
        os estados equivalentes a cada símbolo. Retornará ao estado inicial Caso
        o símbolo não corresponda a nenhum dos estados

        Returns:
        stringState(): Estado de Strings
        commentState(): Estado de Comentários
        delimiterState(): Estado de Delimitadores
        opaState(): Estado de Operadores Aritméticos
        oprState(): Estado de Operadores Relacionais
        oplState(): Estado de Operadores Lógicos
        initialState(): Estado Inicial
        '''
        if self.itr.cur == "\"":
            self.lexema += self.itr.cur
            return self.stringState()  
        elif self.itr.cur == "/":
            return self.commentState()
        elif self.delimitadores.__contains__(self.itr.cur):
            return self.delimiterState()
        elif self.operadoresAritmeticos.__contains__(self.itr.cur):
            return self.opaState()
        elif self.itr.cur in {"=", "!", ">", "<"}:
            return self.oprState()
        elif self.itr.cur in {"&","|"}: # OP.
            return self.oplState()
        else:
            self.error_tokens.append(Error_Token(SYMBOL_ERROR, self.itr.cur, self.line))
            self.itr.next()
        self.initialState()

    def stringState(self):
        """
        Estado de Strings, criando tokens de Cadeia de Caracteres,
        retornando para o estado inicial pós-identificação de token.

        Returns:
        initialState(): Estado Inicial
        """
        contain_no_ascii = False
        self.itr.next()
        while self.itr.cur not in {'"',"\n",None}:
            self.lexema+=self.itr.cur
            self.itr.next()
            if self.itr.cur == None:
                break
            elif not self.isAscii(self.itr.cur):
                contain_no_ascii = True
            elif self.itr.cur == "\\" and self.itr.nxt == '"':
                self.lexema+=self.itr.cur + self.itr.nxt
                self.itr.next()
                self.itr.next()

        if self.itr.cur == "\"":
            self.lexema+=self.itr.cur
            if contain_no_ascii:
                self.error_tokens.append(Error_Token(STRING_NO_ASCII, self.lexema, self.line))
            else:
                self.tokens.append(Token(STRING_TOKEN, self.lexema, self.line))
            self.itr.next()
        else:
            self.error_tokens.append(Error_Token(STRING_ERROR, self.lexema, self.line))
            self.line+=1
            self.itr.next()
        self.initialState()
    
    def commentState(self):
        """
        Estado de Comentários, criando tokens de comentários,
        retornando para o estado inicial pós-identificação de token.

        Returns:
        initialState(): Estado Inicial
        """
        self.itr.next()
        if self.itr.cur == "/":
            while self.itr.cur != "\n":
                self.itr.next()
                if self.itr.cur == None:
                    break
            if self.itr.cur == "\n":
                self.line+=1
                self.itr.next()
        elif self.itr.cur == "*":
            skipped_lines = 0
            self.lexema += self.itr.prv + self.itr.cur
            self.itr.next()
            while self.itr.cur != "*" and self.itr.nxt != "/":
                if self.itr.cur == "\n":
                    skipped_lines+=1
                else:
                    self.lexema += self.itr.cur
                self.itr.next()
                if self.itr.cur == None:
                    break
            if self.itr.nxt == None:
                self.error_tokens.append(Error_Token(COMMENT_ERROR, self.lexema, self.line))
            self.itr.next() # Para pular o */ final
            self.itr.next()
            self.line += skipped_lines     
        else:
            self.tokens.append(Token(OP_A_TOKEN, self.itr.prv, self.line))
        self.initialState()
            
    def delimiterState(self):
        """
        Estado de Delimitadores, criando tokens de delimitadores,
        retornando para o estado inicial pós-identificação de token.

        Returns:
        initialState(): Estado Inicial
        """
        self.tokens.append(Token(DELIMITER_TOKEN, self.itr.cur, self.line))
        self.itr.next()
        self.initialState()

    def opaState(self):
        """
        Estado de Operador Aritmético, criando tokens de OP. Aritmético,
        retornando para o estado inicial pós-identificação de token.

        Returns:
        initialState(): Estado Inicial
        """
        if self.itr.cur in {"*","/"}: #REVIEW / já é pego no comentário
            self.tokens.append(Token(OP_A_TOKEN, self.itr.cur, self.line))
            self.itr.next()
        else:
            if self.itr.cur == self.itr.nxt:
                self.tokens.append(Token(OP_A_TOKEN, self.itr.cur + self.itr.nxt, self.line))
                self.itr.next() # Pulando os 2 elementos de ++ ou -- e indo para o próximo
                self.itr.next()
            else:
                self.tokens.append(Token(OP_A_TOKEN, self.itr.cur, self.line))
                self.itr.next()
        self.initialState()

    def oprState(self):
        """
        Estado de Operador Relacional, criando tokens de OP. Relacional,
        retornando para o estado inicial pós-identificação de token.

        Returns:
        initialState(): Estado Inicial
        """
        if self.itr.nxt == "=":
            self.tokens.append(Token(OP_R_TOKEN, self.itr.cur + self.itr.nxt, self.line))
            self.itr.next()
            self.itr.next()
        else:
            if self.itr.cur == "!":
                self.tokens.append(Token(OP_L_TOKEN, self.itr.cur, self.line))
            else:
                self.tokens.append(Token(OP_R_TOKEN, self.itr.cur, self.line))
            self.itr.next()
        self.initialState()

    def oplState(self):
        """
        Estado de Operador Lógico, criando tokens de OP. Lógico,
        retornando para o estado inicial pós-identificação de token.

        Returns:
        initialState(): Estado Inicial
        """
        if self.itr.cur == self.itr.nxt:
            self.tokens.append(Token(OP_L_TOKEN, self.itr.cur + self.itr.nxt, self.line))
            self.itr.next()
        else:
            self.error_tokens.append(Error_Token(OP_ERROR, self.itr.cur, self.line))
        self.itr.next()
        self.initialState()

    def isAscii(self, char) -> bool:
        """
        Verifica se o caractere está presente no intervalo do alfabeto aceito pelo
        Analisador Léxico

        Returns:
        32 <= ord(char) <= 126
        """
        return 32 <= ord(char) <= 126

    def getErrorTokens(self) -> list:
        '''
        Retorna a lista de tokens de erro
        Returns:
        self.error_tokens: Lista de Error_Tokens
        '''
        return self.error_tokens

    def getTokens(self) -> list:
        return self.tokens

if __name__ == "__main__":
    gt = GenerateTokens('''/* 
	teste08 - sem erros
*/
$ & £
"TESTE STRING SEM FECHAR $
const int MAX = 10ü, MAX2 = 50..3;
	
string Mensagem_testeü = "Hello world $ ü";

procedure start {  // comeca aqui o programa principal 

	int idade ü; 
	real salario;
	string nome;

	print("Digite o nome");
	read(nome);
	print("Digite a idade");A
	read(idade);
	
	if (idade >= 150) print("pode aposentar kkkk");
	else {
		print("vai trabalhar");
		salario = salario; // hehehe
	}	
 
} // fim start''')
    items = gt.initialState()
    for i in items:
        print(i)
    for i in gt.getErrorTokens():
        print(i)