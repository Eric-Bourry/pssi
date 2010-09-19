# -*- coding: utf-8 -*-

# -- dump.py
# The dumper


import display
import structure_parser
import card_interface

def startDump():
    card = card_interface.getCard()
    if card:
        content = structure_parser.parseCard(card)
        display.prettyPrint(content)
