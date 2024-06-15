import os
import curses
import curses.ascii
import curses.panel
import curses.textpad
import datetime
import time
import webbrowser

from consts import *
from funcoes import *
from funcoes_curses import *
from ingredientes import listarIngredientes

'''
    FORMULÁRIO : Gestão da composição das refeições
'''
def formEditarRefeicao(stdscr, tipoRefeicaoTitulo, refeicaoTituloAEditar):
    processarInput = 1
    refeicaoIngredientes = []
    refeicaoTitulo = refeicaoTituloAEditar
    refeicaoModoPreparacao = []
    # Carregar os Dados da Refeição ou Nova Refeição!?
    if len(refeicaoTitulo) > 0:
        if carregarRefeicao(refeicaoIngredientes, tipoRefeicaoTitulo, refeicaoTitulo, refeicaoModoPreparacao):
            janelaTitulo = f'Atualizar refeição - {tipoRefeicaoTitulo}'
            processarInput = 2
        else:
            dialogInformacao(stdscr, 'Não foi possível carregar a informação da refeição.', dialogColorPair = 13)
            return
    else:
        janelaTitulo = f'Nova refeição - {tipoRefeicaoTitulo}'

    # Preparar a Janela
    stdscr.clear()
    stdscr.refresh()
    yMax, xMax = stdscr.getmaxyx()
    # Desenhar Janela
    nw = curses.newwin(yMax, xMax)

    gridLinhaSelecionada = 0
    nw.clear()
    while True:
        nw.clear()
        nw.bkgd(curses.color_pair(10))
        nw.box()
        nw.attron(curses.color_pair(10))
        nw.addstr(0, 2, '< ' + janelaTitulo + ' >')
        nw.attron( curses.color_pair(12))
        nw.addstr(2,2, 'Título da Refeição : ')
        nw.addstr(refeicaoTitulo, curses.color_pair(15))
        nw.refresh()
        # Painel : Solicitar o Título da Refeição (tecla TAB ou no caso em que estou a criar uma receita nova)
        if processarInput == 1:
            valor = inputDialog(stdscr, 'Título da Refeição', 50)
            if valor == '':
                dialogInformacao(stdscr, 'Deve introduzir um título para a refeição.', dialogColorPair = 13)
            else:
                refeicaoTitulo = valor.replace(';', ',')
                processarInput = 2
                gridLinhaSelecionada = 0
            processarInput = 2
            continue

        # Painel : Lista de Ingredientes
        if processarInput == 2:
            gridLinhaSelecionada, gridOpcao, gridTeclaSaida = inputGrid(stdscr, refeicaoIngredientes, 'Composição da Refeição', 'ESC = Sair / + = Adicionar / - = Remover / TAB = Título / ENTER = Quantidade / F2 = Guardar / F4 - Imprimir / F5 - Procurar Ingrediente / F6 - Preparação', GRID_INGREDIENTES_COLS, GRID_INGREDIENTES_DIMS, GRID_INGREDIENTES_ALIGN, 5,1, yMax - 6, xMax - 2, gridLinhaSelecionada, [ord('+'), ord('-'), curses.ascii.TAB, curses.KEY_F2, curses.KEY_F4, curses.KEY_F5, curses.KEY_F6] )

            # Sair sem guardar
            if gridTeclaSaida == curses.ascii.ESC:
                if dialogConfirmacao(stdscr, 'Pretende sair sem guardar?', dialogColorPair = 13):
                    break
                continue

            # Indicar o modo de preparação da receita
            if gridTeclaSaida == curses.KEY_F6:
            #if gridTeclaSaida == curses.ascii.TAB:
                refeicaoModoPreparacao = inputText(stdscr, 'Modo de Preparação', 60, 20, refeicaoModoPreparacao)
                continue

            # Alterar o input
            if gridTeclaSaida == curses.ascii.TAB:
                processarInput = 1
                continue


            # Adicionar um ingrediente
            if gridTeclaSaida == ord('+'):
                ingreSele = listarIngredientes(stdscr, True)
                if ingreSele:
                    ingreUtilizar = listaIngredientes[ingreSele]
                    refeicaoIngredientes.append([
                        ingreUtilizar[DES_COD], 
                        ingreUtilizar[DES_NOME_DO_ALIMENTO], 
                        formatarParaFloat(100), 
                        formatarParaFloat(ingreUtilizar[DES_ENERGIA_KCAL_]), 
                        formatarParaFloat(ingreUtilizar[DES_ENERGIA_KJ_]), 
                        formatarParaFloat(ingreUtilizar[DES_LIPIDOS_]), 
                        formatarParaFloat(ingreUtilizar[DES_ACIDOS_GORDOS_SATURADOS_]), 
                        formatarParaFloat(ingreUtilizar[COL_HIDRATOS_DE_CARBONO]), 
                        formatarParaFloat(ingreUtilizar[COL_PROTEINA_]), 
                        formatarParaFloat(ingreUtilizar[DES_SAL_]), 
                        formatarParaFloat(ingreUtilizar[DES_MONO_DISSACARIDOS_ACUCARES_]), 
                        ])
                    gridLinhaSelecionada = len(refeicaoIngredientes)-1
                nw.clear()
                continue

            # Remover um ingredientes
            if gridTeclaSaida == ord('-'):
                if 0 <= gridLinhaSelecionada and gridLinhaSelecionada < len(refeicaoIngredientes):
                    if dialogConfirmacao(stdscr, 'Pretende remover o ingrediente?', dialogColorPair = 13):
                        del refeicaoIngredientes[gridLinhaSelecionada]
                continue

            # Guardar a refeição
            if gridTeclaSaida == curses.KEY_F2:
                if dialogConfirmacao(stdscr, 'Pretende guardar a refeição?'):
                    if removerRefeicao(tipoRefeicaoTitulo, refeicaoTituloAEditar):
                        if guardarRefeicao(tipoRefeicaoTitulo, refeicaoTitulo, refeicaoIngredientes, refeicaoModoPreparacao):
                            return
                    dialogInformacao(stdscr, "Não foi possível guardar a refeição.", dialogColorPair = 13)
                continue

            # Imprimir a Ficha Técnica
            if gridTeclaSaida == curses.KEY_F4:
                imprimirFichaTecnica(stdscr, tipoRefeicaoTitulo, refeicaoTitulo, refeicaoIngredientes, refeicaoModoPreparacao )
                continue

            # Procurar um artigo pela descrição
            if gridTeclaSaida == curses.KEY_F5:
                procurar = inputDialog(stdscr, 'Ingrediente?', 50 )
                if procurar != '':
                    lista = pedirListaPorChaveSubString(listaIngredientes, DES_NOME_DO_ALIMENTO, procurar)
                    lista = pedirListaPorAtributo(lista, DES_NOME_DO_ALIMENTO)
                    if len(lista) > 0:
                        posicaoSeleccionada = 0
                        filtroIngIdx, filtroIng, teclaSaidaIng = inputLista(stdscr, lista, 'Ingredientes', '[ESC - Sair / ENTER - Escolher]', 2, xMax // 4, yMax - 4, xMax // 2, posicaoSeleccionada)
                        if filtroIng != '':
                            posIndexIng = saberIndexPorChave(listaIngredientes, DES_NOME_DO_ALIMENTO, filtroIng)
                            if posIndexIng != -1:
                                ingreUtilizar = listaIngredientes[posIndexIng]
                                refeicaoIngredientes.append([
                                    ingreUtilizar[DES_COD], 
                                    ingreUtilizar[DES_NOME_DO_ALIMENTO], 
                                    formatarParaFloat(100), 
                                    formatarParaFloat(ingreUtilizar[DES_ENERGIA_KCAL_]), 
                                    formatarParaFloat(ingreUtilizar[DES_ENERGIA_KJ_]), 
                                    formatarParaFloat(ingreUtilizar[DES_LIPIDOS_]), 
                                    formatarParaFloat(ingreUtilizar[DES_ACIDOS_GORDOS_SATURADOS_]), 
                                    formatarParaFloat(ingreUtilizar[COL_HIDRATOS_DE_CARBONO]), 
                                    formatarParaFloat(ingreUtilizar[COL_PROTEINA_]), 
                                    formatarParaFloat(ingreUtilizar[DES_SAL_]), 
                                    formatarParaFloat(ingreUtilizar[DES_MONO_DISSACARIDOS_ACUCARES_]), 
                                    ])
                                gridLinhaSelecionada = len(refeicaoIngredientes)-1
                    else:
                        dialogInformacao(stdscr, 'Não foram encontrador ingredientes.', dialogColorPair = 13)
                continue


            # Alterar a quantidade
            if gridOpcao != '':
                quantidade = inputDialog(stdscr, 'Qual a quantidade a utilizar?', 7 )
                try:
                    quantidade = float(quantidade)
                except:
                    quantidade = float(refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_QTD])
                    dialogInformacao(stdscr, 'Deve introduzir um valor numérico para representar a quantidade do ingrediente.', dialogColorPair = 13)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_QTD] = formatarParaFloat(quantidade)
                # Recalcular valores calóricos
                ingrediente = listaIngredientes[saberIndexPorChave(listaIngredientes, DES_COD, refeicaoIngredientes[gridLinhaSelecionada][0])]
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_ENERGIA_KCAL] = formatarParaFloat(ingrediente[DES_ENERGIA_KCAL_] * quantidade / 100.0)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_ENERGIA_KJ] = formatarParaFloat(ingrediente[DES_ENERGIA_KJ_] * quantidade / 100.0)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_LIPIDOS] = formatarParaFloat(ingrediente[DES_LIPIDOS_] * quantidade / 100.0)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_ACS] = formatarParaFloat(ingrediente[DES_ACIDOS_GORDOS_SATURADOS_] * quantidade / 100.0)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_HC] = formatarParaFloat(ingrediente[COL_HIDRATOS_DE_CARBONO] * quantidade / 100.0)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_PROTEINA] = formatarParaFloat(ingrediente[COL_PROTEINA_] * quantidade / 100.0)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_SAL] = formatarParaFloat(ingrediente[DES_SAL_] * quantidade / 100.0)
                refeicaoIngredientes[gridLinhaSelecionada][COL_REF_ING_ACUCAR] = formatarParaFloat(ingrediente[DES_MONO_DISSACARIDOS_ACUCARES_] * quantidade / 100.0)
                continue

