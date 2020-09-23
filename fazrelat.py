import os

class FazRelat():
    def __init__(self, classificador):
        self.criaPasta()

        self.features = classificador.most_informative_features(1000)
        self.arq = open('relatorio/relatorio.txt', 'w', encoding='utf-8')

        for (palavra, n) in self.features:
            self.arq.write(palavra + '   ' + str(n) + '\n')
        
        self.arq.close()
    
    @staticmethod
    def erros(classificador, baseteste, arqteste):
        FazRelat.criaPasta()

        arq_erros = open('relatorio/erros.txt', 'w', encoding='utf-8')
        conta_erros = dict.fromkeys(classificador.labels(), 0)

        for i in range(len(baseteste)):
            linha = arqteste[i]
            resultado = classificador.classify(baseteste[i][0])
            
            if resultado != baseteste[i][1]:
                arq_erros.write(str(i+1) + " " + linha[0] + " #esperado: " + baseteste[i][1] + " #resultado: " + resultado + "\n")
                conta_erros[baseteste[i][1]] += 1
        
        arq_erros.write("\n")

        total = 0
        for classe in conta_erros:
            arq_erros.write(classe + ": " + str(conta_erros[classe]) + "\n")
            total += conta_erros[classe]
        
        arq_erros.write("Total: " + str(total) + "\n")

        arq_erros.close()
    
    @staticmethod
    def criaPasta():
        if not os.path.isdir('relatorio'):
            os.mkdir('relatorio')
