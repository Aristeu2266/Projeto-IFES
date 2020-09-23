import json

arq = open('reviews.json', encoding='utf-8')


linha = arq.readline().strip()
contador = 1
listaDeJsons = []

while linha:

    try:
        review = json.loads(linha[:-1] if linha[-1] == ',' else linha)
        if review['idreview']:
            listaDeJsons.append(review)
        else:
            print('linha', contador, 'não foi adicionada')
    except AttributeError:
        print('Erro de conversão na linha ', end='')
    except:
        print('Erro na linha ', end='')

    print(contador)
    contador += 1

    linha = arq.readline().strip()


print('\nIniciando escrita')
arqPos = open('positivas.txt', 'w', encoding='utf-8')
arqNeg = open('negativas.txt', 'w', encoding='utf-8')
arqPos.close()
arqNeg.close()
arqPos = open('positivas.txt', 'a', encoding='utf-8')
arqNeg = open('negativas.txt', 'a', encoding='utf-8')

contador = 1
for review in listaDeJsons:
    print(contador)
    contador += 1
    if review['rate'] == '5':
        arqPos.write(review['content'] + ' #label#:5\n')
    elif review['rate'] == '1':
        arqNeg.write(review['content'] + ' #label#:1\n')
    else:
        print(review)


arq.close()
arqPos.close()
arqNeg.close()
