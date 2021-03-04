import os
files = os.listdir("./input/")
for file in files:
    pathName = open("./input/"+file, "r")
    out = open("./output/"+file.replace("entrada", "saida"), "w")
    codigoFonte = pathName.read()