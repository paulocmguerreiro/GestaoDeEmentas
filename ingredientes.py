import os
import curses
import curses.ascii
import curses.panel
import curses.textpad
import datetime
import time

from consts import *
from funcoes import *
from funcoes_curses import *

'''
    FORMULÁRIO : Procura e consulta de informação detalhada dos alimentos da TCA
'''
def listarIngredientes(stdscr, sairComIngrediente = False):
    stdscr.clear()
    stdscr.refresh()
    yMax, xMax = stdscr.getmaxyx()

    # Recolher a lista inicial a mostrar (Nível 1)
    listaVisualizar = pedirListaPorAtributo(listaNivel1, DES_NIVEL_1)
    visualizarPainel = 1

    # Criar Janela
    nw = curses.newwin(yMax, xMax // 2 + 1, 0, (xMax // 2))

    filtroNivel1 = -1                       # Idx na listaNivel1
    filtroNivel2 = -1                       # Idx na listaNivel2
    filtroNivel3 = -1                       # Idx na listaNivel3
    filtroIngrediente = -1                  # Idx na listaIngredientes
    selFiltroNivel1 = -1                    # Idx na listaVisualizar (listaNivel1 com filtro aplicado)
    selFiltroNivel2 = -1                    # Idx na listaVisualizar (listaNivel2 com filtro aplicado)
    selFiltroNivel3 = -1                    # Idx na listaVisualizar (listaNivel3 com filtro aplicado)
    selFiltroIngrediente = -1               # Idx na listaVisualizar (listaIngredientes com filtro aplicado)
    linhaSeleccionada = 0                   # Idx na listaVisualizar da linha selecionada (para selecionar automaticamente a linha ao recarregar a listaVisualizar)
    rodape = 'ESC = Sair'
    while True:
        nw.bkgd(curses.color_pair(10))
        nw.clear()
        nw.box()
        nw.addstr(0, 2, " FILTRO INGREDIENTES ")
        nw.attron(curses.color_pair(12))
        espacoTexto = xMax // 2 - 30
        if filtroNivel1 >= 0:
            nw.addstr(2, 2, "NÍVEL 1                 : ")
            nw.addnstr(listaNivel1[filtroNivel1].get(DES_NIVEL_1), espacoTexto, curses.color_pair(15))
        if filtroNivel2 >= 0:
            nw.addstr(3, 2, "NÍVEL 2                 : ")
            nw.addnstr(listaNivel2[filtroNivel2].get(DES_NIVEL_2), espacoTexto, curses.color_pair(15))
        if filtroNivel3 >= 0:
            nw.addstr(4, 2, "NÍVEL 3                 : ")
            nw.addnstr(listaNivel3[filtroNivel3].get(DES_NIVEL_3), espacoTexto, curses.color_pair(15))
        if filtroIngrediente >= 0:
            ingrediente = listaIngredientes[filtroIngrediente]
            nw.addstr(6, 2, "INGREDIENTE             : ")
            nw.addnstr(ingrediente.get(DES_COD) + ' > ' + ingrediente.get(DES_NOME_DO_ALIMENTO), espacoTexto, curses.color_pair(15))
            nw.addstr(8, 2, "ENERGIA  KCAL           : ")
            nw.addnstr(formatarParaFloat(ingrediente[DES_ENERGIA_KCAL_]) + ' ' + ingrediente[DES_ENERGIA_KCAL_ESCALA] + ' ' + ingrediente[DES_ENERGIA_KCAL_EDIVEL], espacoTexto, curses.color_pair(15))
            nw.addstr(9, 2, "ENERGIA  KJ             : ")
            nw.addnstr(formatarParaFloat(ingrediente[DES_ENERGIA_KJ_]) + ' ' + ingrediente[DES_ENERGIA_KJ_ESCALA] + ' ' + ingrediente[DES_ENERGIA_KJ_EDIVEL], espacoTexto, curses.color_pair(15))
            nw.addstr(10, 2, "LÍPIDOS                 : ")
            nw.addnstr(formatarParaFloat(ingrediente[DES_LIPIDOS_]) + ' ' + ingrediente[DES_LIPIDOS_ESCALA] + ' ' + ingrediente[DES_LIPIDOS_EDIVEL],espacoTexto, curses.color_pair(15))
            nw.addstr(11, 2, "ÁCIDOS GORDOS SATURADOS : ")
            nw.addnstr(formatarParaFloat(ingrediente[DES_ACIDOS_GORDOS_SATURADOS_]) + ' ' + ingrediente[DES_ACIDOS_GORDOS_SATURADOS_ESCALA] + ' ' + ingrediente[DES_ACIDOS_GORDOS_SATURADOS_EDIVEL], espacoTexto, curses.color_pair(15))
            nw.addstr(12, 2, "HIDRATOS DE CARBONO     : ")
            nw.addnstr(formatarParaFloat(ingrediente[COL_HIDRATOS_DE_CARBONO]) + ' ' + ingrediente[COL_HIDRATOS_DE_CARBONO_ESCALA] + ' ' + ingrediente[COL_HIDRATOS_DE_CARBONO_EDIVEL], espacoTexto, curses.color_pair(15))
            nw.addstr(13, 2, "PROTEINAS               : ")
            nw.addnstr(formatarParaFloat(ingrediente[COL_PROTEINA_]) + ' ' + ingrediente[COL_PROTEINA_ESCALA] + ' ' + ingrediente[COL_PROTEINA_EDIVEL], espacoTexto, curses.color_pair(15))
            nw.addstr(14, 2, "SAL                     : ")
            nw.addnstr(formatarParaFloat(ingrediente[DES_SAL_]) + ' ' + ingrediente[DES_SAL_ESCALA] + ' ' + ingrediente[DES_SAL_EDIVEL], espacoTexto, curses.color_pair(15))
            nw.addstr(15, 2, "AÇUCAR                  : ")
            nw.addnstr(formatarParaFloat(ingrediente[DES_MONO_DISSACARIDOS_ACUCARES_]) + ' ' + ingrediente[DES_MONO_DISSACARIDOS_ACUCARES_ESCALA] + ' ' + ingrediente[DES_MONO_DISSACARIDOS_ACUCARES_EDIVEL], espacoTexto, curses.color_pair(15))

        nw.refresh()
        mensagemRodape = rodape + ' / ENTER = Escolher'
        teclasSaida = []
        # Posso escolher um ingrediente (return)?
        if sairComIngrediente and visualizarPainel == 4:
            mensagemRodape += ' / F2 - Utilizar Ingrediente'
            teclasSaida = [curses.KEY_F2]
        idxPos, opcao, teclaSaida = inputLista(stdscr, listaVisualizar, 'Filtrar', mensagemRodape, 0, 0, yMax, xMax // 2, linhaSeleccionada, teclasSaida)

        # Acção de escolher um Ingrediente
        if sairComIngrediente and teclaSaida == curses.KEY_F2:
            return saberIndexPorChave(listaIngredientes, DES_NOME_DO_ALIMENTO, opcao)

        # PAINEL - Filtro Nível 1
        if visualizarPainel == 1:
            if opcao != '':
                posIndex = saberIndexPorChave(listaNivel1, DES_NIVEL_1, opcao)
                filtroNivel1 = posIndex
                selFiltroNivel1 = idxPos
                listaVisualizar = pedirListaPorAtributoChave(listaNivel2, DES_NIVEL_2, DES_SUPERIOR, posIndex)
                visualizarPainel = 2
                filtroNivel2 = -1
                linhaSeleccionada = 0
                rodape = 'ESC = Voltar Nível 1'
                continue
            else:
                return None

        # PAINEL - Filtro Nível 2
        if visualizarPainel == 2:
            if opcao != '':
                posIndex = saberIndexPorChave(listaNivel2, DES_NIVEL_2, opcao)
                filtroNivel2 = posIndex
                selFiltroNivel2 = idxPos
                listaVisualizar = pedirListaPorAtributoChave(listaNivel3, DES_NIVEL_3, DES_SUPERIOR, posIndex)
                visualizarPainel = 3
                filtroNivel3 = -1
                linhaSeleccionada = 0
                rodape = 'ESC = Voltar Nível 2'
                continue
            else:
                visualizarPainel = 1
                filtroNivel2 = -1
                listaVisualizar = pedirListaPorAtributo(listaNivel1, DES_NIVEL_1)
                linhaSeleccionada = selFiltroNivel1
                rodape = 'ESC = Sair'
                continue

        # PAINEL - Filtro Nível 3
        if visualizarPainel == 3:
            if opcao != '':
                posIndex = saberIndexPorChave(listaNivel3, DES_NIVEL_3, opcao)
                filtroNivel3 = posIndex
                selFiltroNivel3 = idxPos
                listaVisualizar = pedirListaPorAtributoChave(listaIngredientes, DES_NOME_DO_ALIMENTO, DES_NIVEL_3, posIndex)
                visualizarPainel = 4
                filtroIngrediente = -1
                linhaSeleccionada = 0
                rodape = 'ESC - Voltar Nível 3'
                continue
            else:
                visualizarPainel = 2
                filtroNivel3 = -1
                listaVisualizar = pedirListaPorAtributoChave(listaNivel2, DES_NIVEL_2, DES_SUPERIOR, filtroNivel1)
                linhaSeleccionada = selFiltroNivel2
                rodape = 'ESC = Voltar Nível 1'
                continue


        # PAINEL - Filtro Ingrediente
        if visualizarPainel == 4:
            if opcao != '':
                posIndex = saberIndexPorChave(listaIngredientes, DES_NOME_DO_ALIMENTO, opcao)
                filtroIngrediente = posIndex
                selFiltroIngrediente = idxPos
                linhaSeleccionada = selFiltroIngrediente
                rodape = 'ESC = Voltar Nível 3'
                continue
            else:
                visualizarPainel = 3
                filtroIngrediente = -1
                listaVisualizar = pedirListaPorAtributoChave(listaNivel3, DES_NIVEL_3, DES_SUPERIOR, filtroNivel2)
                linhaSeleccionada = selFiltroNivel3
                rodape = 'ESC = Voltar Nível 2'
                continue


'''
    Carregar a informação dos ingredientes a partir do ficheiro da INSA
'''
def carregarInformacaoFicheiroIngredientes(listaNivel1, listaNivel2, listaNivel3, listaIngredientes):    
    if os.path.isfile(FICHEIRO_INSA_TCA):
        try:
            handlerFicheiro = open(FICHEIRO_INSA_TCA, 'r', encoding='utf-8')
            for linhaIngrediente in handlerFicheiro:
                ingredienteDetalhado = linhaIngrediente.replace('\n', '').replace(',','.').replace('""','"').split(';')
                # Teste simples à estrutura do ficheiro
                if (len(ingredienteDetalhado) == 125):
                    # MEMORIZAR NÍVEIS (SEM OS DUPLICAR)
                    tratarNivel1 = ingredienteDetalhado[COL_NIVEL_1]
                    tratarNivel2 = ingredienteDetalhado[COL_NIVEL_2]
                    tratarNivel3 = ingredienteDetalhado[COL_NIVEL_3]
                    # Alguns alimentos não tinham todos os níveis preenchidos
                    if not tratarNivel1:
                        tratarNivel1 = 'Diversos'
                    if not tratarNivel2:
                        tratarNivel2 = tratarNivel1 + ' > Diversos'
                    if not tratarNivel3:
                        tratarNivel3 = tratarNivel2 + ' > Diversos'

                    posNivel1 = saberIndexPorChave(listaNivel1, DES_NIVEL_1, tratarNivel1)
                    posNivel2 = saberIndexPorChave(listaNivel2, DES_NIVEL_2, tratarNivel2)
                    posNivel3 = saberIndexPorChave(listaNivel3, DES_NIVEL_3, tratarNivel3)
                    if posNivel1 == -1:
                        tempDict = dict()
                        tempDict[DES_INDEX] = len(listaNivel1)
                        tempDict[DES_NIVEL_1] = tratarNivel1
                        listaNivel1.append(tempDict)
                        posNivel1 = tempDict[DES_INDEX]
                    if posNivel2 == -1:
                        tempDict = dict()
                        tempDict[DES_INDEX] = len(listaNivel2)
                        tempDict[DES_NIVEL_2] = tratarNivel2
                        tempDict[DES_SUPERIOR] = posNivel1
                        listaNivel2.append(tempDict)
                        posNivel2 = tempDict[DES_INDEX]
                    if posNivel3 == -1:
                        tempDict = dict()
                        tempDict[DES_INDEX] = len(listaNivel3)
                        tempDict[DES_NIVEL_3] = tratarNivel3
                        tempDict[DES_SUPERIOR] = posNivel2
                        listaNivel3.append(tempDict)
                        posNivel3 = tempDict[DES_INDEX]

                    # Ingrediente
                    tempDict = dict()
                    tempDict[DES_COD] = ingredienteDetalhado[COL_COD]
                    tempDict[DES_NOME_DO_ALIMENTO] = ingredienteDetalhado[COL_NOME_DO_ALIMENTO]
                    tempDict[DES_NIVEL_1] = posNivel1
                    tempDict[DES_NIVEL_2] = posNivel2
                    tempDict[DES_NIVEL_3] = posNivel3

                    tempDict[DES_ENERGIA_KCAL_] = float(ingredienteDetalhado[COL_ENERGIA_KCAL_])
                    tempDict[DES_ENERGIA_KCAL_ESCALA] = ingredienteDetalhado[COL_ENERGIA_KCAL_ESCALA]
                    tempDict[DES_ENERGIA_KCAL_EDIVEL] = ingredienteDetalhado[COL_ENERGIA_KCAL_EDIVEL]
                    
                    tempDict[DES_ENERGIA_KJ_] = float(ingredienteDetalhado[COL_ENERGIA_KJ_])
                    tempDict[DES_ENERGIA_KJ_ESCALA] = ingredienteDetalhado[COL_ENERGIA_KJ_ESCALA]
                    tempDict[DES_ENERGIA_KJ_EDIVEL] = ingredienteDetalhado[COL_ENERGIA_KJ_EDIVEL]

                    tempDict[DES_LIPIDOS_] = float(ingredienteDetalhado[COL_LIPIDOS_])
                    tempDict[DES_LIPIDOS_ESCALA] = ingredienteDetalhado[COL_LIPIDOS_ESCALA]
                    tempDict[DES_LIPIDOS_EDIVEL] = ingredienteDetalhado[COL_LIPIDOS_EDIVEL]

                    tempDict[DES_ACIDOS_GORDOS_SATURADOS_] = float(ingredienteDetalhado[COL_ACIDOS_GORDOS_SATURADOS_])
                    tempDict[DES_ACIDOS_GORDOS_SATURADOS_ESCALA] = ingredienteDetalhado[COL_ACIDOS_GORDOS_SATURADOS_ESCALA]
                    tempDict[DES_ACIDOS_GORDOS_SATURADOS_EDIVEL] = ingredienteDetalhado[COL_ACIDOS_GORDOS_SATURADOS_EDIVEL]

                    tempDict[COL_HIDRATOS_DE_CARBONO] = float(ingredienteDetalhado[COL_HIDRATOS_DE_CARBONO])
                    tempDict[COL_HIDRATOS_DE_CARBONO_ESCALA] = ingredienteDetalhado[COL_HIDRATOS_DE_CARBONO_ESCALA]
                    tempDict[COL_HIDRATOS_DE_CARBONO_EDIVEL] = ingredienteDetalhado[COL_HIDRATOS_DE_CARBONO_EDIVEL]

                    tempDict[COL_PROTEINA_] = float(ingredienteDetalhado[COL_PROTEINA_])
                    tempDict[COL_PROTEINA_ESCALA] = ingredienteDetalhado[COL_PROTEINA_ESCALA]
                    tempDict[COL_PROTEINA_EDIVEL] = ingredienteDetalhado[COL_PROTEINA_EDIVEL]

                    tempDict[DES_SAL_] = float(ingredienteDetalhado[COL_SAL_])
                    tempDict[DES_SAL_ESCALA] = ingredienteDetalhado[COL_SAL_ESCALA]
                    tempDict[DES_SAL_EDIVEL] = ingredienteDetalhado[COL_SAL_EDIVEL]

                    tempDict[DES_MONO_DISSACARIDOS_ACUCARES_] = float(ingredienteDetalhado[COL_MONO_DISSACARIDOS_ACUCARES_])
                    tempDict[DES_MONO_DISSACARIDOS_ACUCARES_ESCALA] = ingredienteDetalhado[COL_MONO_DISSACARIDOS_ACUCARES_ESCALA]
                    tempDict[DES_MONO_DISSACARIDOS_ACUCARES_EDIVEL] = ingredienteDetalhado[COL_MONO_DISSACARIDOS_ACUCARES_EDIVEL]

                    listaIngredientes.append(tempDict)
                else:
                    print(f'A estrutura do ficheiro "{FICHEIRO_INSA_TCA}" está incorreta.')
                    print(f'Deve descarregar novamente o ficheiro e convertê-lo para CSV.')
                    break
            handlerFicheiro.close()
        except:
            print(f'O ficheiro "{FICHEIRO_INSA_TCA}" existe mas não foi possível ler o seu conteúdo.' )
            return False
    return True



