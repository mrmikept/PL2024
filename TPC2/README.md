# TPC2 - Conversor de MD para HTML

## Data: 2024-02-16

## Autor

**Nome:** Mike Pinto

**ID:** A89292

## Objetivo

Criar um conversor de ficheiros do tipo *markdown* para ficheiros *HTML* para os seguintes elementos:


>**Cabeçalhos**: Linhas iniciadas por `# texto` ou `## texto` ou `### texto`
>
>**Exemplo:**
>
>   in: `# Exemplo`
>
>   out: `<h1>Exemplo<h1>`

>**Negrito**: Texto entre `**`
>
>**Exemplo:**
>
>   in: `Este é um **exemplo**`
>
>   out: `Este é um <b>exemplo</b>`

>**Itálico**: Texto entre `*`
>
>**Exemplo:**
>
>   in: `Este é um *exemplo*`
>
>   out: `Este é um <i>exemplo</i>`

>**Lista Numerada**: Linhas iniciadas por `um valor numerico e um ponto`
>
>**Exemplo:**
>
>   in: 
>
>   `1. Primera Linha`<br>`2. Segunda Linha` <br> `3. Terceira Linha`
>
>   out:
>
>   `<ol>` <br> `<li> Primera Linha </li>` <br> `<li> Segunda Linha </li>` <br> `<li> Terceira Linha </li>` <br> `</ol>`

>**Endereços URL**: Texto do genero de `[texto](endereço URL)`
>
>**Exemplo:**
>
>   in: `Como pode ser consultado em [página da UC](http://www.uc.pt)`
>
>   out: `Como pode ser consultado em <a href="http://www.uc.pt">página da UC</a>`

>**Imagens**: Texto do genero de `![texto alternativo](caminho da imagem)`
>
>**Exemplo:**
>
>   in: `Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ...`
>
>   out: `Como se vê na imagem seguinte: <img src="http://www.coellho.com" alt="imagem dum coelho"/> ...`

## Resolução

Para a realização deste TPC foram utilizados os módulos `sys` e `re` do **python**.

Inicialmente leu-se o ficheiro dado como argumento ao programa utilizando `sys.stdin.readlines()`.

Para o processamento dos diversos elementos em linguagem `markdown` utilizou-se expressões regulares:

1. Para os **cabeçalhos** é utilizada uma expressão regular que procura por linhas iniciadas por um ou mais `#` e substitui por cabeçalhos em `HTML` `<h1> <h2> e <h3>` conforma a quantidade de `#` presentes.
2. Para o texto em **negrito** ou **itálico** o script envolve o texto entre `*` com tags `<i>` para o **itálico**, já o texto entre `**` o texto é envolvido com tags `bold` para o **negrito**. Para ambos os casos, teve-se o cuidado de a expressão regular dar match em resultados com exatamente dois `*` ou exatamente um `*`.
3. Para as listas numeradas, inicialmente é transformada as linhas iniciadas com um número seguidas de um ponto em items de tag `<li>`. Por fim esses items são agrupados entre tags `<ol>` para formar uma lista númerada.
4. Para **Endereços URL** é substituido o texto na forma de `[texto](endereço url)` por tags de âncora `<a>` com o texto como conteudo e o endereço url como atributo `href`. Na expressão regular utilizada teve-se o cuidado de excluir *matches* que sejam precedidas por um `!` devido a ser a *syntax* em `markdown` para imagem.
5. Para as **imagens** é substituido o texto na forma de `![texto alternativo](caminho da imagem)` por tags de `<img>` com o texto alternativo como atributo `alt` e o caminho da imagem como `src`.

Por fim o script escreve o conteúdo convertido num ficheiro `HTML` chamado de `conversor.html`
