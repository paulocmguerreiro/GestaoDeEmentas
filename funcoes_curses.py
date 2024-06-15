from consts import *
import os
import curses
import curses.ascii
import curses.panel
import curses.textpad
import datetime
import time
from funcoes import *

'''
    Desenhar uma Janela de Pedido de Confirmação
'''
def dialogConfirmacao(stdscr, mensagem = "Confirma a operação?", botaoConfirmacao = 'SIM', botaoCancelar = 'NÃO', dialogColorPair = 16):

    botaoConfirmacao = f' {botaoConfirmacao} '
    botaoCancelar = f' {botaoCancelar} '

    # saber a altura/largura dos itens
    larguraMaxima = len(mensagem)+4
    if larguraMaxima < 45:
        larguraMaxima = 45

    # Calcular Dimensões
    yMax, xMax = stdscr.getmaxyx()
    yPos = yMax // 2 - 4
    xPos = xMax // 2 - larguraMaxima // 2

    nw = curses.newwin(7, larguraMaxima, yPos + 1, xPos + 1)
    nw.bkgd(curses.color_pair(12) + curses.A_REVERSE)
    nw.clear()
    nw.refresh()
    nw.mvwin(yPos, xPos)

    nw.bkgd(curses.color_pair(dialogColorPair))
    nw.clear()
    nw.border()
    nw.addstr(0,2, '< Informação >')
    nw.addstr(2, 2, mensagem, curses.color_pair(dialogColorPair))
    botaoEscolhido = True
    posBotao1 = larguraMaxima // 4 - len(botaoConfirmacao) // 2
    posBotao2 = 3 * larguraMaxima // 4 - len(botaoConfirmacao) // 2
    while True:
        # controlar o botão seleccionado
        cor1 = curses.color_pair(dialogColorPair) + curses.A_REVERSE + curses.A_BOLD
        cor2 = curses.color_pair(dialogColorPair)
        if not botaoEscolhido:
            cor1, cor2 = cor2, cor1
        nw.addstr(4, posBotao1, botaoConfirmacao, cor1)
        nw.addstr(4, posBotao2, botaoCancelar, cor2)
        nw.refresh()
        tecla = stdscr.getch()

        # Seleccionar o botão
        if tecla == curses.KEY_ENTER or tecla in [10,13]:
            return botaoEscolhido
        # Navegar entre as opções
        if tecla in [curses.KEY_LEFT, curses.KEY_RIGHT]:
            botaoEscolhido = not botaoEscolhido


'''
    Desenhar uma janela de alerta, que, aguarda que o utilizador carregue numa tecla
'''
def dialogInformacao(stdscr, mensagem, dialogColorPair = 16 ):

    # saber a altura/largura dos itens
    larguraMaxima = len(mensagem)+4
    if larguraMaxima < 45:
        larguraMaxima = 45

    # Calcular Dimensões
    yMax, xMax = stdscr.getmaxyx()
    yPos = yMax // 2 - 3
    xPos = xMax // 2 - larguraMaxima // 2

    nw = curses.newwin(5, larguraMaxima, yPos + 1, xPos + 1)
    nw.bkgd(curses.color_pair(12) + curses.A_REVERSE)
    nw.clear()
    nw.refresh()
    nw.mvwin(yPos, xPos)

    nw.bkgd(curses.color_pair(dialogColorPair))
    nw.clear()
    nw.border()
    nw.addstr(0,2, '< Informação >')
    nw.addstr(2, 2, mensagem)
    nw.addstr(4, 2, '[ Carregue numa tecla para continuar! ]')
    nw.refresh()
    stdscr.getch()
    

'''
    Caixa para solicitar a introdução valores (texto/numeros) por parte do utilizador
'''
def inputDialog(stdscr, mensagem, dimensao):

    # saber a altura/largura dos itens
    larguraMaxima = len(mensagem)
    if larguraMaxima < dimensao:
        larguraMaxima = dimensao
    if larguraMaxima < 45:
        larguraMaxima = 45
    larguraMaxima += 4          # Contemplar espaço extra entre reborbo e informação

    # Calcular Dimensões
    yMax, xMax = stdscr.getmaxyx()
    yPos = yMax // 2 - 3
    xPos = xMax // 2 - larguraMaxima // 2

    nw = curses.newwin(5, larguraMaxima, yPos, xPos)
    nw.bkgd(curses.color_pair(1))
    nw.clear()
    nw.border()
    nw.addstr(0,2, '< ' + mensagem + ' >')
    nw.addstr(2,2, '')
    curses.echo(True)
    curses.curs_set(2)
    nw.attron( curses.color_pair(2))
    retorno = str(nw.getstr(dimensao).decode(encoding="utf-8"))
    curses.noecho()
    curses.curs_set(0)
    nw.refresh()
    return retorno

