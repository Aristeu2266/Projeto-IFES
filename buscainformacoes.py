from processadados import ProcessaDados


class BuscaInformacoes:
    """O objeto do tipo BuscaInformacoes serve para carregar como atributo os dados processados pelos métodos
    da classe ProcessaDados. Ele recebe os nomes dos arquivos de treinamento e de teste sendo o de teste opcional."""
    def __init__(self, nome_arquivo=None):
        self.base = None
        self.palavrasUnicas = None
        # Passar o valor True para arquivo_de_teste ocorreria um erro pois não é um nome de arquivo
        if nome_arquivo and nome_arquivo != True:
            nome_arquivo = self.valida_nome_do_arquivo(nome_arquivo)
            self.baseCompleta = ProcessaDados.cria_base_completa(self, nome_arquivo)
        

    @staticmethod
    def valida_nome_do_arquivo(nome_do_arquivo):
        """Retorna o nome do arquivo com .txt ao final

        Vai dar um erro (FileNotFoundError) caso o arquivo .txt não exista.
        Vai dar um erro (IndexError) caso receba uma string vazia."""
        if not nome_do_arquivo:
            raise NameError("Campo vazio")

        if nome_do_arquivo[-4:] != '.txt':
            nome_do_arquivo += '.txt'

        f = open(nome_do_arquivo)
        f.close()

        return nome_do_arquivo
