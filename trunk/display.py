# -*- coding: utf-8 -*-

from smartcard.util import toHexString
import types
import sys

verboseMode = False

def formatOutput(interpretation, rawdata, comment):
    """Returns a string with the value of a field, its interpretation
    and a comment in verbose mode."""
    global verboseMode
    if verboseMode:
        return "%-35s ---   %s (%s)" % (interpretation, rawdata, comment)
    return "%-35s (%s)" % (interpretation, comment)

# TODO : également dans les interpréteurs ?
# TODO : Faire des fonctions dispo aux interpréteurs, du genre matchWithCode
def hexListToBinaryString(tab):
    """Returns a string containing the binary representation of `tab'."""
    s = ''
    blen = len(tab) * 8
    for b in range(0, blen):
        s = s + "%d" % (((tab[b/8] >> ((7-b)%8))) & 1)
    return s

# TODO(m): nom pourri
def printExchange(query, response, sw1, sw2):
    """Prints an APDU exchange (query-response)."""
    print ">> ",
    if type(query) is types.ListType:
         print toHexString(query)
    else:
        print query
    print "<< ", toHexString(response), " / ", "%x %x" % (sw1, sw2)

def printExchangeWithBinary(query, response, sw1, sw2):
    """Prints an APDU exchange (query-response) in hexadecimal, and
    the response in binary."""
    printExchange(query, response, sw1, sw2)
    print "\t ==  ", hexListToBinaryString(response)

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
    # TODO(e): pourquoi le \n ?
    print "Error while verifying the PIN code\n"
    sys.exit()

def printAddress(address, space):
    length = len(address)
    print space, "[0x%02x%02x]" % (address[length-2], address[length-1])

def printRecord(response, nb):
    print "====  ", nb, "  ===="
    print "\t", hexListToBinaryString(response), "\n"


# Main printing functions.
def prettyPrint(data, tabs=""):
    """Pretty print to standard output."""
    if type(data) is types.DictType:
        for key in data["Keys"]:
            print
            if type(key) is types.StringType:
                print tabs, ("%-27s" % key),
                prettyPrint(data[key], tabs + "   ")
            else:
                print tabs, "====  ", key, "  ====",
                prettyPrint(data[key], tabs + "   ")
    else:
        print ": " + data,

def prettyPrintToFile(data, output_file, tabs=""):
    """Pretty print to `output_file' (handle)."""
    if type(data) is types.DictType:
        for key in data["Keys"]:
            output_file.write("\n")
            if type(key) is types.StringType:
                output_file.write("%s%-27s" % (tabs, key))
                prettyPrintToFile(data[key], output_file, tabs+"   ")
            else:
                output_file.write("%s====  %s  ====" % (tabs, str(key)))
                prettyPrintToFile(data[key], output_file, tabs)
    else:
        output_file.write(": "+str(data))
