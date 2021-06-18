import os
from generate_tokens import GenerateTokens
from sintax_analyzer import Parser
from sintax_error import SintaxError
from semantic_analyzer import SemanticAnalyzer
path = "./input/"
if os.path.isdir(path):
    files = os.listdir(path)
    if len(files) != 0:
        for file in files:
            if file.endswith(".txt"):
                if file.startswith("entrada"):
                    # Seleciona todos os arquivos de entrada e, para cada um deles, gera um arquivo de saída
                    pathName = open(f"{path}{file}", "r",encoding="utf-8")
                    codigoFonte = pathName.read()
                    out = open("./output/"+file.replace("entrada", "saida"), "w")

                    # Gerando e armazenando tokens e erros
                    gtokens = GenerateTokens(codigoFonte)
                    tokens = gtokens.initialState()
                    lexicalErrors = gtokens.getErrorTokens()
                    
                    # Análise Sintática
                    sintaxParser = Parser(tokens)
                    sintaxResult = sintaxParser.sintaxParser()
                    sintaxErrors = 0
                    
                    # Escrevendo no arquivo de saída
                    for item in sintaxResult:
                        out.write(str(item) + "\n")
                        if type(item) == SintaxError:
                            sintaxErrors += 1
                    out.write("\n")
                    semantic = SemanticAnalyzer(sintaxParser.getTokens())
                    semanticErrors = semantic.symbolTable()

                    for error in semanticErrors:
                        out.write(str(error) + "\n")

                    for error in lexicalErrors:
                        out.write(str(error) + "\n")
                    
                    if len(lexicalErrors) + sintaxErrors + len(semanticErrors) > 0:
                        print (f"ERRO: Encontrados {len(lexicalErrors) + sintaxErrors + len(semanticErrors)} erros durante a leitura do arquivo {file}")
                    else:
                        out.write(f"SUCESSO: O arquivo {file} foi lido com sucesso! Não foram encontrados erros lexicos.")
                        print(f"SUCESSO: O arquivo {file} foi lido com sucesso! Não foram encontrados erros lexicos.")
                else:
                    print(f"ALERTA: O arquivo {file} foi ignorado. Nome do arquivo não corresponde ao padrão estabelecido.")
            else:
                print(f"ERRO: Formato do arquivo {file} não é suportado.")
    else:
        print(f"ERRO: Não foram encontrados arquivos no diretório {path}")
else:
    print(f"ERRO: Diretório {path} não encontrado")
