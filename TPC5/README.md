# TPC5 - Máquina de Vending

## Data: 2024-03-08

## Autor

**Nome:** Mike Pinto

**ID:** A89292

## Objetivo

Desenvolver um programa que simule uma máquina de Vending.

A máquina tem um stock de produtos: uma lista de triplos, nome do produto, quantidade e preço.

```json
stock = [
 {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7},
 ...
]
```

A lista de stock pode persistir num ficheiro em JSON que é carregado no arranque do programa e é atulizado
quando o programa termina.

A seguir apresenta-se um exemplo de uma interação com a máquina, assim que esta é ligada:

```bash
maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
cod | nome | quantidade |  preço
---------------------------------
A23 água 0.5L 8 0.7
...
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> SELECIONAR A23
maq: Saldo insufuciente para satisfazer o seu pedido
maq: Saldo = 60c; Pedido = 70c
>> ...
...
maq: Saldo = 74c
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
maq: Até à próxima
```

## Resolução

Para a resolução deste TPC recorreu-se à linguaguem de programação python e ao modulo `PLY (Python Lex-Yacc)`, o modulo `json` para interpretar a lista de stocks e ainda ao modulo `tabulate`.

O modulo tabulate pode ser instalado usando um dos seguintes comandos na `shell`:

```shell
$ pip install tabular (non-arch systems)
$ sudo pacman -S python-tabular (arch systems)
```

Foi então implementada uma classe `VendingMachine` onde irão constar todas as operações necessárias para o funcionamento da máquina de vending, cujas váriaveis de instacia são:

- `stock`: Dicionário com o Stock de artigos da Maquina.
- `saldo`: Saldo dísponivel na máquina. Por omissão 0.
- `on`: Váriavel booleana que representa o estado de ligado/desligado da máquina.
- `lex`: Objeto de lex.
- `manutencao`: Váriavel booleana que representa se a máquina está em estado de manutenção ou não.

Está classe é responsável por ler e escrever no ficheiro json de stock, cujo caminho é passado como argumento ao programa, fazer gestão do stock e saldo da máquina e interpretar os comandos enviados pelo utilizador.
Para além dos comandos apresentados no enunciado: `LISTAR; MOEDA; SELECIONAR e SAIR` foram ainda implementados os comandos: `AJUDA; MANUTENCAO; CARREGAR; ADICIONAR; REMOVE e ALTERAR`.

- `LISTAR` -> Lista a informação dos artigos presentes na máquina.
- `MOEDA :moeda1:, :moeda2:, ...` -> Carregar saldo na máquina.
- `SELECIONAR :codigo:` -> Seleciona um artigo para comprar.
- `SALDO` -> Devolve o saldo dísponivel na máquina.
- `AJUDA` -> Apresenta o manual de utilização da Máquina.
- `MANUTENCAO` -> Ativa/Desativa o modo de manutenção da Máquina.
- `CARREGAR :código: :quantidade:` -> Adiciona uma determinada quantidade a um artigo. 
- `ADICIONAR :codigo:, :nome:, :quantidade:, :preço:` -> Adiciona um novo artigo à Máquina.
- `REMOVE :código:` -> Remove um artigo da Máquina.
- `ALTERAR :código: :campo: :valor:` -> Altera um determinado dado de um artigo.

### Tokens definidos

Começamos então por definir os tokens utilizados para a operar a máquina de vending:

- `LISTAR`
- `MOEDA`
- `SELECIONAR`
- `SALDO`
- `AJUDA`
- `MANUTENCAO`
- `CARREGAR`
- `ADICIONAR`
- `REMOVE`
- `ALTERAR`

### Funções implementadas

- `lerStock` -> Responsavel por ler o stock e povoar o dicionario de stock da máquina com a informação dos artigos. Possui ainda a verificação para quando o ficheiro não é encontrado ou se ocorrer algum erro na leitura do mesmo.

- `guardaStock` -> Responsavel por escrever o stock em ficheiro no final do uso da máquina.

- `ligarVending` -> Altera o estado da máquina para ligado.

- `t_LISTAR` -> Lista o artigos presentes na máquina de vending e as respetivas informações. Exemplo:
```shell
>> LISTAR
╭──────────┬───────────────────┬──────────────┬─────────╮
│ CÓDIGO   │ NOME              │   QUANTIDADE │ PREÇO   │
├──────────┼───────────────────┼──────────────┼─────────┤
│ B12      │ Café              │           15 │ 1.2 €   │
│ C45      │ Batatas Fritas    │           10 │ 1.0 €   │
│ D67      │ Chocolate         │           20 │ 0.8 €   │
│ E89      │ Refrigerante 0.5L │           12 │ 1.5 €   │
│ F34      │ Bolachas          │           18 │ 0.6 €   │
│ G56      │ Sandes de Frango  │            5 │ 2.0 €   │
│ H78      │ Sopa Instantânea  │            7 │ 1.3 €   │
│ I90      │ Maçã              │            9 │ 0.9 €   │
│ J01      │ Amendoins         │           11 │ 0.75 €  │
│ A33      │ Água 0.5 ml       │           15 │ 0.7 €   │
╰──────────┴───────────────────┴──────────────┴─────────╯
```

