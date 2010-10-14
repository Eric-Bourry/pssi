# -*- coding: utf-8 -*-

# -- display.py
# Output and formatting functions


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


from smartcard.util import toHexString
import types
import sys

# In verbose mode, we output the raw data
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
    """Asks the user for his PIN code, and returns it as a sequence of 8 bytes"""
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
    """Exits because of a wrong PIN code"""
    print "Error while verifying the PIN code"
    sys.exit()

def printAddress(address, space):
    """Prints some spaces followed by the relative part of an address"""
    length = len(address)
    print space, "[0x%02x%02x]" % (address[length-2], address[length-1])

def printRecordInBinary(response, nb):
    """Prints the content of a record in binary, along with its index"""
    print "====  ", nb, "  ===="
    print "\t", hexListToBinaryString(response), "\n"


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
