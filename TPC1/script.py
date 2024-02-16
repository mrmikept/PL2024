import sys
import math

modalidades = []
aptos = 0
inaptos = 0
nrTotalAtletas = 0
distIdades : dict[tuple[int,int],int] = {}

stdin = sys.stdin
next(stdin) # Para ignorar a primeira linha do csv

for data in stdin: # Processar a informação das linhas do csv
    linha = data.removesuffix("\n") # Remover o \n do final
    campos = linha.split(",") # Separar os campos pelo caracter delimitador
    
    # Modalidade
    
    if(campos[8] not in modalidades):
        modalidades.append(campos[8])
    
    # Atletas aptos e inaptos
    
    if(campos[12] == "true"):
        aptos += 1
    elif(campos[12] == "false"):
        inaptos += 1
    
    # Intervalo etário
    
    idade = int(campos[5])
    intIdadeMin = idade - (idade % 5)
    intIdadeMax = intIdadeMin + 4
    faixa = (intIdadeMin,intIdadeMax)
    distIdades[faixa] = distIdades.get(faixa,0) + 1
    
    
    nrTotalAtletas += 1


print("### Informações ###\n")

print("# Lista de Modalidades por ordem alfabetica #")
print(modalidades)

print("\n# Percentagem de atletas aptos e inaptos #")
print(f'Aptos: {(aptos / nrTotalAtletas) * 100} %')
print(f'inaptos: {(inaptos / nrTotalAtletas) * 100} %')

print("\n# Distribuição de atletas por escalão etário #")
for escalao in sorted(distIdades.keys()):
    print(f'[{escalao[0],escalao[1]}] - {distIdades[escalao]}')
