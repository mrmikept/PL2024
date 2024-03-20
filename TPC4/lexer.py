import ply.lex as lex
import sys

tokens = (
    'COMMAND',
    'FUNCTION',
    'OPERATORS',
    'NUMBERS',
    'SEPARATORS',
    'VARIABLES',
    'LEFT_PAR',
    'RIGHT_PAR'
)

t_COMMAND = r'SELECT|UPDATE|DELETE|WHERE|FROM'
t_FUNCTION = r'COUNT|AVG|MIN|MAX|SUM'
t_OPERATORS = r'[\>\<]?=|[+]|[-]'
t_NUMBERS = r'[+\-]?\d+'
t_SEPARATORS = r',|;'
t_VARIABLES = r'\w+'
t_LEFT_PAR = r'\('
t_RIGHT_PAR = r'\)'


t_ignore = ' \t'

def t_newline(token):
    r'\n+'
    token.lexer.lineno += len(token.value)
    
def t_error(token):
    print(f'Illegal Character "{token.value[0]}"')
    token.lexer.skip(1)

lexer = lex.lex()

text = sys.stdin.read().upper()

lexer.input(text)

for tok in lexer:
    print(f'Type: {tok.type} | Value: {tok.value} | Line Number: {tok.lineno} | Position: {tok.lexpos}')
