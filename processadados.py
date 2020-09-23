import nltk
from preprocessamento import PreProcessamento


def concatena_stopwords():
    stopwords_f = open('extrastopwords.txt', 'a', encoding='utf-8')
    stopwords_f.close()
    
    stopwords_f = open('extrastopwords.txt', 'r', encoding='utf-8')
    linha = stopwords_f.readline().strip()
    while linha:
        stopwords.append(linha)
        linha = stopwords_f.readline().strip()
    stopwords_f.close()


# Recebe da biblioteca nltk as stopwords em português para serem removidas da base de dados de treinamento
stopwords = nltk.corpus.stopwords.words('portuguese')
concatena_stopwords()


class ProcessaDados:
    """A classe possui métodos que irão aplicar algoritmos que processarão a matriz de dados para que possa ser criada
    a lista que será utilizada no treinamento do classificador."""

    @staticmethod
    def aplica_stemming(base_de_dados):
        """Retorna uma lista com uma tupla para cade elemento da base_de_dados contendo uma lista com strings dos
        radicais de cada palavra e também a string da classe."""
        stemmer = nltk.stem.RSLPStemmer()

        frases_com_stemming = []
        for (frase, emocao) in base_de_dados:
            com_stemming = []
            for palavra in frase.split():
                stemmado = str(stemmer.stem(palavra))
                if palavra not in stopwords and stemmado not in stopwords:
                    com_stemming.append(stemmado)
            #com_stemming = [str(stemmer.stem(palavra)) for palavra in frase.split() if palavra not in stopwords]
            frases_com_stemming.append((com_stemming, emocao))

        return frases_com_stemming

    @staticmethod
    def aplica_stemming_frase(frase):
        """Retorna uma lista com os radicais das palavras.

        Recebe uma string."""
        stemmer = nltk.stem.RSLPStemmer()

        frases_com_stemming = [str(stemmer.stem(palavra)) for palavra in frase.split() if palavra not in stopwords]

        return frases_com_stemming

    @staticmethod
    def lista_de_palavras(base_com_stemming):
        """Retorna uma lista com todos os radicais que estão na base de dados."""
        todas_as_palavras = []
        for (frase, emocao) in base_com_stemming:
            todas_as_palavras.extend(frase)

        return todas_as_palavras

    @staticmethod
    def busca_frequencia(lista_de_todas_palavras):
        """Retorna um objeto FreqDist da biblioteca nltk que carrega consigo a frequencia das palavras da lista
        passada."""
        return nltk.FreqDist(lista_de_todas_palavras)

    @staticmethod
    def lista_de_palavras_unicas(frequencia):
        """Retorna um objeto dict_keys das palavras passadas para a frequência sem palavras repetidas."""
        return frequencia.keys()

    @staticmethod
    def busca_caracteristicas(frase, palavras_unicas):
        """Retorna um dicionário com as palavras da base de dados (palavras_unicas) dizendo se a frase passada às contem
        ou não."""
        caracteristicas = {}
        for palavra in palavras_unicas:
            caracteristicas[palavra] = frase.count(palavra)

        return caracteristicas

    @staticmethod
    def finaliza_base_completa(base_com_stem, palavras_unicas):
        """Retorna a lista a ser usada para o treinamento do classificador.
        Uma lista contendo tuplas sendo que cada tupla contém um dicionário com as "características" da frase e também a
        string da classe.

        Recebe a lista das frases com suas classes e passa cada frase pela função busca_caracteristicas."""
        base_completa = []
        for (frase, emocao) in base_com_stem:
            base_completa.append((ProcessaDados.busca_caracteristicas(frase, palavras_unicas), emocao))

        return base_completa
    
    @staticmethod
    def cria_base_completa(BInfo, nome_arquivo):
        baseCompleta = None

        if nome_arquivo and nome_arquivo != True:
            # Gerando a lista de tuplas com as frases do texto do arquivo de treinamento
            BInfo.base = PreProcessamento.transformar_texto(nome_arquivo)
            # Processando as frases com Stemming
            baseStem = ProcessaDados.aplica_stemming(BInfo.base)
            # Criando lista com todas as palavras para extrair a frequência das mesmas
            todasPalavras = ProcessaDados.lista_de_palavras(baseStem)
            # Criando objeto de frequência (FreqDist) do nltk
            freq = ProcessaDados.busca_frequencia(todasPalavras)
            del todasPalavras
            # Separando as palavras sem repetidos (dict_keys)
            BInfo.palavrasUnicas = ProcessaDados.lista_de_palavras_unicas(freq)
            del freq
            # Recebe a lista que será utilizada para treinar o classificador
            baseCompleta = ProcessaDados.finaliza_base_completa(baseStem, BInfo.palavrasUnicas)
        
        return baseCompleta

    @staticmethod
    def gera_classificador(base_completa):
        """Retorna um NaiveBayesClassifier da biblioteca nltk treinado com uma base de dados criados de preferência
        por finaliza_base_completa(base_com_stem, palavras_unicas)."""
        print('criando classificador')
        classificador = nltk.NaiveBayesClassifier.train(base_completa)
        print('classificador criado')
        return classificador

    @staticmethod
    def retorna_precisao(classificador, base_testes):
        """Utiliza o classificador e uma outra base de dados já classificados de preferência por finaliza_base_completa(base
        _com_stem, palavras_unicas) para que a biblioteca nltk calcule o seu grau de acerto."""
        return nltk.classify.accuracy(classificador, base_testes)
