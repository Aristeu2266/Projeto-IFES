from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
import pickle
import json
from buscainformacoes import BuscaInformacoes
from processadados import ProcessaDados
from preprocessamento import PreProcessamento
from fazrelat import FazRelat


class Janela:
    def __init__(self):
        """Monta a janela com seus widgets iniciais."""
        self.arq_treinamento = None  # self.arq_treinamento se tornará um objeto da classe BuscaInformacoes
        self.arq_teste = None  # self.arq_teste se tornará um objeto da classe BuscaInformacoes
        self.dados_treinamento = None  # self.dados_treinamento se tornará um objeto da classe BuscaInformacoes
        self.dados_teste = None  # self.dados_treinamento se tornará um objeto da classe BuscaInformacoes
        self.classificador = None  # self.classificador se tornará um objeto da classe nltk.NaiveBayesClassifier
        self.frase = None  # Receberá a frase a ser classificada pelo classificador

        self.root = Tk()
        self.frame = Frame(self.root, padx=30, pady=10)
        self.frame.pack()

        # Instancia os widgets que serão utilizados
        self.label_0 = Label(self.frame, text="")  # Label responsável por avisos
        self.label_1 = Label(self.frame, text="Arquivo de treinamento:")
        self.entry_1 = Entry(self.frame)
        self.label_2 = Label(self.frame, text="Arquivo de teste:")
        self.entry_2 = Entry(self.frame)
        self.button_1 = Button(self.frame, text="Criar classificador", command=lambda: self.cria_classificador())
        self.button_2 = Button(self.frame, text="Testar classificador", command=lambda: self.mostra_precisao())
        self.label_3 = Label(self.frame, text="Inserir texto:")
        self.entry_3 = Entry(self.frame)
        self.button_3 = Button(self.frame, text="Classificar", command=lambda: self.classifica())
        self.button_4 = Button(self.frame, text="Criar Relatório", command=lambda: self.cria_relatorio())
        self.button_5 = Button(self.frame, text='Carrega Classificador', command=lambda: self.carrega_classificador())
        self.button_6 = Button(self.frame, text='Carrega Teste', command=lambda: self.carrega_teste())

        # Posiciona os widgets iniciais
        self.label_0.pack()
        self.label_1.pack()
        self.entry_1.pack()
        self.label_2.pack()
        self.entry_2.pack()
        self.button_1.pack(pady=2)
        self.button_5.pack(pady=2)
        self.button_6.pack(pady=2)

        self.root.mainloop()

    def cria_classificador(self):
        try:  # Try/except para erros na validação no nome do arquivo de treinamento.
            self.arq_treinamento = BuscaInformacoes.valida_nome_do_arquivo(self.entry_1.get().strip())
            self.label_0["text"] = ""  # Caso tenha dado um erro anteriormente reseta a mensagem.

            self.valida_arq_teste()

            # Atribui a base de treinamento do classificador.
            self.dados_treinamento = BuscaInformacoes(self.arq_treinamento)

            # Se tudo der certo com os nomes dos arquivos, finalmente será criado o classificador
            self.classificador = ProcessaDados.gera_classificador(self.dados_treinamento.baseCompleta)

            # Usando o pickle para salvar
            salva_classificador = open('classificador.pickle', 'wb')
            pickle.dump(self.Classificador(self.classificador, list(self.dados_treinamento.palavrasUnicas)), salva_classificador)
            salva_classificador.close()

            #salva_classificador = open('classificador.json', 'w')
            #salva_classificador.write(json.dumps(self.dados_treinamento.palavrasUnicas))

            self.label_3.pack()
            self.entry_3.pack()
            self.button_3.pack(pady=2)
                
                
        except FileNotFoundError:  # Caso o arquivo não exista a validação vai dar FileNotFoundError
            self.label_0["text"] = "Arquivo de treinamento não encontrado"
            self.label_3.pack_forget()
            self.entry_3.pack_forget()
            self.button_3.pack_forget()
            self.button_4.pack_forget()
        except NameError:  # Caso o nome do arquivo de treinamento esteja em branco a validação vai dar NameError.
            # É necessário o nome do arquivo de treinamento para criar o classificador
            self.label_0["text"] = "Campo 'Arquivo de treinamento'\nnão pode ficar em branco"
            self.label_3.pack_forget()
            self.entry_3.pack_forget()
            self.button_3.pack_forget()
            self.button_4.pack_forget()
    
    def valida_arq_teste(self):
        try:  # Try/except para erros na validação no nome do arquivo de teste
            self.arq_teste = BuscaInformacoes.valida_nome_do_arquivo(self.entry_2.get().strip())
            self.label_0["text"] = ""  # Caso tenha dado um erro anteriormente reseta a mensagem

            # Remove os widgets que recebe o input a ser classificado caso eles existam para que o button_2 fique
            # debaixo do button_1, mas só se o nome do arquivo de teste for válido.
            self.label_3.pack_forget()
            self.entry_3.pack_forget()
            self.button_3.pack_forget()
            self.button_4.pack_forget()
            self.dados_teste = BuscaInformacoes(self.arq_teste) 

            self.button_2.pack(pady=2)
            self.button_4.pack(pady=2)
        except FileNotFoundError:  # Caso o arquivo não exista a validação vai dar FileNotFoundError.
            self.label_0["text"] = "Arquivo de teste não encontrado"
            self.button_2.pack_forget()
            self.arq_teste = ""
        except NameError:  # Não é obrigatória a entrada de um arquivo de teste, portanto se der NameError o nome do
            # arquivo de teste somente ficará vazio.
            self.button_2.pack_forget()
            self.arq_teste = ""

    def mostra_precisao(self):
        """Define ao label de aviso a porcentagem da precisao do classificador."""
        precisao = ProcessaDados.retorna_precisao(self.classificador, self.dados_teste.baseCompleta)
        self.label_0["text"] = "Precisao: " + str(float(int(precisao * 10000)) / 100) + "%"

    def classifica(self):
        """Define ao label de aviso a classe da frase passada utilizando o classificador criado."""
        self.frase = self.entry_3.get().strip().lower()
        self.frase = PreProcessamento.remove_caracteres(self.frase)
        self.frase = ProcessaDados.aplica_stemming_frase(self.frase)
        self.frase = ProcessaDados.busca_caracteristicas(self.frase, self.dados_treinamento.palavrasUnicas)
        self.distribuicao = self.classificador.prob_classify(self.frase)
        self.label_0["text"] = self.classificador.classify(self.frase)
        for classe in self.distribuicao.samples():
            self.label_0["text"] += "\n%s: %f %%" % (classe, self.distribuicao.prob(classe) * 100)
        #self.label_0["text"] = self.classificador.classify(self.frase)
    
    def cria_relatorio(self):
        FazRelat(self.classificador)
        FazRelat.erros(self.classificador, self.dados_teste.baseCompleta, self.dados_teste.base)
        print('Relatório criado')
    
    def carrega_classificador(self):
        self.valida_arq_teste()

        try:
            arq_classificador = open('classificador.pickle', 'rb')
            classificador_pickle = pickle.load(arq_classificador)
            arq_classificador.close()

            self.classificador = classificador_pickle.classificador
            self.dados_treinamento = BuscaInformacoes()
            self.dados_treinamento.palavrasUnicas = classificador_pickle.palavrasUnicas

            self.label_3.pack()
            self.entry_3.pack()
            self.button_3.pack(pady=2)

            self.label_0["text"] = 'Classificador carregado'

            if self.arq_teste:
                self.dados_teste = BuscaInformacoes(self.arq_teste)
                self.button_4.pack(pady=2)
        except FileNotFoundError:
            self.label_0["text"] = "Não há classificador salvo"
    
    def carrega_teste(self):
        self.valida_arq_teste()
        if self.arq_teste:
            self.button_2.pack(pady=2)
            self.label_3.pack()
            self.entry_3.pack()
            self.button_3.pack(pady=2)
    
    class Classificador():
        def __init__(self, classificador, palavrasUnicas):
            self.classificador = classificador
            self.palavrasUnicas = palavrasUnicas


# Cria uma instância de Janela para que inicie o programa
janela = Janela()
