# TPC4 - Analisador Léxico

## Data: 2024-03-01

## Autor

- **Nome:** Mike Pinto
- **ID:** A89292

## Objetivo

Desenvolver um analisador Léxico capaz de interpretar comandos básicos SQL, como:

```sql
Select id, nome, salario 
    From empregados 
    Where salario >= 820
```

## Resolução

Para a resolução deste TPC, foi desenvolvido um script em Python (lexer.py) utilizando o módulo `PLY (Python Lex-Yacc)` presente no Python.

Inicialmente foram definidas as palavras-chave (`KEYWORDS`) reservadas e quais `TOKENS` presentes numa expressão SQL e as respetivas expressões regulares.

O analisador identifica esses tokens no texto passado como argumento e imprime o resultado da análise na sáida (stdout):

```bash
$ Type: {token_type} | Value: {token_Value} | Line Number: {Line_Number_of_Token} | Position: {Position_of_Token_in_Text}
```

## Keywords e Tokens

- `COMMAND` -> Representa comandos sql. Exemplo: `Select; UPDATE; DELETE; WHERE; FROM`. 
**Regex**: `'SELECT|UPDATE|DELETE|WHERE|FROM'`
- `FUNCTION` -> Representa algumas funções sql. Exemplo: `COUNT; AVG; MIN; MAX; SUM`. 
**Regex**: `'COUNT|AVG|MIN|MAX|SUM'`
- `OPERATORS` -> Representa alguns operadores. Exemplo: `<=; >=; =; +; -`. 
**Regex**: `'[\>\<]?=|[+]|[-]'`
- `NUMBERS` -> Representa um valor númerico, com ou sem sinal. Exemplo: `+1; 3; -51`. 
**Regex**: `'[+\-]?\d+'`
- `SEPARATORS` -> Representa caracteres de separação. Exemplo: `,` ou `;`. 
**Regex**: `',|;'`
- `VARIABLES` -> Representa o nome de tabelas ou colunas. Exemplo: `NOME; ID; SALARIO`. 
**REgex**: `'\w+'`
- `LEFT_PAR` e `RIGHT_PAR` -> Representam os parentises. Exemplo: `(` e `)`. 
**Regex**: `'\('` ou `'\)'`

