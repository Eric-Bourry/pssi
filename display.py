# -*- coding: utf-8 -*-

from smartcard.util import toHexString

import sys

verboseMode = False

def formatOutput(interpretation, rawdata, comment):
    global verboseMode
    if verboseMode:
        return ("%-35s" % interpretation)+" ---   "+str(rawdata)+" ("+comment+")"
    return ("%-35s" % interpretation)+" ("+comment+")"

# TODO : également dans les interpréteurs ?
# TODO : Faire des fonctions dispo aux interpréteurs, du genre matchWithCode
def hexListToBinaryString(tab):
    """retourne la chaine de la representation binaire de tab"""
    s = ''
    blen = len(tab) * 8
    for b in range(0,blen):
        s = s + "%d" % (((tab[b/8] >> ((7-b)%8))) & 1)
    return s


# FIXME: nom pourri
def printExchange(query, response, sw1, sw2):
    """Affiche un échange query-response."""
    print ">> ",
    if type(query) == type([]):
         print toHexString(query)
    else:
        print query
    print "<< ", toHexString(response), " / ", "%x %x" % (sw1, sw2)

def printExchangeWithBinary(query, response, sw1, sw2):
    """Affiche un échange query-response, avec en plus la reponse en binaire."""
    printExchange(query, response, sw1, sw2)
    print "\t ==  ", toBinaryString(response)


def readPIN():
    print "PIN code required, please enter it:"
    code = raw_input('--> ')
    code = code[0:8]
    pin = []
    for c in code:
        pin.append(ord(c))
    for i in range(len(code), 8):
        pin.append(0xff)
    return pin 


def errorPIN():
    print "Error while verifying the PIN code\n"
    sys.exit()


def printAddress(address, space):
    length = len(address)
    print space, "[0x%02x%02x]" % (address[length-2], address[length-1])
    
    
def printRecord(response, nb):
    print "====  ", nb, "  ===="
    print "\t", toBinaryString(response), "\n"


def prettyPrint(data, tabs=""):
    if type(data) == type(dict()):
        for key in data["Keys"]:
            print
            if (type(key) == type("")):
                print tabs, ("%-27s" % key),
                prettyPrint(data[key], tabs+"   ")
            else:
                print tabs, "====  ", key, "  ====",
                prettyPrint(data[key], tabs+"   ")
    else:
        print ": "+data,
                
def prettyPrintToFile(data, file, tabs=""):
    """Ecriture d'un dump sous forme lisible dans le fichier `file' (handle)."""
    if type(data) == type(dict()):
        for key in data["Keys"]:
            file.write("\n")
            if (type(key) == type("")):
                file.write(tabs)
                file.write(("%-27s" % key))
                prettyPrintToFile(data[key], file, tabs+"   ")
            else:
                file.write(tabs)
                file.write("====  ")
                file.write(str(key))
                file.write("  ====")
                prettyPrintToFile(data[key], file, tabs)
    else:
        file.write(": "+str(data))
