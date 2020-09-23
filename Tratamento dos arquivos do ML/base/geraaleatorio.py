import json
import os
import random


class GeraAleatorio:
    def __init__(self):
        assert os.path.exists('Fonte das reviews/positivas.txt')
        assert os.path.exists('Fonte das reviews/negativas.txt')
        assert os.path.exists('opcoes.txt')

        self.opcoes = self.getoptions()
        self.nomesdearquivos = {'ambos': '', 'positivas': '', 'negativas': ''}

        if self.opcoes['Ambos juntos']:
            assert int(self.opcoes['Linhas do arquivo positivo']) > 0
            assert int(self.opcoes['Linhas do arquivo negativo']) > 0

            print('Criando o arquivo de reviews negativas e positivas')
            self.criaarquivo('ambos', self.opcoes['Linhas do arquivo positivo'], self.opcoes['Linhas do arquivo negativo'])
            print('Arquivo criado')
            print('Nome do arquivo:', self.nomesdearquivos['ambos'])
            print('Adicionando as reviews positivas')
            self.geralinhasaleatorias('positivas', self.opcoes['Linhas do arquivo positivo'], 'ambos')
            print('Reviews positivas adicionadas')
            print('Adicionando as reviews negativas')
            self.geralinhasaleatorias('negativas', self.opcoes['Linhas do arquivo negativo'], 'ambos')
            print('Reviews negativas adicionadas')
        else:
            if self.opcoes['Arquivo negativo']:
                print('Criando o arquivo de reviews negativas')
                self.criaarquivo('negativas', self.opcoes['Linhas do arquivo negativo'])
                print('Arquivo criado')
                print('Nome do arquivo:', self.nomesdearquivos['negativas'])
                print('Adicionando reviews negativas')
                self.geralinhasaleatorias('negativas', self.opcoes['Linhas do arquivo negativo'])
                print('Reviews negativas adicionadas')
            if self.opcoes['Arquivo positivo']:
                print('Criando o arquivo de reviews positivas')
                self.criaarquivo('positivas', self.opcoes['Linhas do arquivo positivo'])
                print('Arquivo criado')
                print('Nome do arquivo:', self.nomesdearquivos['positivas'])
                print('Adicionando reviews positivas')
                self.geralinhasaleatorias('positivas', self.opcoes['Linhas do arquivo positivo'])
                print('Reviews positivas adicionas')

    def geralinhasaleatorias(self, tipo, qtdlinhas, nome=''):
        assert tipo == 'negativas' or tipo == 'positivas' or tipo == 'ambos'

        if not nome:
            nome = tipo

        linhas = 0
        listalinhas = [0]

        porcentagem = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', '']

        while linhas < qtdlinhas and len(listalinhas) > 0:
            with (open(self.nomesdearquivos[nome], 'a', encoding='utf-8')) as arqNovo:
                with (open(os.path.join('Fonte das reviews', tipo + '.txt'), encoding='utf-8')) as arq:
                    listalinhas = arq.readlines()

                for i in listalinhas:
                    escolha = random.randint(0, 1)
                    if escolha:
                        arqNovo.write(i)
                        linhas += 1
                        if porcentagem[int((linhas / qtdlinhas) * 10)] != '':
                            print(porcentagem[int((linhas / qtdlinhas) * 10)])
                            porcentagem[int((linhas / qtdlinhas) * 10)] = ''
                        if linhas == qtdlinhas:
                            break

            print('Reescrevendo arquivo ' + tipo + '.txt')
            with (open(self.nomesdearquivos[nome], encoding='utf-8')) as arqNovo:
                linhasselecionadas = arqNovo.readlines()
                self.removelinha(os.path.join('Fonte das reviews', tipo + '.txt'), linhasselecionadas)
        print()

    @staticmethod
    def trocanome(nome):
        final = nome
        nome = nome.replace('.txt', '')
        tentativa = 2
        while os.path.exists(final):
            final = nome + "(" + str(tentativa) + ").txt"

        return final

    @staticmethod
    def removelinha(arquivo, linhasremovidas):
        with open(arquivo, "r", encoding='utf-8') as f:
            lines = f.readlines()

        porcentagem = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', '']
        with open(arquivo, "w", encoding='utf-8') as f:
            for i in range(len(lines)):
                if lines[i] not in linhasremovidas:
                    f.write(lines[i])
                    if porcentagem[int((i / len(lines)) * 10)] != '':
                        print(porcentagem[int((i / len(lines)) * 10)])
                        porcentagem[int((i / len(lines)) * 10)] = ''
            print()

    @staticmethod
    def getoptions():
        with (open('opcoes.txt', encoding='utf-8')) as arq:
            text = arq.read()

        return json.loads(text)

    def criaarquivo(self, tipo, linhas, linhas2=False):
        if linhas2:
            linhas = str(linhas) + '_' + str(linhas2)

        fd = False
        tentativa = 2
        complemento = ''
        while not fd:
            try:
                self.nomesdearquivos[tipo] = tipo + str(linhas) + complemento + '.txt'
                if not os.path.exists(self.nomesdearquivos[tipo]):
                    arq = open(self.nomesdearquivos[tipo], 'a', encoding='utf-8')
                    arq.close()
                    fd = True
                else:
                    raise FileExistsError
            except FileExistsError:
                complemento = ' (' + str(tentativa) + ')'
                tentativa += 1


if __name__ == '__main__':
    a = GeraAleatorio()
