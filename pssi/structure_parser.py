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
from field_types import FieldType

from smartcard.util import toHexString
from smartcard.ATR import ATR
import types


MAX_RECORDS = 1000


def interpretFinalField(value, type, name):
    interpreterTable = plugin.getInterpretersTable()
    interpretation = interpreterTable[type](value)
    if "ANY" in interpreterTable:
        interpreterTable["ANY"](name, interpretation, type, value)
    return interpretation


class IncorrectStructure():
    def __init__(self):
        return

    def __str__(self):
        print(": ","Tried to parse a binary string with an incorrect structure")


class notTLVRecord(BaseException):
    def __init__(self, data):
        self.data = data
        return

    def __str__(self):
        print(": ","The following record isn't in the TLV format: ", data)


def parseTLV(data):
    typeTable = plugin.getInterpretersTable()
    table = {}
    keys = []
    while len(data) > 0:
        cur_type = data[0]
        data = data[1:]
        
        # if the 5 last bits are 1, the tag is 2-byte-long
        if cur_type%32 == 31 and len(data)>0:
            cur_type = cur_type*256 + data[0]
            data = data[1:]

        # when the length is between 127 and 255 bytes, it is coded on two bytes. 
        # The first byte has a constant hexadecimal value ‘81’, while the second byte 
        # is the actual length in hexadecimal.
        if len(data)>0 and data[0] == 0x81: 
            data = data[1:]
            
        try:
            length = data[0]
            value = data[1:1+length]
            data = data[1+length:]
            assert len(value)==length
        except: #not TLV
            raise notTLVRecord(data)
        if not cur_type in typeTable:
            continue
        info = typeTable[cur_type]          
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
        data, sw1, sw2 = readRecord(connection, 1, 0, mode)
        if not statusFileNotFound(sw1, sw2):
            return mode
    return -1


# TODO: sizeParsed isn't always correct, in the TLV case for instance
def parseCardStruct(connection, structure, data=[], sizeParsed=[], defaultStruct=[]):
    table = {}
    keys = []
    total = 0
    while (structure != []):
        
        if structure == -1: # TLV
            structure = []
            mode = findReadRecordMode(connection)
            fileCounter = 0
            while mode != -1:
                entry = {}
                subkeys = []
                for number in range(1, MAX_RECORDS+1):
                    cardData, sw1, sw2 = readRecord(connection, number, 0, mode)
                    if len(cardData)>0:
                        try:
                            entry[number] = parseTLV(cardData)
                        except notTLVRecord:
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
            if type(name) == list:
                hiddenFields = True
            else:
                hiddenFields = False
            structure = structure[1:]

            if field[1] == FieldType.Bitmap:
                if not (type(data) is bytes):
                    data = display.hexListToBinaryString(data)
                for bit in data:
                    if bit != '0' and bit != '1':
                        raise IncorrectStructure
                length = field[2]
                bitmap = data[0:length]
                
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
                for i in range(int(datalen/length)):
                    if data[i*length: (i+1)*length] == [0xff]*length:
                        break
                    subfields.append( ("%s %u" % (field[0], i+1), FieldType.Final, field[2], field[3], field[4]) )
                structure = subfields + structure

            elif field[1] == FieldType.StructRepeated:
                length = field[2]
                datalen = len(data)
                number = 0
                for i in range(datalen/length):
                    if data[i*length: (i+1)*length] == [0xff]*length:
                        break
                    number += 1
                field = [(field[0], FieldType.Counter, 1, field[3])]
                data = [number] + data
                structure = field + structure

            
            elif field[1] == FieldType.ReversedStructRepeated:
                length = field[2]
                datalen = len(data)
                newdata = []
                for i in reversed(list(range(datalen/length))):
                    newdata += data[i*length: (i+1)*length]
                data = newdata
                structure = [(field[0], FieldType.StructRepeated, field[2], field[3])] + structure


            else:
                entry = None
                if field[1] == FieldType.DF:
                    entry = parseCardStruct(connection, field[3], data+field[2])
                elif field[1] == FieldType.DFName:
                    selectFileByName(connection, field[2])
                    entry = parseCardStruct(connection, field[3],[])
                elif field[1] == FieldType.DFList:
                    entry = {}
                    subkeys = []
                    for addr in field[2]:
                        selectFile(connection, addr, 0x04)
                        addr= toHexString(addr)
                        subkeys.append(addr)
                        
                        if len(field)>4:
                            defaultStruct = field[4]
                        entry[addr] = parseCardStruct(connection, field[3], [], sizeParsed, defaultStruct)
                    entry["Keys"] = subkeys


                elif field[1] == FieldType.TransparentEF:
                    (response, sw1, sw2, size) = selectFile(connection, data+field[2])
                    if not statusIsOK(sw1, sw2): 
                        entry = "File not found"
                    else:
                        hexdata, sw1, sw2 = readData(connection, size)
                        entry = parseCardStruct(connection, field[3], hexdata)


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
                        for number in range(1, MAX_RECORDS+1):
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
                    
                    if type(data) is bytes:
                        counter = int(data[0:length], 2)
                    else:
                        counter = data[0] 
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
                elif field[1] == FieldType.Final or field[1] == FieldType.FinalWithHeader:
                    value = None
                    if field[1] == FieldType.Final:
                        length = field[2]
                        description = field[3]
                        finalType = field[4]
                    elif field[1] == FieldType.FinalWithHeader:
                        headerLength = field[2]
                        header = data[0:headerLength]
                        data = data[headerLength:]
                        length = header[field[3]]
                        description = field[4]
                        finalType = field[5]
                    if type(length) is list:
                        length = length[0]
                    if length != 0:
                        value = data[0:length]
                        data = data[length:]
                        total += length
                    elif field[1] == FieldType.Final:
                        value = data
                        data = []
                        total += len(value)       
                    
                    if value is not None:
                        interpretation = interpretFinalField(value, finalType, name)
                        if type(value) is list:
                            value = toHexString(value)
                        entry = display.formatOutput(interpretation, value, description)
                    else:
                        entry = display.formatOutput("", "", description)

                if entry is not None:
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
