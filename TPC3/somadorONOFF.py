import sys
import re

inputReg = r'(?P<on>[oO][nN])|(?P<off>[oO][fF][fF])|(?P<num>[+-]?\d+)|(?P<mostra>=)'

def main(input):
    
    text = sys.stdin.readlines()
    
    sum = 0
    state = True
    
    for line in text:
        matches = re.finditer(inputReg, line) # Cria um iterador sobre a string nas partes onde exista match da expressão regular
        for elem in matches:
            if elem.lastgroup == 'on':
                state = True
            elif elem.lastgroup == 'off':
                state = False
            elif (elem.lastgroup == 'num' and state):
                sum += int(elem.group())
            elif elem.lastgroup == 'mostra':
                print(f'Soma: {sum}')

if __name__ == '__main__':
    main(sys.argv)
