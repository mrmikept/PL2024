# TP6 - Grámatica Independente de Contexto (GIC)

## Data 2024-03-15

## Autor

**Nome:** Mike Pinto

**ID:** A89292

## Objetivo

Construir uma grámatica independente de Contexto (GIC) simples para a seguinte linguagem:

```
?a
b = a * 2 / (27 - 3)
! a + b
c = a * b / (a / b)
```

## Resolução

```
T = {'?', '!', '=', '+', '-', '*', '/', '(', ')', VAR, NUM}
N = {S, Exp, Exp', Termo, Op1, Op2}

P = {

       S -> '?' VAR             LA = {'?'}
          | '!' Exp             LA = {'!'}
          | VAR '=' Exp         LA = {VAR}

    Exp -> Exp' Op1             LA = {'(', NUM, VAR}

    Op1 -> '+' Exp              LA = {'+'}
         | '-' Exp              LA = {'-'}
         | &                    LA = {')', $}

    Exp' -> Termo Op2           LA = {'(', NUM, VAR}

    Op2 -> '*' Exp'             LA = {'*'}
         | '/' Exp'             LA = {'/'}
         | &                    LA = {'+', '-', ')', $}

    Termo -> '(' Exp ')'        LA = {'('}
           | NUM                LA = {NUM}
           | VAR                LA = {VAR}
}
```