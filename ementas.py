import os
import curses
import curses.ascii
import curses.panel
import curses.textpad
import datetime
import time
import locale

import webbrowser

from consts import *
from funcoes import *
from funcoes_curses import *
from refeicoes import escolherRefeicaoPorTipo, carregarRefeicao, totalCaloriasRefeicao

'''
    FORMULÁRIO : Gestão de Ementas
'''
def listarEmentas(stdscr):
    stdscr.clear()
    stdscr.refresh()
    yMax, xMax = stdscr.getmaxyx()

    # Posicionar no dia atual
    dataTrabalho = datetime.datetime.now()
    
    dataJanela = curses.newwin(3, xMax)
    ementaJanela = curses.newwin(yMax - 4, xMax, 3, 0)

    ementasSemana = []

    visualizarDia = 0
    visualizarTipoRefeicao = 0

    while True:
        dataJanela.bkgd(curses.color_pair(1))
        dataJanela.clear()
        dataJanela.box()
        dataJanela.addnstr(0, 2, '< Semana da Ementa >', xMax - 4)
        dataJanela.addnstr(2, 2, '[ ESC = Sair / F2 - Semana Anterior / F3 = Próxima Semana / F4 = Imprimir Ementa ]', xMax - 4)

        ementaJanela.bkgd(curses.color_pair(10))
        ementaJanela.clear()
        ementaJanela.box()
        ementaJanela.addnstr(0, 2, '< Ementas >', xMax - 4)
        ementaJanela.addnstr(yMax - 5, 2, '[ ESC = Sair / ENTER = Escolher Refeição / - = Remover Refeição ]', xMax - 4)

        # Informação da Semana
        anoTrabalho, semanaTrabalho, diaSemanaTrabalho = dataTrabalho.isocalendar()
        dataPrimeiroDia = dataTemp = dataTrabalho
        while dataTemp.isocalendar()[1] == semanaTrabalho:
            dataPrimeiroDia -= datetime.timedelta(days=1)
            dataTemp = dataPrimeiroDia

        # Recarregar dados
        if len(ementasSemana) == 0:
            if not carregarEmentas(ementasSemana, anoTrabalho, semanaTrabalho):
                dialogInformacao(stdscr, 'Não foi possível carregar a informação das ementas.', dialogColorPair = 13)

        dataJanela.addstr(1,2, f'Ano {anoTrabalho} - Semana {semanaTrabalho}', curses.color_pair(11) + curses.A_BOLD + curses.A_BLINK)

        dataJanela.addstr(1,xMax // 2, 'Inicia a ' + dataPrimeiroDia.strftime("%A, %d de %B de %Y"), curses.color_pair(11) + curses.A_BOLD + curses.A_BLINK)

        # Mostrar a informação dos dias/tipos refeições/refeições
        dataPrimeiroDia += datetime.timedelta(days=1)   # Primeiro Dia da Semana é o Domingo e somente pretendo trabalhar a partir de segunda
        for dia in range(5):
            posDia = 2 + dia * (len(listaTiposDeRefeicao)+1)
            diaMostrar = dataPrimeiroDia + datetime.timedelta(days=dia)
            ementaJanela.addnstr( posDia, 1, ("{:<" + str(xMax-2) + "}").format(diaMostrar.strftime("%A, %d de %B de %Y")), xMax - 2, curses.color_pair(1))
            posRefeicao = posDia + 1
            for tipo in range(len(listaTiposDeRefeicao)):
                cor1 = curses.color_pair(12)
                cor2 = curses.color_pair(15)
                if dia == visualizarDia and tipo == visualizarTipoRefeicao:
                    cor1 = cor2 = curses.color_pair(12) + curses.A_BOLD + curses.A_REVERSE
                ementaJanela.addnstr(posRefeicao, 1, ("{:<20}").format(listaTiposDeRefeicao[tipo]), 20, cor1)
                ementaJanela.addnstr(posRefeicao,21, ("{:<" + str(xMax-2-20) + "}").format( ementasSemana[dia].get(listaTiposDeRefeicao[tipo])), xMax - 2 - 20, cor2)
                posRefeicao += 1


        stdscr.refresh()
        dataJanela.refresh()
        ementaJanela.refresh()

        tecla = stdscr.getch()

        # Sair
        if tecla in [curses.ascii.ESC, 27]:
            return
        
        # Semana Anterior
        if tecla == curses.KEY_F2:
            dataTrabalho -= datetime.timedelta(days=7)
            ementasSemana.clear()

        # Próxima Semana
        if tecla == curses.KEY_F3:
            dataTrabalho += datetime.timedelta(days=7)
            ementasSemana.clear()

        # Imprimir Ementa da Semana
        if tecla == curses.KEY_F4:
            imprimirEmenta(stdscr, ementasSemana, anoTrabalho, semanaTrabalho, dataPrimeiroDia.timestamp())

        # Remover a refeição deste dia
        if tecla == ord('-'):
            if dialogConfirmacao(stdscr, 'Pretende retirar a refeição?', dialogColorPair = 13):
                ementasSemana[visualizarDia][listaTiposDeRefeicao[visualizarTipoRefeicao]] = ''
                if not guardarEmentas(ementasSemana, anoTrabalho, semanaTrabalho):
                    dialogInformacao(stdscr, 'Não foi possível guardar a informação das ementas.', dialogColorPair = 13)

        # Navegar nos dias/refeições
        if tecla == curses.KEY_UP:
            visualizarTipoRefeicao -= 1
            if visualizarTipoRefeicao < 0:
                visualizarTipoRefeicao = len(listaTiposDeRefeicao)-1
                visualizarDia -= 1
                if visualizarDia < 0:
                    visualizarDia = 0
                    visualizarTipoRefeicao = 0

        # Navegar nos dias/refeições
        if tecla == curses.KEY_DOWN:
            visualizarTipoRefeicao += 1
            if visualizarTipoRefeicao >= len(listaTiposDeRefeicao):
                visualizarTipoRefeicao = 0
                visualizarDia += 1
                if visualizarDia > 4:
                    visualizarDia = 4
                    visualizarTipoRefeicao = len(listaTiposDeRefeicao)-1

        # Escolher uma refeição
        if tecla in [curses.KEY_ENTER, 10, 13]:
            ementasSemana[visualizarDia][listaTiposDeRefeicao[visualizarTipoRefeicao]] = escolherRefeicaoPorTipo(stdscr, listaTiposDeRefeicao[visualizarTipoRefeicao], ementasSemana[visualizarDia][listaTiposDeRefeicao[visualizarTipoRefeicao]])
            if not guardarEmentas(ementasSemana, anoTrabalho, semanaTrabalho):
                dialogInformacao(stdscr, 'Não foi possível guardar a informação das ementas.', dialogColorPair = 13)

'''
    Imprimsão da ementa do Dia
'''
def imprimirEmenta(stdscr, listaEmentas, anoTrabalho, semanaTrabalho, dataPrimeiroDia):
    ficheiroEmentas = f'{FICHEIRO_EMENTAS_OUTPUT}{anoTrabalho}_{semanaTrabalho}.html'
    dataPrimeiroDia = datetime.datetime.fromtimestamp(dataPrimeiroDia)

    try:
        
        handlerFicheiro = open(FICHEIRO_HTML_EMENTAS, 'r', encoding='utf-8')
        conteudoFicheiro = handlerFicheiro.read()
        handlerFicheiro.close()

        conteudoFicheiro = conteudoFicheiro.replace("%ANO%", str(anoTrabalho) )
        conteudoFicheiro = conteudoFicheiro.replace("%SEMANA%", str(semanaTrabalho) )
                
        for dia in range(len(listaEmentas)):
            diaTrabalho = dataPrimeiroDia + datetime.timedelta(days=dia)
            conteudoFicheiro = conteudoFicheiro.replace("%DIA_" + str(dia) + "%",diaTrabalho.strftime("%A, %d de %B de %Y") )
            linhaGuardar = ""
            totalCalorias = 0
            
            for chave, valor in (listaEmentas[dia]).items():
                
                refIng = []
                refeicaoModoPreparacao = []
                carregarRefeicao(refIng, chave, valor, refeicaoModoPreparacao)
                totalR = totalCaloriasRefeicao(refIng)
                totalCalorias += totalR

                linhaGuardar += "<tr>\n"
                linhaGuardar += f"<th>{chave}</th>\n"
                linhaGuardar += f"<td>{valor}</td>\n"
                if totalR == 0:
                    linhaGuardar += f"<td>&nbsp;</td>\n"
                else:
                    linhaGuardar += f"<td>{formatarParaFloat(totalR)} kcal</td>\n"
                linhaGuardar += "</tr>\n"
            
            if  totalCalorias != 0:
                linhaGuardar += f"<tr><td colspan='3'>{formatarParaFloat(totalCalorias)} kcal</td></tr>\n"
            conteudoFicheiro = conteudoFicheiro.replace("%EMENTAS_" + str(dia) + "%", linhaGuardar )
        
        handlerFicheiro = open(ficheiroEmentas, 'w', encoding='utf-8')
        handlerFicheiro.write(conteudoFicheiro)
        handlerFicheiro.close()
        
        webbrowser.open('file://' + os.path.realpath('./') + '/' + ficheiroEmentas)
        dialogInformacao(stdscr, 'Impressão concluída.')
        return
    except:
        conteudoFicheiro = ''

    dialogInformacao(stdscr, 'Não foi possível criar a impressão da ementa da semana.', dialogColorPair = 13)



'''
    Carregar a informação dos títulos das refeições de um determinado tipo de refeição
'''
def carregarEmentas(listaEmentas, ano, semana):
    ficheiroEmentas = f'{FICHEIRO_EMENTAS}{ano}_{semana}.dat'
    if not prepararFicheiro(ficheiroEmentas):
        return False
    try:
        listaEmentas.clear()
        # Dias da Semana
        for aux in range(5):
            temp = dict()
            for tipo in listaTiposDeRefeicao:
                temp[tipo] = ''
            listaEmentas.append(temp)

        handlerFicheiro = open(ficheiroEmentas, 'r', encoding='utf-8')
        for linhaRefeicao in handlerFicheiro:
            linhaTratar = linhaRefeicao.replace('\n', '').split(';')
            listaEmentas[int(linhaTratar[0])][linhaTratar[1]] = linhaTratar[2]

        handlerFicheiro.close()
    except:
        print(f'O ficheiro "{ficheiroEmentas}" existe mas não foi possível ler o seu conteúdo.' )
        return False

    return True


'''
    Guardar a informação dos títulos das refeições de um determinado tipo de refeição
'''
def guardarEmentas(listaEmentas, ano, semana):
    ficheiroEmentas = f'{FICHEIRO_EMENTAS}{ano}_{semana}.dat'
    if not prepararFicheiro(ficheiroEmentas):
        return False
    try:
        handlerFicheiro = open(ficheiroEmentas, 'w', encoding='utf-8')
        for linhaRefeicao in range(len(listaEmentas)):
            for tipo in listaTiposDeRefeicao:
                handlerFicheiro.write(f'{linhaRefeicao};{tipo};{listaEmentas[linhaRefeicao][tipo]};\n')
        handlerFicheiro.close()
    except:
        print(f'O ficheiro "{ficheiroEmentas}" existe mas não foi possível ler o seu conteúdo.' )
        return False

    return True
