import ply.lex as lex
import json
import sys
import re
from datetime import date
from tabulate import tabulate

class VendingMachine:
    
    def __init__(self):
        self.stock = {}
        self.saldo = 0
        self.on = False
        self.lex = lex.lex(module=self)
        self.manutencao = False
        
    tokens = (
        'LISTAR',
        'MOEDA',
        'SELECIONAR'
        'SALDO'
        'AJUDA'
        'CARREGAR'
        'ADICIONAR'
        'SAIR'
        'ALTERAR'
        'MANUTENCAO'
    )
    
    def lerStock(self, pathJson):
        try:
            with open(pathJson,"r", encoding='UTF-8') as jsonFile:
                jsonData = json.load(jsonFile)

                stock = {}

                for item in jsonData:
                    key = item["cod"]
                    value = (item['nome'], int(item["quant"]), float(item["preco"]))
                    stock[key] = value

                self.stock = stock
                print(f'maq: {date.today()}, Stock Carregado, Estado Atualizado.')
        
        except FileNotFoundError:
            print(f'maq: Ficheiro "{pathJson}" de Stock não encontrado.')
            print("maq: A encerrar sistema...")
            sys.exit(1)
        except Exception as e:
            print(f'maq: Ocorreu um erro: {e}')
            print("maq: A encerrar sistema...")
            sys.exit(1)
            
    def guardaStock(self, pathJson):
        stock = []
        
        for key, value in self.stock.items():
            stock.append({
                "cod" : key,
                "nome" : value[0],
                "quant" : value[1],
                "preco" : value[2]
            })
            
        with open(pathJson, "w", encoding='UTF-8') as jsonFile:
            json.dump(stock,jsonFile,indent=2)
            
        print("maq: Alterações no stock registadas com sucesso!")

    def ligarVending(self):
        self.on = True
        print(f'maq: Bom dia. Estou dísponivel para atender ao seu pedido.')
        print(f'maq: Insira "AJUDA" para obter o manual de utilização.')
    
    def t_LISTAR(self, token):
        r'LISTAR'
        
        header = ['CÓDIGO','NOME','QUANTIDADE','PREÇO']
        data = []
        for key, value in self.stock.items():
            item = [key,value[0],value[1],str(value[2]) + " €"]
            data.append(item)
            
        print(tabulate(data, headers=header, tablefmt="rounded_outline"))
    
    def t_ADICIONAR(self, token):
        r'ADICIONAR\s+(.+?)\s*,*\s*"(.+?)"\s*,*\s*(\d+)\s*,*\s*(\d\.*\d*)'
        
        if self.manutencao:
            m = re.match(r'ADICIONAR\s+(?P<COD>.+?)\s*,*\s*"(?P<NOME>.+?)"\s*,*\s*(?P<QUANT>\d+)\s*,*\s*(?P<VALOR>\d\.*\d*)', token.value)
            cod = m.group('COD')

            if cod not in self.stock.keys():
                self.stock[cod] = (nome, quant, valor)
                nome = m.group('NOME')
                quant = int(m.group('QUANT'))
                valor = float(m.group('VALOR'))
                print(f'maq: Artigo adicionado: Código = {cod}; Nome = "{nome}"; Quantidade = {quant}; Valor = {valor}')
            else:
                print(f'maq: Código: {cod} já existente no sistema.')
                print(f'maq: Para alterar os dados de um artigo utilize o comando: "ALTERAR". Consulte o comando "AJUDA" para mais informações.')
        else:
            print("maq: Necessário ativar o modo de Manutenção para aceder a esta funcionalidade!")
            print('maq: Ative o modo de Manutenção com o comando: "MANUTENCAO". Use o comando "AJUDA" para mais informações.')
        
    def t_REMOVE(self, token):
        r'REMOVE\s+(.+?)'
        
        if self.manutencao:
            m = re.match(r'REMOVE\s+(?P<COD>.+?)')   
            cod = m.group('COD')
            if cod in self.stock.keys():
                self.stock.pop(cod)
                print(f'maq: Artigo Removido: {cod}.')
            else:
                print(f'maq: Código de Artigo não encontrado: {cod}')
        else:
            print("maq: Necessário ativar o modo de Manutenção para aceder a esta funcionalidade!")
            print('maq: Ative o modo de Manutenção com o comando: "MANUTENCAO". Use o comando "AJUDA" para mais informações.')
    
    def t_ALTERAR(self, token):
        r'ALTERAR\s+(\w\d+)\s*,*\s*(\w+)\s*,*\s*"?(.+)"?'
        
        if self.manutencao:
            m = re.match(r'ALTERAR\s+(?P<COD>\w\d+)\s*,*\s*(?P<CAMPO>\w+)\s*,*\s*"?(?P<VAR>.+)"?', token.value)
            cod = m.group('COD')

            if cod in self.stock.keys():
                campo = m.group('CAMPO').upper()
                match campo:
                    case 'CODIGO':
                        item = self.stock.pop(cod)
                        self.stock[m.group('VAR')] = item
                        print(f'maq: Código do artigo: "{item[0]}" alterado de "{cod}" para "{m.group("VAR")}".')
                    case 'NOME':
                        item = self.stock[cod]
                        self.stock[cod] = (m.group('VAR'), item[1], item[2])
                        print(f'maq: Nome do artigo "{cod}" alterado de "{item[0]}" para "{m.group("VAR")}".')
                    case 'QUANTIDADE':
                        item = self.stock[cod]
                        self.stock[cod] = (item[0], int(m.group('VAR')), item[2])
                        print(f'maq: Quantidade do artigo "{cod}" alterado para {m.group("VAR")}.')
                    case 'PRECO':
                        item = self.stock[cod]
                        self.stock[cod] = (item[0], item[1], float(m.group('VAR')))
                        print(f'maq: Preço do artigo "{cod}" alterado para {m.group("VAR")}.')
                    case _:
                        print(f'Campo não reconhecido: {m.group("CAMPO")}')
            else:
                print(f"maq: Código de artigo não encontrado: {cod}.")    
        else:
            print("maq: Necessário ativar o modo de Manutenção para aceder a esta funcionalidade!")
            print('maq: Ative o modo de Manutenção com o comando: "MANUTENCAO". Use o comando "AJUDA" para mais informações.')

        
    def t_CARREGAR(self, token):
        r'CARREGAR\s+(.+?)\s+(\d+)'
        
        if self.manutencao:
            m = re.match(r'CARREGAR\s+(?P<COD>.+?)\s+(?P<QUANT>\d+)', token.value)
            cod = m.group('COD')
            quant = int(m.group('QUANT'))

            if cod in self.stock.keys():
                nome, quantItem, preco = self.stock[cod]
                quantItem += quant

                self.stock[cod] = (nome, quantItem, preco)
                
                print(f'maq: Quantidade do artigo {nome}, carregado para {quantItem}.')
        else:
            print("maq: Necessário ativar o modo de Manutenção para aceder a esta funcionalidade!")
            print('maq: Ative o modo de Manutenção com o comando: "MANUTENCAO". Use o comando "AJUDA" para mais informações.')

    def t_SALDO(self, token):
        r'SALDO'
        self.showSaldo()
        
    def t_AJUDA(self, token):
        r'AJUDA'
        
        print("maq: Comandos dísponiveis:")
        header = ['COMANDO', 'DESCRIÇÃO']
        data= [
            ['LISTAR', 'Lista os Artigos Presentes na Máquina.'],
            ['MOEDA <moeda1>, <moeda2>, ...', 'Carrega moedas para o saldo. Moedas aceites: 2e, 1e, 50c, 20c, 10c, 5c e 2c'],
            ['SALDO', 'Apresenta o saldo dísponivel restante.'],
            ['SELECIONAR <codArtigo>','Seleciona um artigo para comprar.'],
            ['SAIR','Devolve o troco restante, atualiza a lista de Stock e encerra a Máquina.'],
            ['MANUTENCAO','Ativa/Desativa o Modo de manutenção da Máquina de Vending, somente a ser usado por funcionários.'],
            ['CARREGAR','Adicionar uma determinada quantidade a um artigo. Somente dísponível no modo de Manutenção. Modo de uso: "CARREGAR <Código>, <Quantidade>"'],
            ['ADICIONAR','Adiciona um artigo novo à maquina. Somente dísponivel no modo de Manutenção. Modo de uso: "ADICIONAR <Código>, <Nome Artigo>, <Quantidade>, <Preço>"'],
            ['ALTERAR','Alterar algum dado de um determinado Artigo. Somente dísponivel no modo de Manutenção. Modo de uso: "ALTERAR <Código>, <Campo a Alterar>, <Valor do Campo>"']
        ]
        print(tabulate(data, headers=header))
    
    def t_MANUTENCAO(self, token):
        r'MANUTENCAO'
        
        self.manutencao = not self.manutencao
        if self.manutencao:
            print("maq: Modo de Manutenção ativado!")
        else:
            print("maq: Modo de Manutenção desativado!")
            
    
    def t_MOEDA(self, token):
        r'MOEDAS?\s+((1|2)[eE]|(2|5|10|20|50)[cC])((?:\s*,*\s*)((1|2)[eE]|(2|5|10|20|50)[cC]))*'
        
        for moeda in re.finditer(r'(?P<CENTS>1|2|5|10|20|50)C|(?P<EURO>1|2)E', token.value.upper()):
            if moeda.lastgroup == 'CENTS':
                self.saldo += int(moeda.group('CENTS'))
            elif moeda.lastgroup == 'EURO':
                self.saldo += int(moeda.group('EURO')) * 100
            else:
                print("maq: Moedas inseridas inválidas!")
                print("maq: Moedas Aceites:")
                print("-> Centimos: 1c, 2c, 5c, 10c, 20c, 50c")
                print("-> Euro: 1e, 2e")
        
        self.showSaldo()
        
    def t_error(self, token):
        print(f'Comando não reconhecido: "{token.value}"\nmaq: Insira "AJUDA" para ver a lista de comandos.')
        token.lexer.skip(len(token.value))
    
    
    def t_SELECIONAR(self, token):
        r'SELECIONA(R)?\s+(.+)'
        
        isMatch = re.match(r'^SELECIONAR\s+(?P<COD>.+)',token.value)
        if(isMatch):
            itemCod = isMatch.group('COD')
            if(itemCod in self.stock.keys()):
                nome, quant, preco_ = self.stock.get(itemCod)
                preco = preco_ * 100
                if (quant > 0):
                    if (self.saldo >= preco):
                        quant -= 1
                        self.stock.update({itemCod : (nome, quant, preco_)})
                        
                        print(f'maq: Pode retirar o produto dispensado: "{nome}"')
                        self.saldo -= int(preco)
                        self.showSaldo()
                    else:
                        print('maq: Saldo insuficiente para satisfazer o pedido!')
                        euro, cents = self.calcValor(preco)
                        print(f'maq: Pedido = {int(euro)}e{int(cents)}c')
                        self.showSaldo()
                else:
                    print(f'maq: Produto esgotado: "{nome}"')
                    print('maq: Escolha outro Produto!')
            else:
                print(f'maq: Código de artigo inexistente: {itemCod}.')
                
    def t_SAIR(self, token):
        r'SAIR'
        
        if self.saldo == 0:
            print('maq: Sem Troco a Devolver.')
        else:
            output = 'maq: Pode Retirar o Troco: '
            trocoList = []
            moedasEuro = [200, 100]
            moedasCents = [50, 20, 10, 5, 2]
            
            for moeda in moedasEuro:
                quant, resto = divmod(self.saldo,moeda)
                if quant != 0:
                    trocoList.append(f'{quant}x {moeda / 100}e')
                self.saldo = resto
                
            for moeda in moedasCents:
                if self.saldo == 0:
                    break
                quant, resto = divmod(self.saldo,moeda)
                if quant != 0:
                    trocoList.append(f'{quant}x {moeda}c')
                self.saldo = resto
                
            for i in range(len(trocoList)):
                output += trocoList[i]
                
                if i < len(trocoList) - 2:
                    output += ", "
                elif i < len(trocoList) - 1:
                    output += " e "
            
            output += '.'
            print(output)
        
        self.on = False
        print('maq: Até à próxima!')        
                    
    def calcValor(self, valor):
        return divmod(valor,100)
    
    def showSaldo(self):
        euroValue, centsValue = self.calcValor(self.saldo)
        if euroValue == 0 and centsValue != 0:
            print(f'maq: Saldo = {centsValue}c')
        elif centsValue == 0 and euroValue == 0:
            print('maq: Sem Saldo dísponivel.')
        else:
            print(f'maq: Saldo = {euroValue}e{centsValue}c')
            
        
def main(args):
    if(len(args) < 2):
        print("Número de Argumentos insuficientes! Tente")
        print('"python3 vendingMachine.py <caminho Para json de Stocks>"')
        sys.exit(1)
    
    vending = VendingMachine()
    vending.lerStock(args[1])
    vending.ligarVending()
    
    while(vending.on):
        try:
            data = input('>> ')
            vending.lex.input(data)
            vending.lex.token()
        except KeyboardInterrupt:
            print("\nmaq: Erro na leitura do Teclado...\nmaq: A encerrar Máquina... Até à próxima!")
            break
        except EOFError:
            print("maq: Erro na leitura do Teclado...\nmaq: A encerrar Máquina... Até à próxima!")
            break
        
    vending.guardaStock(args[1])


if __name__ == '__main__':
    main(sys.argv)