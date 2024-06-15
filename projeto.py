#!/usr/bin/env python
# encoding: utf-8
import os
import curses
import curses.ascii
import curses.panel
import curses.textpad
import datetime
import time
import locale
import sys

from funcoes import *
from funcoes_curses import *
from consts import *

import ingredientes
import refeicoes
import ementas

# Carregar informação
bCarregouInformacao = True
bCarregouInformacao = ingredientes.carregarInformacaoFicheiroIngredientes(listaNivel1, listaNivel2, listaNivel3, listaIngredientes) or bCarregouInformacao
bCarregouInformacao = refeicoes.carregarInformacaoFicheiroTiposDeRefeicao(listaTiposDeRefeicao) or bCarregouInformacao

# PONTO DE ENTRADA DO PROGRAMA
def entrada(stdscr):
    curses.curs_set(0)
    #curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_YELLOW)

    curses.init_pair(10, curses.COLOR_RED, curses.COLOR_WHITE)                  # JANELA
    curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLUE)                 # LINHA SELECIONADA
    curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_WHITE)                # LINHA TEXTO
    curses.init_pair(13, curses.COLOR_WHITE, curses.COLOR_RED)                  # JANELA ERRO
    curses.init_pair(14, curses.COLOR_YELLOW, curses.COLOR_RED)                 # JANELA ERRO
    curses.init_pair(15, curses.COLOR_BLUE, curses.COLOR_WHITE)                 # Linha de Informação (resultado do input)
    curses.init_pair(16, curses.COLOR_WHITE, curses.COLOR_GREEN)                # JANELA Confirmação

    while True:
        stdscr.notimeout(1)
        stdscr.attron(curses.color_pair(1))
        stdscr.bkgd(curses.color_pair(1))
        stdscr.clear()
        stdscr.refresh()

        yMax, xMax = stdscr.getmaxyx()

        # Verificar requisitos mínimos
        if yMax < 35 or xMax < 95:
            dialogInformacao(stdscr, "O terminal não cumpre os requisitos", dialogColorPair = 13)
            print("A console de terminal não cumpre os requisitos mínimos, por favor, prepara a consola para o mínimo de 95 colunas e 35 linhas.")
            return

        # Desenhar Logo
        posLinha = 2
        for linha in cabecalhoEntrada:
            stdscr.addstr(posLinha, xMax // 2 - len(linha) // 2 , linha)
            posLinha+=1

        posLinha = yMax - len(rodapeEntrada) - 3
        for linha in rodapeEntrada:
            stdscr.addstr(posLinha, xMax // 2 - len(linha) // 2 , linha)
            posLinha+=1

        stdscr.addstr(yMax-2, xMax // 2 - 26  , "Paulo Guerreiro - 2019/20")

        idxPos, opcao, teclaSaida = inputMenu(stdscr)

        # Ingredientes
        if opcao == MENU_OPCAO_INGREDIENTES:
            ingredientes.listarIngredientes(stdscr)

        # Refeições
        if opcao == MENU_OPCAO_REFEICOES:
            refeicoes.listarTiposDeRefeicoes(stdscr)

        # Ementas
        if opcao == MENU_OPCAO_EMENTA:
            ementas.listarEmentas(stdscr)

        # Sair?
        if opcao == '' or opcao == MENU_OPCAO_SAIR:
            if dialogConfirmacao(stdscr, 'Pretende sair da aplicação?', dialogColorPair = 13):
                break

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, "pt")
else:
    locale.setlocale(locale.LC_ALL, "pt_PT")

# Iniciar a aplicação - Através do Curses
curses.wrapper(entrada)
