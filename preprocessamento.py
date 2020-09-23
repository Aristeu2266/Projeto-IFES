class PreProcessamento:
    @staticmethod
    def remove_caracteres(texto, extender=None, caracteres=None):
        """Retorna o 'texto' sem os caracteres contidos em 'caracteres' mais os contidos em extender.

        O parâmetro 'extender' recebe uma lista de caracteres À MAIS (além dos já listados) para serem removidos.

        Caso não queira somente adicionar caracteres, pode passar ao 'extender' uma lista vazia e à 'caracteres' os
        caracteres desejados para serem removidos."""
        if extender == True:
            extender = []
        if caracteres is None:
            caracteres = ["'", '"', '[', ']', '(', ')', '!', '?', ':', ';', ',', '.']

        if extender:
            caracteres.extend(extender)

        for char in caracteres:
            texto = texto.replace(char, '')

        return texto

    @staticmethod
    def transformar_texto(nome_do_arquivo):
        """Retorna uma lista contendo tuplas com a frase e a classe, uma tupla para cada linha sendo a frase e a classe
        separadas por '#label#:'."""
        arq = open(nome_do_arquivo, encoding='utf-8')

        linha = arq.readline().strip().lower()
        separatriz = []

        while linha:
            separatriz.append(linha.split('#label#:'))
            linha = arq.readline().strip().lower()

        dados = []
        for (linha, emocao) in separatriz:
            dados.append((PreProcessamento.remove_caracteres(linha.strip()), emocao.strip()))

        arq.close()

        return dados
