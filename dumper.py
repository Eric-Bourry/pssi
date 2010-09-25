# -*- coding: utf-8 -*-

# -- dump.py
# The dumper


import display
import structure_parser
import card_interface

def startDump():
    """Launch the dumping process: parse the card and print the
    results."""
    card = card_interface.getCard()
    if card:
        content = structure_parser.parseCard(card)
        display.prettyPrint(content)
