# -*- coding: utf-8 -*-

# -- card_parser.py
# Defines the parsing functions


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



import plugin
import display
from card_interface import *

from smartcard.util import toHexString
from smartcard.ATR import ATR
import types
import exceptions


MAX_RECORDS = 1000


class FieldType:
    DF = 0.1
    RecordEF = 0.2
    Bitmap = 0.3
    Final = 0.4
    Counter = 0.5
    DFName = 0.6
    DFList = 0.7
    TransparentEF = 0.8
    FinalRepeated = 0.9
    StructRepeated = 0.01
    ReversedStructRepeated = 0.02


def interpretFinalField(value, type, name):
    #print "Interpret", value, type, name
    interpreterTable = plugin.getInterpretersTable()
    interpretation = interpreterTable[type](value)
    if "ANY" in interpreterTable:
        interpreterTable["ANY"](name, interpretation, type, value)
    return interpretation


class IncorrectStructure(exceptions.Exception):
    def __init__(self):
        return

    def __str__(self):
        print ": ","Tried to parse a binary string with an incorrect structure"


class notTLVRecord(exceptions.Exception):
    def __init__(self, data):
        self.data = data
        return

    def __str__(self):
        print ": ","The following record isn't in the TLV format: ", data


def parseTLV(data):
    typeTable = plugin.getInterpretersTable()
    table = {}
    keys = []
    while len(data) > 0:
        #        print data
        cur_type = data[0]
        data = data[1:]
        if cur_type%32 == 31 and len(data)>0: #TODO(e) : Vérifier 5
                                          #derniers bits à 1 =? multi
                                          #byte tag
            cur_type = cur_type*256 + data[0]
            data = data[1:]

        if data[0] == 0x81 and len(data)>0: # TODO(e): Pourquoi ?
            data = data[1:]
        try:
            length = data[0]
            #print length
            value = data[1:1+length]
            #print value
            data = data[1+length:]
            #print data
            assert len(value)==length
            #print data
            #print ""
        except: #not TLV
            #print data
            raise notTLVRecord(data)
        if not cur_type in typeTable:
            continue
        info = typeTable[cur_type]          # TODO(e): Faire une fonction interpret
        name = info[0]
        interpreter = info[1]
        keys.append(name)
        if interpreter == -1:
            table[name] = parseTLV(value)
        else:
            if "FORMAT" in typeTable:
                value = typeTable["FORMAT"](value)
            table[name] = interpreter(value)
    table["Keys"] = keys
    return table


def findReadRecordMode(connection, begin=4):
    for left in range(1 + ((begin-4) >> 3), 2**5):
        mode = (left<<3) + 4
        #print left, mode
        data, sw1, sw2 = readRecord(connection, 1, 0, mode)
        if not statusFileNotFound(sw1, sw2):
            return mode
    return -1

