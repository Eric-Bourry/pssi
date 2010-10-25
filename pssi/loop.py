# -*- coding: utf-8 -*-

# -- loop.py
# Card scanner


# Copyright © 2010 Eric Bourry & Julien Flaissy

# This file is part of PSSI (Python Simple Smartcard Interpreter).

# PSSI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PSSI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PSSI.  If not, see <http://www.gnu.org/licenses/>


from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString


import structure_parser
import card_interface
import Tkinter
import os
import datetime
import exceptions
import display
import time

class ReloadDump(exceptions.Exception):
    def __init__(self):
        return

    def __str__(self):
        print ": ","There was an error during the dumping process"


dumped = [] # les cartes deja vues


def dumpCard(card):
    """Initie une connection à la carte, dumpe, se déconnecte
    et fait un beep."""
    if not card_interface.connectToCard(card):
        return False
    Tkinter.Tk().bell()
    try:
        content = structure_parser.parseCard(card.connection)
    except CardConnectionException:
        return False
    card.connection.disconnect()
    Tkinter.Tk().bell()
    return content


class observer(CardObserver):
    """`directory' est le repertoire où on stocke les dumps."""
    def __init__(self, directory):
        self.directory = directory

    def update(self, observable, (addedcards, removedcards)):
        """Quand on detecte un carte, on dumpe puis on l'ecrit dans
        le fichier `directory'/xx - ATR.txt"""
        try:
            for card in addedcards:
                Tkinter.Tk().bell()
                if not card.atr in dumped:
                    content = dumpCard(card)
                    if content:
                        dumped.append(card.atr)
                        filename = "%s%s%02u - %s.txt" % \
                                                (self.directory, os.sep, len(dumped),
                                                 toHexString(card.atr))
                        print filename,
                        file = open(filename, 'w')
                        display.prettyPrintToFile(content, file)
                        file.close()
                        print ": OK."
                    else:
                        raise ReloadDump
        except ReloadDump:
            startLoop()
        except:
            return


def startLoop():
    now = datetime.datetime.today()
    directory = "%04u-%02u-%02u_%02uh%02um%02us" % \
        (now.year, now.month, now.day, now.hour, now.minute, now.second)
    os.makedirs(directory)
    cardmonitor = CardMonitor()
    cardobserver = observer(directory)
    cardmonitor.addObserver(cardobserver)
    while True:
        try:
            time.sleep(60)
        except:
            break

    cardmonitor.deleteObserver(cardobserver)
