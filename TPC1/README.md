# TPC1 - Análise de um dataset

## Data: 2024-02-09

## Autor

**Nome:** Mike Pinto

**ID:** A89292

## Objetivo

O objetivo deste TPC era analisar um dado dataset, fornecido pela equipa docente, com informações sobre atletas e receber os seguintes resultados:
1. Lista Ordenada de Modalidades Desportivas.
2. Percentagem de Atletas aptos e inaptos para a prática desportiva.
3. Distribuição de atletas por escalão etário (intervalo de 5 anos).

## Resolução

Para a realização deste TPC foram utilizados os módulos **sys** e **math** do Python.

Inicialmente inicializaram-se algumas variáveis:
1. **modalidades**: Lista para armazenar as modalidades encontradas.
2. **aptos** e **inaptos**: Contadores para o número de atletas aptos e inaptos.
3. **nrTotalAtletas**: Contador para o número total de atletas.
4. **distIdades**: Dicionário para armazenar a distribuição de atletas por faixa etária.

É lido do **stdin** linha por linha, o dataset fornecido (recorrendo ao comando *python3 script.py < emd.csv*), ignorando a primeira linha (cabeçalho do dataset).

Para cada linha lida, os campos são extraídos pelo caractere delimitador "," e armazenados numa lista denominada de **campos**.

São então realizadas as seguintes operações:
- Adiciona a modalidade à lista de **modalidades**, se esta ainda não estiver presente.
- Incrementa os contadores **aptos** e **inaptos** com base no valor do campo **Resultado** do dataset (caso o valor seja "*true*" é considerado **apto**, caso seja "*false*" é considerado **inapto**).
- Calcula a faixa etária do atleta, com base na idade (subtraindo à idade do atleta o resto da divisão da sua idade por 5), e atualiza a distribuição de atletas por faixa etária no dicionário **distIdades**.
- Incrementa o contador **nrTotalAtletas**.

Por fim, após processar todas as linhas, é impresso no **stdout** o resultado pretendido.