# TODO : MAJ sizeParsed ?
def parseCardStruct(connection, structure, data=[], sizeParsed=[], defaultStruct=[]):
    table = {}
    keys = []
    total = 0
    while (structure != []):
        #print structure
        #print table
        #print ""

        # TODO : maj total
        if structure == -1: #TLV !
            # TODO : Le faire sans bruteforce
            structure = []
            mode = findReadRecordMode(connection)
            fileCounter = 0
            while mode != -1:
                entry = {}
                subkeys = []
                for number in range(1, MAX_RECORDS):
                    cardData, sw1, sw2 = readRecord(connection, number, 0, mode)
                    if len(cardData)>0:
                        try:
                            entry[number] = parseTLV(cardData)
                        except notTLVRecord:
                            '''
                            interpretersTable = plugin.getInterpretersTable()
                            if "default" in plugin.getInterpretersTable():
                                entry[number] = interpretersTable["default"](data)
                            else:
                                entry[number] = "No interpreter found for this NOT TLV field"
                            '''
                            # TODO : if defaultStruct !- [] ?
                            entry[number] = parseCardStruct(connection, defaultStruct, cardData, sizeParsed, defaultStruct)
                        subkeys.append(number)
                    else:
                        break
                mode = findReadRecordMode(connection, mode)
                fileCounter += 1
                entry["Keys"] = subkeys
                keys.append(fileCounter)
                table[fileCounter] = entry



        else:
            field = structure[0]
            name = field[0]
            if type(name) == types.ListType:
                hiddenFields = True
            else:
                hiddenFields = False
            structure = structure[1:]

            if field[1] == FieldType.Bitmap:
                # TODO : check si c'est bien des 0 et des 1
                if not (type(data) is types.StringType):
                    data = display.hexListToBinaryString(data)
                length = field[2]
                bitmap = data[0:length]
                #print bitmap
                data = data[length:]
                total += length
                counter = 0
                subfields = []
                for subfield in field[3]:
                    try:
                        if bitmap[len(bitmap)-counter-1] == '1':
                            subfields.append(subfield)
                    except IndexError:
                        raise IncorrectStructure
                    counter += 1
                structure = subfields + structure


            elif field[1] == FieldType.FinalRepeated:
                length = field[2]
                datalen = len(data)
                subfields = []
                for i in range(datalen/length):
                    if data[i*length: (i+1)*length] == [0xff]*length:    # TODO : faire avec des strings
                        break
                    subfields.append( ("%s %u" % (field[0], i+1), FieldType.Final, field[2], field[3], field[4]) )
                structure = subfields + structure

            elif field[1] == FieldType.StructRepeated:
                #print data
                length = field[2]
                datalen = len(data)
                number = 0
                for i in range(datalen/length):
                    #print i,number, length
                    #print toHexString(data[i*number: i*number+length])
                    if data[i*length: (i+1)*length] == [0xff]*length:    # TODO : faire avec des strings
                        break
                    number += 1
                field = [(field[0], FieldType.Counter, 1, field[3])]
                data = [number] + data
                structure = field + structure
                #print structure

            # TODO : regrouper avec le cas précédent ? faire un reverse d'autres cas ?
            elif field[1] == FieldType.ReversedStructRepeated:
                length = field[2]
                datalen = len(data)
                newdata = []
                for i in reversed(range(datalen/length)):
                    newdata += data[i*length: (i+1)*length]
                data = newdata
                #print data, newdata
                structure = [(field[0], FieldType.StructRepeated, field[2], field[3])] + structure


            else:
                if field[1] == FieldType.DF:
                    entry = parseCardStruct(connection, field[3], data+field[2])
                elif field[1] == FieldType.DFName:
                    # TODO : Check error
                    selectFileByName(connection, field[2])
                    entry = parseCardStruct(connection, field[3],[])
                elif field[1] == FieldType.DFList:
                    entry = {}
                    subkeys = []
                    for addr in field[2]:
                        selectFile(connection, addr, 0x04)
                        addr= toHexString(addr)
                        subkeys.append(addr)
                        # TODO : le faire dans les autres cas, style DFName
                        if len(field)>4:
                            defaultStruct = field[4]
                        entry[addr] = parseCardStruct(connection, field[3], [], sizeParsed, defaultStruct)
                    entry["Keys"] = subkeys


                elif field[1] == FieldType.TransparentEF:
                    (response, sw1, sw2, size) = selectFile(connection, data+field[2])
                    # TODO : code d'erreur ?
                    #try:
                    #    size = findTransparentEFSize(connection, sw2)
                    #except:
                    #    entry = "File not found"
                    if not statusIsOK(sw1, sw2): # or size == 0:
                        entry = "File not found"
                    else:
                        hexdata, sw1, sw2 = readData(connection, size)
                        entry = parseCardStruct(connection, field[3], hexdata)


                # TODO : Quand est-on en binaire ou en hexa ?
                elif field[1] == FieldType.RecordEF:
                    (response, sw1, sw2, size) = selectFile(connection, data+field[2])
                    if not statusIsOK(sw1, sw2):
                        entry = "Could not select the file in order to fetch the data"
                    else:
                        if hiddenFields:
                            newSizeParsed = []
                            entry = []
                            for i in range(len(name)):
                                entry.append({})
                        else:
                            entry = {}
                        subkeys = []
                        for number in range(1, MAX_RECORDS):
                            cardData, sw1, sw2 = readRecord(connection, number, size)
                            if len(cardData) > 0:
                                if cardData == [0xff]*len(cardData):
                                    continue
                                interpreterTable = plugin.getInterpretersTable()
                                if "FORMAT" in interpreterTable:
                                    cardData = interpreterTable["FORMAT"](cardData)
                                if hiddenFields:
                                    counter = 0
                                    for struct in field[3]:
                                        entry[counter][number] = parseCardStruct(connection, struct, cardData, newSizeParsed)
                                        cardData = cardData[newSizeParsed[0]:]
                                        counter += 1
                                else:
                                    entry[number] = parseCardStruct(connection, field[3], cardData)
                                subkeys.append(number)
                            else:
                                break

                        if hiddenFields:
                            for i in range(len(name)):
                                entry[i]["Keys"] = subkeys
                        else:
                            entry["Keys"] = subkeys
                elif field[1] == FieldType.Counter:
                    length = field[2]
                    # TODO : bof, faire une fonction qui virifie si c'est du binaire ?
                    if type(data) is types.StringType:
                        counter = int(data[0:length], 2)
                    else:
                        counter = data[0] # TODO : data sur plusieurs octets
                    data = data[length:]
                    total += length
                    entry = {}
                    subkeys = []
                    for number in range(counter):
                        size = []
                        entry[number] = parseCardStruct(connection, field[3], data, size)
                        subkeys.append(number)
                        data = data[size[0]:]
                    entry["Keys"] = subkeys
                elif field[1] == FieldType.Final:
                    length = field[2]
                    if type(length) is types.ListType:
                        length = length[0]
                    if length != 0:
                        #print length
                        value = data[0:length]
                        data = data[length:]
                        total += length
                    else:
                        value = data
                        data = []
                        total += len(value)
                    #print value
                    interpretation = interpretFinalField(value, field[4], name)
                    # TODO : beurk
                    if type(value) is types.ListType:
                        value = toHexString(value)
                    entry = display.formatOutput(interpretation, value, field[3])

                if hiddenFields:
                    counter = 0
                    for subname in name:
                        table[subname] = entry[counter]
                        keys.append(subname)
                        counter += 1
                else:
                    table[name] = entry
                    keys.append(name)

    sizeParsed.append(total)
    table["Keys"] = keys
    #print table
    return table



def parseCard(connection):
    card = {}
    if "ATR" in plugin.getInterpretersTable():
        card["ATR"] = plugin.getInterpretersTable()["ATR"](ATR(getATR(connection)))
    else:
        card["ATR"] = toHexString(getATR(connection))
    card["Content"] = parseCardStruct(connection, plugin.getRootStructure())
    card["Keys"] = ["ATR", "Content"]
    return card
