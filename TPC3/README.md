# TPC3 - Somador On/Off

## Data: 2024-02-23

## Autor

**Nome:** Mike Pinto

**ID:** A89292

## Objetivo

Criar um programa em *Python* que **some todas as sequências de dígitos** que encontrar em um texto. Caso encontre uma string `Off` ou `On` em qualquer combinação de maiúsculas/minúsculas, o comportamento da soma é desligado/ligado respetivamente. Sempre que encontrar a string `=`, o resultado da soma é colocado à saída.

## Resolução

Para a resolução deste TPC, foram utilizadas expressões regulares para identificar cada tipo de operadores.

Inicialmente é lido todas as linhas de um ficheiro dado como argumento utilizando `text = sys.stdin.readlines()` e iniciada uma variável `sum = 0` responsável por somar todos os números inteiros encontrados e uma variável `state = True` que representa o estado do *somador* (O programa inicia a somar números).

É então iterado por todas as linhas da variável `text`. Para encontrar todos os padrões capturados pela expressão regular definida, é utilizada a função `re.finditer()` cujo seu valor é guardado na variável `matches = re.finditer(inputReg, line)`.

Para cada correspondência encontrada é verificado o grupo pertencente:
- Se a correspondência corresponde ao grupo `on`, é definido o `state = True` para sinalizar que os números deverão ser somados.
- Se a correspondência corresponde ao grupo `off`, é definido o `state = False` para sinalizar que os números não deverão ser somados.
- Se a correspondência corresponde ao grupo `num` e o estado do somador (`state`) for verdadeiro, é somado o valor numérico à variável `sum`.
- Se a correspondência corresponde ao grupo `mostra`, o resultado da soma acumulada é colocado à saída.

### Expressão Regular Utilizada

`(?P<on>[oO][nN])|(?P<off>[oO][fF][fF])|(?P<num>[+-]?\d+)|(?P<mostra>=)`

Esta expressão regular possui 4 grupos nomeados:
- Grupo `on ([oO][nN])` -> Captura strings que possuem a sequência de caracteres `on` (com qualquer combinação de maiúsculas e minúsculas).
- Grupo `off ([oO][fF][fF])` -> Captura strings que possuem a sequência de caracteres `off` (com qualquer combinação de maiúsculas e minúsculas).
- Grupo `num ([+-]?\d+)` -> Captura um número inteiro que opcionalmente pode possuir um sinal de `mais` ou `menos`.
- Grupo `mostra (=)` -> Captura caracteres `=`
