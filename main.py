from pdf_searcher.pdf import find_decree
from pdf_searcher.pdf import find_nomination
from pdf_searcher.pdf import insights_decree
from pdf_searcher.pdf import insights_nomination
from scrapper.scrapper import get_gazzete

menu = "============================================" \
"\n1 = BUSCAR DIÁRIOS MAIS RECENTES" \
"\n2 = EXTRAIR DECRETOS DOS DIÁRIOS" \
"\n3 = EXTRAIR NOMEAÇÕES E EXONERAÇÕES DOS DIÁRIOS" \
"\n4 = OBTER INSIGHTS DOS DECRETOS EXTRAÍDOS" \
"\n5 = OBTER INSIGHTS DAS NOMEAÇÕES E EXONERAÇÕES EXTRAÍDAS" \
"\nE = SAIR" \
"\n============================================" \
"\n=== "

while True:
    menu_inp = str(input(menu))
    
    if menu_inp == "1":
        get_gazzete()

    if menu_inp == "2":
        find_decree()

    if menu_inp == "3":
        find_nomination()

    if menu_inp == "4":
        insights_decree()

    if menu_inp == "5":
        insights_nomination()

    if menu_inp == "E":
        break