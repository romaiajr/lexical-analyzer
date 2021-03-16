import os
from generate_tokens import GenerateTokens
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
                    errors = gtokens.getErrorTokens()

                    # Escrevendo no arquivo de saída
                    for token in tokens:
                        out.write(str(token) + "\n")
                    out.write("\n")
                    for error in errors:
                        out.write(str(error) + "\n")
                    
                    if len(errors) > 0:
                        print (f"ERRO: Encontrados {len(errors)} erros durante a leitura do arquivo {file}")
                    else:
                        out.write(f"SUCESSO: O arquivo {file} foi lido com sucesso! Não foram encontrados erros.")
                        print(f"SUCESSO: O arquivo {file} foi lido com sucesso! Não foram encontrados erros.")
                else:
                    print(f"ALERTA: O arquivo {file} foi ignorado. Nome do arquivo não corresponde ao padrão estabelecido.")
            else:
                print(f"ERRO: Formato do arquivo {file} não é suportado.")
    else:
        print(f"ERRO: Não foram encontrados arquivos no diretório {path}")
else:
    print(f"ERRO: Diretório {path} não encontrado")
