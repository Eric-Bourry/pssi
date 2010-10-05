# -*- coding: utf-8 -*-

# -- bruteforce.py
# Bruteforces through the file structure

from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.util import toHexString


import sys
import display
from  card_interface import *


recursiveMode = False


def explore(connection, startAddress = [], space = "", firstByteMin = 0,
           firstByteMax = 0xff, secondByteMin = 0, secondByteMax = 0xff):

    selectFileMode = 0x08
    response, sw1, sw2, size = selectFile(connection, [0,0], selectFileMode)
    if statusWrongParameters(sw1, sw2):
        selectFileMode = 0x02

    for firstByte in range(firstByteMin, firstByteMax+1):
    #    print space + ("0x%02x" % firstByte) + " 0xxx"
        for secondByte in range(secondByteMin, secondByteMax+1):
            address = startAddress + [firstByte, secondByte]
            response, sw1, sw2, size = selectFile(connection, address, selectFileMode)

            if not statusIsOK(sw1, sw2):
                continue
            # Le select est bon, on regarde les enregistrements.
            display.printAddress(address, space)

            for recordNumber in range(255):
                response, sw1, sw2 = readRecord(connection, recordNumber+1)
                print "\t",
                if statusIsOK(sw1, sw2):
                    display.printRecordInBinary(response, recordNumber+1)
                else:
                    if statusSecurityNotOK(sw1, sw2):
                        print "Security status not satisfied\n"
                    elif statusCommandNotAllowed(sw1, sw2): # ie. c'est un DF
                        print "This is a DF\n"
                        if recursiveMode:
                            explore(connection, startAddress+address, space+"   ")
                    elif statusRecordNotFound(sw1, sw2):
                        # Record not found, it was the last one
                        print "Total: %u record(s)\n" % (recordNumber)
                    elif statusBadLength(sw1, sw2):
                        # mauvaise longueur, on peut recuperer le coup.
                        len = sw2
                        response, sw1, sw2 = readRecord(connection, recordNumber+1, sw2)
                        if statusIsOK(sw1, sw2):
                            display.printRecordInBinary(response, recordNumber+1)
                            print "\t(longueur %d)\n" % len
                    else:
                        print "Unknown error: %02x %02x\n" % (sw1, sw2)
                    break


def startBruteforce():
    card = getCard()
    if card:
        explore(card, [], "", 0x00, 0x3f, 0x00, 0x80)
