from consts import *
import os
import datetime
import time

'''
    Auxiliar para formatar um valor para visualizar
'''
def formatarParaFloat(valor, dimensao=7, casasDecimais=2):
    return ("{:>" + str(dimensao) + "." + str(casasDecimais) + "f}").format(float(valor))

'''
    Procura a posição do Index
'''
def saberIndex(lista, agulha):

    for indice in range(len(lista)):
        if lista[indice] == agulha:
            return indice
    return -1

'''
    Procura a posição do Index através de uma CHAVE
'''
def saberIndexPorChave(lista, chave, agulha):

    for indice in range(len(lista)):
        if lista[indice].get(chave) == agulha:
            return indice
    return -1

'''
   Retornar uma lista através de uma CHAVE
'''
def pedirListaPorChave(lista, chave, agulha):
    retornar = []
    for item in lista:
        if item.get(chave) == agulha:
            retornar.append(item)
    return retornar

'''
   Retornar uma lista que contenha uma substring através de uma CHAVE
'''
def pedirListaPorChaveSubString(lista, chave, agulha):
    retornar = []
    for item in lista:
        if agulha.upper() in item.get(chave).upper():
            retornar.append(item)
    return retornar

'''
   Retornar uma lista somente com um dos atributos
'''
def pedirListaPorAtributo(lista, atributo):
    retornar = list()
    for item in lista:
        retornar.append(item.get(atributo))
    return retornar

'''
    Retorna uma lista de um atributo tendo em conta uma chave
'''
def pedirListaPorAtributoChave(lista, atributo, chave, agulha):
    temp = pedirListaPorChave(lista, chave, agulha)
    return pedirListaPorAtributo(temp, atributo)

'''
    Criar um Ficheiro Vazio caso não exista
'''
def prepararFicheiro(ficheiro, conteudoFicheiroVazio = []):
    if not os.path.isfile(ficheiro):
        try:
            handlerFicheiro = open(ficheiro, 'w', encoding='utf-8')
            for adicionarLinha in conteudoFicheiroVazio:
                handlerFicheiro.writelines(adicionarLinha + '\n')
            handlerFicheiro.close()
        except:
            print(f'Não foi possível criar e guardar informação no ficheiro "{ficheiro}".' )
            return False
    return True
