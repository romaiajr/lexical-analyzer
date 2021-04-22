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

        Returns:
            getTokens(): Lista de Tokens Válidos
        '''

        while True:
            try:
                self.lexema = ''
                if self.itr.cur == None:
                    return self.getTokens()
                if self.itr.cur.isspace():
                    if self.itr.cur == "\n":
                        self.line+=1
                    self.itr.next()
                elif self.isAscii(self.itr.cur):
                    if self.itr.cur.isidentifier():
                        if self.itr.cur == "_":
                            token = self.symbolState()
                        else:
                            token = self.ideState()
                    elif self.itr.cur.isnumeric():
                        token = self.numberState()
                    else:
                        token = self.symbolState()
                    if isinstance(token,Error_Token):
                        self.error_tokens.append(token)
                    elif isinstance(token,Token) and token != None:
                        self.tokens.append(token)
                else:
                    self.error_tokens.append(Error_Token(OUT_ASCII_ERROR, self.itr.cur, self.line))
                    self.itr.next()
            except StopIteration:
                return self.getTokens()
            
    def ideState(self) -> Token:
        '''
        Estado de Identificadores, responsável por criar 
        tokens de identificadores e palavras reservadas, transicionando para o estado
        inicial, pós-identificação de token.

        Returns:
            Token(): Token de Identificadores ou Palavra Reservada
        '''
        while (self.itr.cur.isidentifier() or self.itr.cur.isnumeric() or self.itr.cur == "_") and self.isAscii(self.itr.cur):
            self.lexema+=self.itr.cur
            self.itr.next()
            if self.itr.cur == None:
                break
        if not self.symbols_table.__contains__(self.lexema): # Insere o na tabela de simbolos
            self.symbols_table.append(self.lexema)
        if self.reservedWords.__contains__(self.lexema): # Caso seja uma palavra reservada
            return Token(RW_TOKEN, self.lexema, self.line)
        else: # Se não for uma palavra reservada, será um identificador
            return Token(ID_TOKEN, self.lexema, self.line)                                    

    def numberState(self) -> Token:
        '''
        Estado inteiro dos Números, responsável por criar 
        tokens de números inteiros. Caso um "." seja encontrado
        ocorrerá uma transição para o estado float, se não, retornará o estado inicial
        pós-identificação de token.

        Returns:
            Token(): Token de Número
            floatState(): Token de Número Float
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
            return Token(NUMBER_TOKEN, self.lexema, self.line)

    def floatState(self) -> Token:
        '''
        Estado Decimal dos Números, responsável por criar tokens de números,
        retornando para o estado inicial pós-identificação de token.

        Returns:
            Token(): Token de Número Float
        '''
        self.itr.next()
        if self.itr.cur.isnumeric():
            while self.itr.cur.isnumeric():
                self.lexema+=self.itr.cur
                self.itr.next()
                if self.itr.cur == None:
                    break
            return Token(NUMBER_TOKEN, self.lexema, self.line)
        else:
            return Error_Token(NUMBER_ERROR, self.lexema, self.line)

    def symbolState(self) -> Token:
        '''
        Estado de Símbolos, responsável por criar transições para
        os estados equivalentes a cada símbolo. Retornará ao estado inicial Caso
        o símbolo não corresponda a nenhum dos estados.

        Returns:
            stringState(): Token de Cadeia de Caracteres
            commentState(): Token de Comentário
            delimiterState(): Token de Delimitador
            opaState(): Token de Operador Aritmético
            oprState(): Token de Operador Relacional
            oplState(): Token de Operador Lógico
            Error_Token(): Token de Erro 
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
            self.itr.next()
            return Error_Token(SYMBOL_ERROR, self.itr.prv, self.line)

    def stringState(self) -> Token:
        """
        Estado de Strings, criando tokens de Cadeia de Caracteres,
        retornando para o estado inicial pós-identificação de token.

        Returns:
            Token(): Token de Cadeia de Caracteres
            Error_Token(): Token de Erro
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
            self.itr.next()
            if contain_no_ascii:
                return Error_Token(STRING_NO_ASCII, self.lexema, self.line)
            else:
                return Token(STRING_TOKEN, self.lexema, self.line)
        else:
            self.line+=1 #REVIEW
            self.itr.next()
            return Error_Token(STRING_ERROR, self.lexema, self.line -1)

    def commentState(self) -> Token:
        """
        Estado de Comentários, criando tokens de comentários,
        retornando para o estado inicial pós-identificação de token.

        Returns:
            Error_Token(): Token de Erro
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
                return Error_Token(COMMENT_ERROR, self.lexema, self.line)
            self.itr.next() # Para pular o */ final
            self.itr.next()
            self.line += skipped_lines     
        else:
            return Token(OP_A_TOKEN, self.itr.prv, self.line)
            
    def delimiterState(self) -> Token:
        """
        Estado de Delimitadores, criando tokens de delimitadores,
        retornando para o estado inicial pós-identificação de token.

        Returns:
            Token(): Token de Delimitador
        """
        self.itr.next()
        return Token(DELIMITER_TOKEN, self.itr.prv, self.line)

    def opaState(self) -> Token:
        """
        Estado de Operador Aritmético, criando tokens de OP. Aritmético,
        retornando para o estado inicial pós-identificação de token.

        Returns:
            Token(): Token de Operador Aritmético
        """
        if self.itr.cur in {"*","/"}: #REVIEW / já é pego no comentário
            self.itr.next()
            return Token(OP_A_TOKEN, self.itr.prv, self.line)
        else:
            if self.itr.cur == self.itr.nxt:
                cur, nxt = self.itr.cur, self.itr.nxt
                self.itr.next() # Pulando os 2 elementos de ++ ou -- e indo para o próximo
                self.itr.next()
                return Token(OP_A_TOKEN, cur + nxt, self.line)
            else:
                self.itr.next()
                return Token(OP_A_TOKEN, self.itr.prv, self.line)

    def oprState(self) -> Token:
        """
        Estado de Operador Relacional, criando tokens de OP. Relacional,
        retornando para o estado inicial pós-identificação de token.

        Returns:
            Token(): Token de Operador Relacional
        """
        if self.itr.nxt == "=":
            cur, nxt = self.itr.cur, self.itr.nxt
            self.itr.next()
            self.itr.next()
            return Token(OP_R_TOKEN, cur + nxt, self.line) 
        else:
            if self.itr.cur == "!":
                self.itr.next()
                return Token(OP_L_TOKEN, self.itr.prv, self.line)
            else:
                self.itr.next()
                return Token(OP_R_TOKEN, self.itr.prv, self.line)

    def oplState(self) -> Token:
        """
        Estado de Operador Lógico, criando tokens de OP. Lógico,
        retornando para o estado inicial pós-identificação de token.

        Returns:
            Token(): Token de Operador Lógico
        """
        if self.itr.cur == self.itr.nxt:
            cur, nxt = self.itr.cur, self.itr.nxt
            self.itr.next() # Pulando os 2 elementos de ++ ou -- e indo para o próximo
            self.itr.next()
            return Token(OP_L_TOKEN, cur + nxt, self.line)
        else:
            self.itr.next()
            return Error_Token(OP_ERROR, self.itr.prv, self.line)

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
    gt = GenerateTokens('''string _msg = "teste''')
    items = gt.initialState()
    for i in items:
        print(i)
    for i in gt.getErrorTokens():
        print(i)