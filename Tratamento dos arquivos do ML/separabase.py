from datetime import datetime
import os
from shutil import copy


class Main:
    def __init__(self):
        self.foldername = self.nome()
        self.criapasta(self.foldername)

        os.mkdir(os.path.join(self.foldername, 'Fonte das reviews'))
        copy('base/negativas.txt', os.path.join(self.foldername, 'Fonte das reviews'))
        copy('base/positivas.txt', os.path.join(self.foldername, 'Fonte das reviews'))
        copy('base/opcoes.txt', self.foldername)
        copy('base/geraaleatorio.py', self.foldername)

    @staticmethod
    def criapasta(foldername):
        fd = False
        tentativa = 2
        complemento = ''
        while not fd:
            try:
                os.mkdir(foldername + complemento)
                fd = True
            except FileExistsError:
                complemento = ' (' + str(tentativa) + ')'
                tentativa += 1

    @staticmethod
    def nome():
        hoje = datetime.now()
        return str(hoje.day) + '_' + str(hoje.hour) + '_' + str(hoje.minute)


if __name__ == '__main__':
    a = Main()