'''
    Caixa para introdução de um campo de observações (texto livre)
'''
def inputText(stdscr, titulo, largura, altura, conteudo):

    # Calcular Dimensões e outras Condições 
    yMax, xMax = stdscr.getmaxyx()
    janelaTopX = xMax // 2 - largura // 2
    janelaTopY = yMax // 2 - altura // 2
    if len(conteudo) == 0 :
        conteudo.append('')

    iniciarLinhaNaLista = 0
    iniciarColunaNaLista = 0
    cursorX = 0
    cursorY = 0

    nw = curses.newwin(altura, largura, janelaTopY, janelaTopX)

    while True:
        # Desenhar a Janela
        nw.bkgd(curses.color_pair(1))
        nw.clear()
        nw.border()
        nw.addstr(0,2, '< ' + titulo + ' >')
        nw.addstr(2,2, '')
        curses.echo(True)
        #curses.curs_set(2)
        nw.attron( curses.color_pair(2))
        curses.noecho()
        curses.curs_set(0)

        # Desenhar o conteúdo
        for linha in range(iniciarLinhaNaLista, iniciarLinhaNaLista + altura - 2):
            if linha < len(conteudo):
                mostrarTexto = conteudo[linha][iniciarColunaNaLista:]
                nw.addstr(linha - iniciarLinhaNaLista + 1, 1, mostrarTexto[:(largura-2)])

        stdscr.notimeout(1)
        nw.notimeout(1)

        # Calculos necessários para  aposicação onde estou a trabalhar
        posicaoColuna = iniciarColunaNaLista + cursorX
        posicaoLinha = iniciarLinhaNaLista + cursorY

        # Aguardar por uma ordem
        curses.curs_set(1)
        nw.attron( curses.color_pair(10))
        nw.addstr(cursorY + 1, cursorX + 1, '')
        nw.refresh()
        tecla = stdscr.get_wch( janelaTopY + cursorY + 1, janelaTopX + cursorX + 1)
        curses.curs_set(0)

        # Teclas que não são interpretadas como WIDE
        if type(tecla) is int:
            # Subir
            if tecla == curses.KEY_UP:
                if cursorY > 0:
                    cursorY -= 1
                    if len(conteudo[posicaoLinha-1]) <= ( iniciarColunaNaLista +  cursorX):
                        cursorX = len(conteudo[posicaoLinha-1])
                        iniciarColunaNaLista = 0
                        if cursorX >= largura - 2:
                            iniciarColunaNaLista = cursorX
                            cursorX = 0
                else:
                    if (iniciarLinhaNaLista > 0):
                        iniciarLinhaNaLista -= 1
            # Descer
            if tecla == curses.KEY_DOWN:
                if iniciarLinhaNaLista + cursorY + 1 < len(conteudo):
                    cursorY += 1
                    if len(conteudo[posicaoLinha+1]) < ( iniciarColunaNaLista +  cursorX):
                        cursorX = len(conteudo[posicaoLinha+1])
                        iniciarColunaNaLista = 0
                        if cursorX >= largura - 2:
                            iniciarColunaNaLista = cursorX
                            cursorX = 0
                # Ultrapassou?
                if (cursorY >= altura - 2 ):
                    cursorY -= 1
                    iniciarLinhaNaLista += 1
            # Esquerda
            if tecla == curses.KEY_LEFT:
                if cursorX > 0:
                    cursorX -= 1
                else:
                    if iniciarColunaNaLista > 0:
                        iniciarColunaNaLista -= 1
            # Direita
            if tecla == curses.KEY_RIGHT:
                if len(conteudo[posicaoLinha]) >= iniciarColunaNaLista + cursorX + 1:
                    if cursorX + iniciarColunaNaLista + 1 >= largura - 2:
                        iniciarColunaNaLista += 1
                    else:
                        cursorX += 1

        else:

            # Delete
            if tecla == chr(curses.ascii.DEL) or tecla == chr(curses.ascii.BS):
                if posicaoColuna == 0:
                    if posicaoLinha > 0:
                        cursorX = len(conteudo[posicaoLinha-1])
                        conteudo[posicaoLinha-1] += conteudo[posicaoLinha]
                        if cursorX <= largura - 2:
                            iniciarColunaNaLista = 0
                        else:
                            iniciarColunaNaLista = cursorX
                            cursorX = 0
                             
                        conteudo.remove(conteudo[posicaoLinha])

                        if cursorY > 0:
                            cursorY -= 1
                        else:
                            iniciarLinhaNaLista -= 1
                    continue
                        
                texto = list(conteudo[posicaoLinha])
                conteudo[posicaoLinha] = ''.join(texto[:(posicaoColuna-1)]) + ''.join(texto[(posicaoColuna):]) 
                if cursorX > 0:
                    cursorX -= 1
                else:
                    if iniciarColunaNaLista > 0:
                        iniciarColunaNaLista -= 1
                continue

            # ENTER
            if tecla == chr(10) or tecla == chr(13):
                conteudo.insert(posicaoLinha + 1, conteudo[posicaoLinha][posicaoColuna:] )
                conteudo[posicaoLinha] = conteudo[posicaoLinha][:posicaoColuna]
                cursorY += 1
                cursorX = 0
                iniciarColunaNaLista = 0
                if cursorY >= altura - 2:
                    cursorY -= 1
                    iniciarLinhaNaLista += 1
                continue

            # Terminar
            if tecla == u"\u001B":
                break

        
            # Adicionar um Caracter
            texto = list(conteudo[posicaoLinha])
            texto.insert(posicaoColuna, tecla)
            conteudo[posicaoLinha] = ''.join(texto)
            cursorX += 1


        # Rever as posições para o caso de ao alterar o texto sair para fora do espaço visivel
        if cursorY >= altura - 2:
            cursorY -= 1
            iniciarLinhaNaLista += 1
        
        if cursorX >= largura - 2:
            cursorX -= 1
            iniciarColunaNaLista += 1

          




    return conteudo




