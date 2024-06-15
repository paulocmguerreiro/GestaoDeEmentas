# Projeto - Gestão de Ementas

## Aplicação Gestão de Ementas

Este projeto consiste na criação de uma aplicação em Python no âmbito da formação dinamizada pela ANPRI intitulada Linguagem de Programação Python em Contexto Educativo – T3.
Resultou na produção de uma aplicação que para auxiliar a nutricionista do agrupamento na gestão da ementa escolar. Desta forma, a aplicação, recorre à Tabela da Composição de Alimentos do Instituto Nacional de Saúde Doutor Ricardo Jorge, I. P.- INSA. v 3.2 – 2018 disponibilizada na plataforma PortFIR - Plataforma Portuguesa de Informação Alimentar. Assim, a nutricionista tem a seu dispor uma ferramenta que lhe permite consultar, entre outra informação, a carga calórica de cada alimento, estruturar uma refeição tendo em conta as quantidades pretendidas dos seus ingredientes, e por fim, produzir as ementas semanais com uma distribuição ponderada de refeições.

### Requisitos da aplicação

-   É necessário ter o Python na versão 3+ com o módulo curses ou windows-curses instalado dependendo do sistema operativo (pip install windows-curses);
-   Dimensão da consola de terminal:
    -   Recomendado: 130 colunas por 35 linhas
    -   Mínimo: 95 colunas por 35 linhas

### Instalação da aplicação

Todos os ficheiros disponibilizados devem estar contidos numa pasta de trabalho de acordo com o tipo de ementa (ex: gestão-almoco, gestão-almoço-dieta, gestão- vegetariano, entre outros).

### Executar a aplicação

A aplicação é executada através do programa projeto.py na pasta de instalação.

### Estrutura da aplicação

A aplicação é composta pelos seguintes ficheiros:

-   Python – Aplicação e módulos:
    -   projeto.py: Aplicação Gestão de Ementas;
    -   ingredientes.py: Módulo da aplicação com as funcionalidades necessárias para consulta dos ingredientes importados do ficheiro TCA;
    -   ementas.py: Módulo da aplicação com as funcionalidades necessárias para a gestão das ementas;
    -   refeicoes.py: Módulo da aplicação com as funcionalidades necessárias para a gestão das refeições;
    -   funções_curses.py: Módulo da aplicação com as funcionalidades necessárias para a gerir o aspeto gráfico/visual da aplicação;
    -   funções.py: Módulo da aplicação com as funcionalidades necessárias para o geral funcionamento da aplicação;
    -   consts.py: Contêm constantes com utilização nas diversas componentes da aplicação;
-   Ficheiros adicionais:

    -   Insa_tca.xslx: Documento TCA1 (Tabela de Composição de Alimentos);
    -   Insa_tca.csv: Documento TCA convertido em .csv para uso da aplicação;
    -   tipos_refeicao.dat: Ficheiro que contêm os diversos tipos de refeição que podem ser utilizados.
    -   > Nota: Inicialmente era pretendido gerir este ficheiro através da aplicação, no entanto, foi verificado que não justificava tal funcionalidade. Se pretendido, este ficheiro pode ser personalizado e acrescentar novos tipos de refeição.

-   Modelos de Impressão:
    -   ementas.html: Estrutura do modelo de impressão da ementa semanal, este documento pode ser ajustado para personalizar o seu aspeto visual;
    -   ficha_tecnica.html: Estrutura do modelo de impressão da ficha técnica de uma refeição, este documento pode ser ajustado para personalizar o seu aspeto visual;