- `t_SALDO` -> Responsável por escrever para o `stdout` o valor do saldo dísponivel na máquina. Comando `SALDO`. Expressão Regular Utilizada: `SALDO`.

- `t_AJUDA` -> Responsável por escrever para o `stdout` a lista de comandos dísponiveis na máquina e a respetiva descrição.  Comando `AJUDA`. Expressão Regular Utilizada: `AJUDA`. 

- `t_MOEDA` -> Responsável por adicionar saldo na máquina de vending. Comando: `MOEDA :moeda1:, :moeda2:, ...`. Exemplo: `MOEDA 1e, 2e, 20c`. Expressão Regular utilizada: `MOEDAS?\s+((1|2)[eE]|(2|5|10|20|50)[cC])((?:\s*,*\s*)((1|2)[eE]|(2|5|10|20|50)[cC]))*`. Exemplo:

```shell
>> MOEDA 1e 2e 50c 5c 2c 1e
maq: Saldo = 4e57c
```

- `t_SELECIONAR` -> Responsável por atualizar o estado do stock de um determinado artigo e o saldo do utilizador na "compra" de um artigo. Possui verificações caso o código de artigo inserido não exista e para o caso do utilizador não possuir saldo suficiente. Comando: `SELECIONAR :código:`. Expressão Regular utilizada: `SELECIONA(R)?\s+(.+)`.

Exemplo: 

```shell
>> SELECIONAR A33
maq: Pode retirar o produto dispensado: "Água 0.5 ml"
maq: Saldo = 3e87c
```

- `t_SAIR`: -> Responsável por definir o estado da máquina para desligado e escrever para o `stdout` o troco dividio por moedas, caso o utilizador possua saldo dísponivel. Comando `SAIR`. Expressão Regular utilizada: `SAIR`

Exemplo:

```shell
>> SAIR
maq: Pode Retirar o Troco: 1x 2.0e, 1x 1.0e, 1x 50c, 1x 20c, 1x 10c, 1x 5c e 1x 2c.
maq: Até à próxima!
```

- `t_MANUTENCAO` -> Responsável por ativar ou desativar o modo de manutenção da Máquina de Vending. Comando `MANUTENCAO`. Expressão REgular Utilizada: `MANUTENCAO`

- `t_ADICIONAR` -> Reponsável por adicionar novos artigos na máquina. Possui verificações para o caso de já existir algum artigo com o código inserido. Comando: `ADICIONAR :código:, :nome:, :quantidade:, :preço:`. Expressão regular utilizada: `ADICIONAR\s+(.+?)\s*,*\s*"(.+?)"\s*,*\s*(\d+)\s*,*\s*(\d\.*\d*)`.
Comando apenas dísponivel no modo de manutenção.

- `t_REMOVE` -> Responsável por remover um artigo da máquina. Verifica se existe algum artigo com o código inserido ou a máquina não esteja em modo de manutenção. Comando: `REMOVE :código:`.
Expressão regular utilizada: `REMOVE\s+(.+?)`.
Comando apenas dísponivel em modo de manutenção.

- `t_ALTERAR` -> Responsável por alterar a informação de um determinado artigo. Possui verificações para o caso do código de artigo inserido não exista ou a máquina não esteja em modo de manutenção. Comando: `ALTERAR :código: :campo: :valor:`. Exemplo: `ALTERAR A23 NOME Chocolate Branco`.
Comando apenas dísponivel em modo de manutenção.

- `t_CARREGAR` -> Responsável por adicionar uma determinada quantidade a um artigo. Possui verificações caso o código do artigo inserido não seja reconhecido ou a máquina não esteja em modo de manutenção. Comando: `CARREGAR :código: :quantidade:`.
Comando apenas dísponivel em modo de manutenção.

### Modo de utilização

Para iniciar a máquina de vending é necessário possuir um ficheiro Json com a lista de stocks (ver ficheiro `stock.json`) e passar o seu caminho como argumento ao programa:
```bash
python3 vendingMachine.py stocks.json
maq: 2024-03-23, Stock Carregado, Estado Atualizado.
maq: Bom dia. Estou dísponivel para atender ao seu pedido.
maq: Insira "AJUDA" para obter o manual de utilização.
>> 
```