'''
    Desenhar e gerir uma lista de valores, com funcionnalidade de navegação, selecção e reconhecimento de teclas especiais.
'''
def inputLista(stdscr, listaItens, titulo, rodape, yPos, xPos, alturaMaxima, larguraMaxima, posicaoSeleccionada, teclasExtraTerminar = None, desenharContornos = True, editar = True):
    espacoContornosLateral = 0
    espacoContornoSombra = 0
    if desenharContornos:
        espacoContornosLateral = 2
        espacoContornoSombra = 1

    # Sombra
    larguraMaxima -= espacoContornoSombra
    alturaMaxima -= espacoContornoSombra

    # Normalizar a lista
    listaItensDisplay = []
    for idxMenu in range(len(listaItens)):
        listaItensDisplay.append(
            ("{:<" + str(larguraMaxima-espacoContornosLateral) + "}").format(listaItens[idxMenu])[:larguraMaxima-espacoContornosLateral])

    # Desenhar Janela
    nw = curses.newwin(alturaMaxima , larguraMaxima, yPos + espacoContornoSombra, xPos + espacoContornoSombra)
    if desenharContornos:
        nw.bkgd(curses.color_pair(12) + curses.A_REVERSE)
        nw.clear()
        nw.refresh()
        nw.mvwin(yPos, xPos)

    nw.bkgd(curses.color_pair(10))
    nw.clear()

    # Gerir espaços para o cabeçalho e rodapé
    alturaRodape = 0
    alturaCabecalho = 0
    if desenharContornos:
        nw.box()
        alturaRodape = 1
        alturaCabecalho = 1
    if len(titulo) > 0:
        nw.addstr(0, espacoContornosLateral, ('< ' + titulo + ' >')[:larguraMaxima - espacoContornosLateral*2 - 1])
        alturaCabecalho = 1
    if len(rodape) > 0:
        nw.addstr(alturaMaxima - 1, espacoContornosLateral, ('[ ' + rodape + ' ]')[:larguraMaxima - espacoContornosLateral*2 - 1])
        alturaRodape = 1

    # Desenhar Lista
    primeiroItem = 0
    if posicaoSeleccionada >= len(listaItens):
        posicaoSeleccionada = len(listaItens)-1
    if posicaoSeleccionada < 0:
        posicaoSeleccionada = 0
        primeiroItem = 0

    # Garantir que tenho uma opção escolhida que existe (para o caso de entrar com uma opção seleccionada)
    if posicaoSeleccionada >= alturaMaxima:
        primeiroItem = posicaoSeleccionada - alturaMaxima // 2
        if primeiroItem < 0:
            primeiroItem = 0

    while True:
        # Desenhar a secção visivel da lista (incluíndo a opção seleccionada)
        iLinha = alturaCabecalho
        textoLinhaSelecionada = ''
        for idxItem in range(primeiroItem, primeiroItem + alturaMaxima - alturaCabecalho - alturaRodape):
            if idxItem < len(listaItensDisplay):
                if idxItem == posicaoSeleccionada:
                    nw.addnstr(iLinha, espacoContornosLateral // 2, listaItensDisplay[idxItem], larguraMaxima - espacoContornosLateral, curses.color_pair(
                        11) + curses.A_BOLD)
                    textoLinhaSelecionada = listaItens[idxItem]
                else:
                    nw.addnstr(iLinha, espacoContornosLateral // 2, listaItensDisplay[idxItem], larguraMaxima - espacoContornosLateral, curses.color_pair(12))
            else:
                nw.addstr(iLinha, espacoContornosLateral // 2, " "*(larguraMaxima - espacoContornosLateral), curses.color_pair(12))
            iLinha += 1
        nw.refresh()
        #stdscr.refresh()

        # Controlar o caso em que esta função foi executada com o propósito de somente mostrar a lista de dados
        if not editar:
            return -1, '', curses.ascii.ESC

        stdscr.notimeout(1)
        nw.notimeout(1)

        tecla = stdscr.getch()

        # Mover
        if tecla == curses.KEY_UP and posicaoSeleccionada > 0:
            posicaoSeleccionada -= 1
        if tecla == curses.KEY_DOWN and posicaoSeleccionada < len(listaItens)-1:
            posicaoSeleccionada += 1
        # Sair sem selecionar
        if tecla == curses.ascii.ESC or tecla in [27]:
            return -1, '', curses.ascii.ESC
        # Escolher uma opção
        if tecla == curses.KEY_ENTER or tecla in [10, 13]:
            return posicaoSeleccionada, textoLinhaSelecionada, curses.KEY_ENTER
        # Sair através de um atalho
        if teclasExtraTerminar:
            if tecla in teclasExtraTerminar:
                return posicaoSeleccionada, textoLinhaSelecionada, tecla

        # Acertar a lista visível
        if posicaoSeleccionada < primeiroItem:
            primeiroItem -= 1
        if posicaoSeleccionada >= primeiroItem + alturaMaxima - alturaCabecalho - alturaRodape:
            primeiroItem += 1


'''
    Desenhar um MENU e aguardar pela seleção de uma opção
'''
def inputMenu(stdscr):
    listaMenu = MENU_PRINCIPAL

    # saber a altura/largura dos itens
    alturaMaxima = len(listaMenu)
    larguraMaxima = 0
    for item in listaMenu:
        if len(item) > larguraMaxima:
            larguraMaxima = len(item)

    # Calcular Dimensões
    yMax, xMax = stdscr.getmaxyx()
    menuPosY = yMax // 2 - alturaMaxima // 2
    menuPosX = xMax // 2 - larguraMaxima // 2

    return inputLista(stdscr, listaMenu, 'MENU', '', menuPosY, menuPosX, alturaMaxima+3, larguraMaxima+3,0)



'''
    Desenhar uma grelha (similar excell) e gerir alguma funcionalidade
'''
def inputGrid(stdscr, listaItens, titulo, rodape, titulosColunas, dimensaoColunas, alinhamentoColunas, yPos, xPos, alturaMaxima, larguraMaxima, posicaoSeleccionada, teclasExtraTerminar = None):

    # Recalcular a dimensão das colunas
    somaTotal = 0
    qtdRecalculos = 0
    for col in dimensaoColunas:
        if col == -1:
            qtdRecalculos += 1
        else:
            somaTotal += col + 1            # Espaço Extra
    if qtdRecalculos > 0:
        dimCol = ( larguraMaxima - 2 - somaTotal ) // qtdRecalculos
        for colIdx in range(len(dimensaoColunas)):
            if dimensaoColunas[colIdx] == -1:
                dimensaoColunas[colIdx] = dimCol - 1

    # Normalizar a lista
    listaItensDisplay = []
    for idxMenu in range(len(listaItens)):
        strLinha = ''
        for idxCol in range(len(listaItens[idxMenu])):
            strLinha += (" {:" + alinhamentoColunas[idxCol] + str(dimensaoColunas[idxCol]) + "}").format(listaItens[idxMenu][idxCol])[:dimensaoColunas[idxCol]+1]
        listaItensDisplay.append(strLinha)

    # Desenhar os Títulos das Colunas
    for idxMenu in range(len(titulosColunas)):
        strLinha = ''
        for idxCol in range(len(titulosColunas[idxMenu])):
            strLinha += (" {:" + alinhamentoColunas[idxCol] + str(dimensaoColunas[idxCol]) + "}").format(titulosColunas[idxMenu][idxCol])
        stdscr.addstr(yPos + idxMenu, xPos, "*"*larguraMaxima, curses.color_pair(12) + curses.A_REVERSE)
        stdscr.addstr(yPos + idxMenu, xPos, strLinha, curses.color_pair(12) + curses.A_REVERSE)
    stdscr.refresh()

    return inputLista(stdscr, listaItensDisplay, '', rodape, yPos + len(titulosColunas), xPos, alturaMaxima - len(titulosColunas), larguraMaxima, posicaoSeleccionada, teclasExtraTerminar, False)