'''
    FORMULÀRIO : Pesquisa e seleção dos tipos de refeição e refeições
'''
def listarTiposDeRefeicoes(stdscr):
    stdscr.clear()
    stdscr.refresh()
    yMax, xMax = stdscr.getmaxyx()

    visualizarPainel = 1
    filtroTipoRefeicaoIdx = 0
    filtroTipoRefeicao = ''
    filtroRefeicaoIdx = 0
    filtroRefeicao = ''
    listaRefeicoes = []
    
    while True:
        # Painel Tipos de Refeição
        if visualizarPainel == 1:
            stdscr.clear()
            stdscr.refresh()
            filtroTipoRefeicaoIdx, filtroTipoRefeicao, teclaSaidaTipoRefeicao = inputLista(stdscr, listaTiposDeRefeicao, 'Tipos de Refeição', 'ESC = Sair / ENTER = Escolher', 0, 0, yMax, xMax // 2, filtroTipoRefeicaoIdx)
            if filtroTipoRefeicao != '':
                listaRefeicoes = []
                if carregarInformacaoFicheiroRefeicoesPorTipo(listaRefeicoes, filtroTipoRefeicao):
                    visualizarPainel = 2
                else:
                    dialogInformacao(stdscr, 'Não foi possível carregar as refeições.', dialogColorPair = 13)
                continue
            else:
                break

        # Painel Refeições
        if visualizarPainel == 2:
            listaRefeicoes = []
            carregarInformacaoFicheiroRefeicoesPorTipo(listaRefeicoes, filtroTipoRefeicao)
            inputLista(stdscr, listaTiposDeRefeicao, 'Tipos de Refeição', 'ESC = Sair / ENTER = Escolher', 0, 0, yMax, xMax // 2, filtroTipoRefeicaoIdx, editar = False)
            filtroRefeicaoIdx, filtroRefeicao, teclaSaidaRefeicao = inputLista(stdscr, listaRefeicoes, 'Refeições do tipo ' + filtroTipoRefeicao, 'ESC = Voltar / ENTER = Escolher / + = Adicionar / - = Remover', 0, xMax // 2, yMax, xMax // 2, filtroRefeicaoIdx, [ord('+'), ord('-')] )
            # Adicionar refeição
            if teclaSaidaRefeicao == ord('+'):
                formEditarRefeicao(stdscr, filtroTipoRefeicao, '')
                continue
            # Remover refeição
            if teclaSaidaRefeicao == ord('-') and filtroRefeicao != '':
                if dialogConfirmacao(stdscr, 'Pretende apagar a refeição?', dialogColorPair = 13):
                    if not removerRefeicao(filtroTipoRefeicao, filtroRefeicao):
                        dialogInformacao(stdscr, 'Não foi possível remover a refeição.', dialogColorPair = 13)
                continue

            # Editar Refeição
            if filtroRefeicao != '':
                formEditarRefeicao(stdscr, filtroTipoRefeicao, filtroRefeicao)
                continue
            else:
                visualizarPainel = 1
                continue

'''
    Carregar a informação de uma Refeição
'''
def carregarRefeicao(refeicaoIngredientes, tipoRefeicao, tituloRefeicao, modoPreparacao):    
    ficheiroRefeicoes = FICHEIRO_REFEICOES + tipoRefeicao + '.dat'
    if not prepararFicheiro(ficheiroRefeicoes):
        return False

    try:
        handlerFicheiro = open(ficheiroRefeicoes, 'r', encoding='utf-8')
        bProcessarRefeicao = False
        for linhaRefeicao in handlerFicheiro:
            linhaTratar = linhaRefeicao.replace('\n', '').split(';')
            # Em que refeição estou posicionado
            if len(linhaTratar) == 1:
                if linhaTratar[0] == tituloRefeicao:
                    bProcessarRefeicao = True
                else:
                    bProcessarRefeicao = False
            # Estou a tratar a refeição pretendida
            if (len(linhaTratar) == 11 and bProcessarRefeicao):
                refeicaoIngredientes.append(linhaTratar)
            # Estou a tratar do Modo de Preparacao
            if (len(linhaTratar) == 2 and bProcessarRefeicao):
                modoPreparacao.append(linhaTratar[1])
        handlerFicheiro.close()
    except:
        print(f'O ficheiro "{ficheiroRefeicoes}" existe mas não foi possível ler o seu conteúdo.' )
        return False

    return True

'''
    Calcular o total das calorias de uma refeição
'''
def totalCaloriasRefeicao(refeicaoIngredientes):
    total = 0
    for ingrediente in refeicaoIngredientes:
        total += float(ingrediente[COL_REF_ING_ENERGIA_KCAL])
    return total

'''
    Carregar a informação dos títulos das refeições de um determinado tipo
'''
def carregarInformacaoFicheiroRefeicoesPorTipo(listaRefeicoes, tipoRefeicao):    
    ficheiroRefeicoes = FICHEIRO_REFEICOES + tipoRefeicao + '.dat'
    if not prepararFicheiro(ficheiroRefeicoes):
        return False

    try:
        handlerFicheiro = open(ficheiroRefeicoes, 'r', encoding='utf-8')
        for linhaRefeicao in handlerFicheiro:
            linhaTratar = linhaRefeicao.replace('\n', '').split(';')
            if len(linhaTratar) == 1:
                listaRefeicoes.append(linhaTratar[0])
        handlerFicheiro.close()
    except:
        print(f'O ficheiro "{ficheiroRefeicoes}" existe mas não foi possível ler o seu conteúdo.' )
        return False

    return True


'''
    Carregar a informação dos ingredientes a partir do ficheiro da INSA
'''
def carregarInformacaoFicheiroTiposDeRefeicao(listaTiposDeRefeicao):    
    if not prepararFicheiro(FICHEIRO_TIPOS_REFEICAO, ['Sopa', 'Prato', 'Salada', 'Sobremesa']):
        return False

    try:
        handlerFicheiro = open(FICHEIRO_TIPOS_REFEICAO, 'r', encoding='utf-8')
        for linhaTipoRefeicao in handlerFicheiro:
            if not linhaTipoRefeicao.replace('\n', '') in listaTiposDeRefeicao: 
                listaTiposDeRefeicao.append(linhaTipoRefeicao.replace('\n', ''))
        handlerFicheiro.close()
    except:
        print(f'O ficheiro "{FICHEIRO_TIPOS_REFEICAO}" existe mas não foi possível ler o seu conteúdo.' )
        return False

    return True

'''
    Remover uma refeição
'''
def removerRefeicao(tipoRefeicao, refeicaoTitulo):    
    ficheiroRefeicoes = FICHEIRO_REFEICOES + tipoRefeicao + '.dat'
    if not prepararFicheiro(ficheiroRefeicoes):
        return False

    try:
        handlerFicheiro = open(ficheiroRefeicoes, 'r', encoding='utf-8')
        bProcessarRefeicao = False
        guardarFicheiro = []
        for linhaRefeicao in handlerFicheiro:
            linhaTratar = linhaRefeicao.replace('\n', '').split(';')
            # Em que refeição estou posicionado
            if len(linhaTratar) == 1:
                if linhaTratar[0] == refeicaoTitulo:
                    bProcessarRefeicao = True
                else:
                    bProcessarRefeicao = False
                    guardarFicheiro.append(linhaRefeicao)
            # Estou a tratar a refeição pretendida
            if (len(linhaTratar) == 11 and not bProcessarRefeicao):
                guardarFicheiro.append(linhaRefeicao)
            # Estou a tratar a refeição pretendida
            if (len(linhaTratar) == 2 and not bProcessarRefeicao):
                guardarFicheiro.append(linhaRefeicao)
        handlerFicheiro.close()

    except:
        print(f'O ficheiro "{ficheiroRefeicoes}" existe mas não foi possível ler o seu conteúdo.' )
        return False

    # Guardar o novo Ficheiro com as Refeições
    try:
        handlerFicheiro = open(ficheiroRefeicoes, 'w', encoding='utf-8')
        handlerFicheiro.writelines(guardarFicheiro)
        handlerFicheiro.close()
    except:
        print(f'Não foi possível criar e guardar informação no ficheiro "{ficheiroRefeicoes}".' )
        return False


    return True

    '''
    Remover uma refeição
'''
def guardarRefeicao(tipoRefeicao, refeicaoTitulo, refeicaoIngredientes, refeicaoModoPreparacao):    
    ficheiroRefeicoes = FICHEIRO_REFEICOES + tipoRefeicao + '.dat'

    if not prepararFicheiro(ficheiroRefeicoes):
        return False

    # Adicionar a nova Refeições
    try:
        handlerFicheiro = open(ficheiroRefeicoes, 'a+', encoding='utf-8')
        handlerFicheiro.write(refeicaoTitulo + '\n')
        for ing in refeicaoIngredientes:
            handlerFicheiro.writelines(';'.join(ing) + '\n')
        for ing in refeicaoModoPreparacao:
            handlerFicheiro.write(';' + ing.replace(';', '') + '\n')
        handlerFicheiro.close()
    except:
        print(f'Não foi possível criar e guardar informação no ficheiro "{ficheiroRefeicoes}".' )
        return False

    return True

# FILTRO : MAPA DE REFEICOES
def escolherRefeicaoPorTipo(stdscr, tipoRefeicao, refeicao = ''):
    yMax, xMax = stdscr.getmaxyx()

    rebordoX = xMax // 4
    rebordoY = yMax // 4

    listaRefeicoes = []
    if not carregarInformacaoFicheiroRefeicoesPorTipo(listaRefeicoes, tipoRefeicao):
        dialogInformacao(stdscr, 'Não foi possível carregar a informação das ementas.', dialogColorPair = 13)
        return ''
    posicaoSeleccionada = 0
    if len(refeicao) > 0:
        posicaoSeleccionada = saberIndex(listaRefeicoes, refeicao)
    filtroRefeicaoIdx, filtroRefeicao, teclaSaidaRefeicao = inputLista(stdscr, listaRefeicoes, 'Refeições : ' + tipoRefeicao, 'ESC = Sair / ENTER = Escolher', rebordoY // 2, rebordoX // 2, rebordoY*3, rebordoX*3, posicaoSeleccionada)

    return filtroRefeicao

'''
    Imprimir a ementa do Dia
'''
def imprimirFichaTecnica(stdscr, refeicaoTipoRefeicao, refeicaoTitulo, refeicaoIngredientes, refeicaoModoPreparacao):
    ficheiroFichaTecnica = f'{FICHEIRO_FICHA_TECNICA_OUTPUT}{refeicaoTipoRefeicao}_{refeicaoTitulo}.html'
    try:
        handlerFicheiro = open(FICHEIRO_HTML_FICHA_TECNICA, 'r', encoding='utf-8')
        conteudoFicheiro = handlerFicheiro.read()
        handlerFicheiro.close()

        conteudoFicheiro = conteudoFicheiro.replace("%TIPOREFEICAO%", refeicaoTipoRefeicao )
        conteudoFicheiro = conteudoFicheiro.replace("%REFEICAO%", refeicaoTitulo )

        linhaGuardar = ""
        totalQtd = 0
        totalKCal = 0
        totalKJ = 0
        totalLIP = 0
        totalACS = 0
        totalHC = 0
        totalPROT = 0
        totalSAL = 0
        totalACUCAR = 0
        for ingreUtilizar in refeicaoIngredientes:
            linhaGuardar += "<tr>\n"
            linhaGuardar += f"<td>{ingreUtilizar[COL_REF_ING_COD]}-{ingreUtilizar[COL_REF_ING_NOME]} </td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_QTD])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_ENERGIA_KCAL])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_ENERGIA_KJ])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_LIPIDOS])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_ACS])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_HC])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_PROTEINA])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_SAL])}</td>\n"
            linhaGuardar += f"<td>{formatarParaFloat(ingreUtilizar[COL_REF_ING_ACUCAR])}</td>\n"
            linhaGuardar += "</tr>\n"

            totalQtd += float(ingreUtilizar[COL_REF_ING_QTD])
            totalKCal += float(ingreUtilizar[COL_REF_ING_ENERGIA_KCAL])
            totalKJ += float(ingreUtilizar[COL_REF_ING_ENERGIA_KJ])
            totalLIP += float(ingreUtilizar[COL_REF_ING_LIPIDOS])
            totalACS += float(ingreUtilizar[COL_REF_ING_ACS])
            totalHC += float(ingreUtilizar[COL_REF_ING_HC])
            totalPROT += float(ingreUtilizar[COL_REF_ING_PROTEINA])
            totalSAL += float(ingreUtilizar[COL_REF_ING_SAL])
            totalACUCAR += float(ingreUtilizar[COL_REF_ING_ACUCAR])


        linhaGuardar += "<tr>\n"
        linhaGuardar += f"<td>&nbsp;</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalQtd)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalKCal)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalKJ)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalLIP)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalACS)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalHC)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalPROT)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalSAL)}</td>\n"
        linhaGuardar += f"<td>{formatarParaFloat(totalACUCAR)}</td>\n"
        linhaGuardar += "</tr>\n"

        conteudoFicheiro = conteudoFicheiro.replace("%INGREDIENTES%", linhaGuardar)


        linhaGuardar = "<td>"
        for passo in refeicaoModoPreparacao:
            linhaGuardar += passo.replace(";", "") + "<br>\n" 
        linhaGuardar += "</td>"
        conteudoFicheiro = conteudoFicheiro.replace("%MODOPREPARACAO%", linhaGuardar)

        handlerFicheiro = open(ficheiroFichaTecnica, 'w', encoding='utf-8')
        handlerFicheiro.write(conteudoFicheiro)
        handlerFicheiro.close()

        webbrowser.open('file://' + os.path.realpath('./') + '/' + ficheiroFichaTecnica)
        dialogInformacao(stdscr, 'Impressão concluída.')
        return
    except:
        conteudoFicheiro = ''

    dialogInformacao(stdscr, 'Não foi possível criar a impressão da ficha técnica.', dialogColorPair = 13)
