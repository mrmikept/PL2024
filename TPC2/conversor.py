import re
import sys

file = sys.stdin.readlines()

# Cabeçalhos

markdown = ""

for line in file:
    markdown += line
    

# Processar cabeçalhos -> Linhas que começam por #

markdown = re.sub(r"^(#{1,3})\s(.+)$", lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', markdown, flags=re.MULTILINE)

# Processar texto em Italico -> frases entre um * . Regex: (?<!\*)(\*)(?!\*)(.*?)(\*)(?!\*) (Para não dar match com palavras em bold é utilizado negative-lookahead e negative-lookbehind)

markdown = re.sub(r"(?<!\*)(\*)(?!\*)(.*?)(\*)(?!\*)", r'<i>\2</i>',markdown, flags=re.MULTILINE)

# Processar texto em bold -> frases entre dois *. Regex: (\*\*)(.*?)(\*\*)

markdown = re.sub(r"(\*\*)(.*?)(\*\*)", r'<b>\2</b>', markdown, flags=re.MULTILINE)
      
# Lista numerada
# Aqui primeiro procuramos as linhas que começam por um ou mais digitos e metemos a parte textual entre a tag de <li>
# Por fim é selecionada todas as linhas seguidas que comecem e acabem com a tag <li> e inserimos a tal de <ol>

markdown = re.sub(r'\d\.\s(.*)',r'<li>\1</li>',markdown, flags=re.MULTILINE)
markdown = re.sub(r'(\<li\>.+\<\/li\>(?:(?:\n).+$)*)',r'<ol>\n\1\n</ol>',markdown, flags=re.MULTILINE)

# Processar texto com links -> frases do estilo [texto](link)
# É de notar que a syntax de links e imagens em markdown é bastante semelhante, por isso é preciso inserir um negative lookbehind para descartar todas os matches que possuam um '!' no inicio
# Após isso é só selecionar num grupo o texto entre [ ] e o link entre as ( ).

markdown = re.sub(r'(?<!\!)\[(.+)?\]\((.+)\)',r'<a href="\2">\1</a>', markdown, flags=re.MULTILINE)
    
# Processar uma imagem -> frases do estilo ![texto alternativo](link)
# Muito semelhante ao texto com links. Basta retirar o negative lookbehind

markdown = re.sub(r'!\[(.+)?\]\((.+)\)',r'<img src="\2" alt="\1"/>', markdown, flags=re.MULTILINE)


# Por fim escrever num ficheiro em html
htmlFile = open("conversor.html","w",encoding="utf-8")
htmlFile.write(markdown)

print(markdown)