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
import tkinter
import os
import datetime
import display
import time

class ReloadDump():
    def __init__(self):
        return

    def __str__(self):
        print(": ","There was an error during the dumping process")

# remember which cards have already been seen
dumped = [] 


def dumpCard(card):
    ''' Connects to a card, dumps the data, disconnects, and produces a beep '''
    if not card_interface.connectToCard(card):
        return False
    tkinter.Tk().bell()
    try:
        content = structure_parser.parseCard(card.connection)
    except CardConnectionException:
        return False
    card.connection.disconnect()
    tkinter.Tk().bell()
    return content


class observer(CardObserver):
    ''' `directory' is where the dumps are stored '''
    def __init__(self, directory):
        self.directory = directory

    def update(self, observable, xxx_todo_changeme):
        ''' When a card is detected, its content is dumped into a file named
        `directory'/xx - ATR.txt'''
        (addedcards, removedcards) = xxx_todo_changeme
        try:
            for card in addedcards:
                tkinter.Tk().bell()
                if not card.atr in dumped:
                    content = dumpCard(card)
                    if content:
                        dumped.append(card.atr)
                        filename = "%s%s%02u - %s.txt" % \
                                                (self.directory, os.sep, len(dumped),
                                                 toHexString(card.atr))
                        print(filename, end=' ')
                        file = open(filename, 'w')
                        display.prettyPrintToFile(content, file)
                        file.close()
                        print(": OK.")
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
