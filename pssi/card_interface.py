# -*- coding: utf-8 -*-

# card.py:
# functions to communicate with a smartcard


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
from smartcard.ATR import ATR
from smartcard.System import readers
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException

import display


apduMode = False
cla = 0
lastRecordSize = 0


def getReadersList():
    try:
        return readers()
    except EstablishContextException:
        return []


def transmitAPDU(connection, apdu):
    global apduMode
    response, sw1, sw2 = connection.transmit(apdu)
    if apduMode: display.printExchange(apdu, response, sw1, sw2)
    return response, sw1, sw2


def sendAPDU(connection, apdu):
    response, sw1, sw2 = transmitAPDU(connection, apdu)
    if statusPinRequired(sw1, sw2):
        pin = display.readPIN()
        pinAPDU = [cla, 0x20, 0, 1, 8] + pin
        response, sw1, sw2 = transmitAPDU(connection, pinAPDU)
        if not statusIsOK(sw1, sw2):
            display.errorPIN()
        response, sw1, sw2 = transmitAPDU(connection, apdu)
    return response, sw1, sw2


def warmResetNeeded(connection):
    global cla
    testAPDU = [cla, 0, 0, 0]
    response, sw1, sw2 = sendAPDU(connection, testAPDU)
    if sw1 == 0x6e:
        return True
    return False


def establishConnection(connection):
    # disposition = 1 = SCARD_RESET_CARD (warm reset)
    connection.connect(disposition=1)
    if warmResetNeeded(connection):
        connection.disconnect()
        connection.connect()
        if apduMode: display.printExchange("reset", getATR(connection), 0x90, 0)

def connectToCard(card):
    try:
        card.connection = card.createConnection()
        establishConnection(card.connection)
        return True
    except (NoCardException, CardConnectionException):
        return False

def connectCard(reader):
    try:
        connection = reader.createConnection()
        establishConnection(connection)
        return connection
    except (NoCardException, CardConnectionException):
        return None

def getCard():
    reader = selectReader()
    if reader is None:
        return None
    card = connectCard(reader)
    if card is None:
        print reader, "--> No card inserted."
    return card

def selectReader():
    """Select a card reader."""
    reader = None
    reader_list = getReadersList()
    if len(reader_list) == 0:
        print "No reader has been found."
    elif len(reader_list) == 1:
        reader = reader_list[0]
    else:
        i = 1
        for reader in reader_list:
            print "%u: %s" % (i, reader)
            i += 1
        choice = raw_input("\nWhich reader do you want to use? ")
        try:
            reader = reader_list[int(choice)-1]
        except:
            print "Please type a correct number"
    return reader


def findEFSize(connection, infoSize):
    global cla
    apdu = [cla, 0xc0, 0, 0, infoSize]
    response, sw1, sw2 = sendAPDU(connection, apdu)
    if not statusIsOK(sw1, sw2):
        return 0
    if len(response) > 14 and response[14] != 0:
        return response[14]
    elif len(response) > 3 and response[3] != 0:
        return response[3]
    return 0


def selectFileByName(connection, name):
    hexName = []
    for c in name:
        hexName.append(ord(c))
    return selectFile(connection, hexName, 0x04)


def selectFile(connection, address, param1 = 0x08, param2 = 0x00):
    """Select a file."""
    global cla
    ins = 0xa4
    addressLen = len(address)
    apdu = [cla, ins, param1, param2, addressLen] + address
    response, sw1, sw2 = sendAPDU(connection, apdu)

    # If we didn't manage to select a file directly with its whole address,
    # we try to do it DF by DF
    if statusBadLength(sw1, sw2) and addressLen > 2:
        numberOfRequests = addressLen / 2
        # first select the right DF
        param1 = 0x01
        for i in range(numberOfRequests):
            if i == numberOfRequests-1:
                # We have the correct DF, now select the EF
                param1 = 0x02
            apdu = [cla, ins, param1, param2, 2] + address[2*i:2*(i+1)]
            response, sw1, sw2 = sendAPDU(connection, apdu)

    size = 0
    if statusHasResponse(sw1, sw2):
        size = findEFSize(connection, sw2)
        if size != 0:
            sw1 = 0x90
            sw2 = 0
    return response, sw1, sw2, size


def readData(connection, size):
    global cla
    apdu = [cla, 0xb0, 0, 0, 0]
    if size == 0:
        good = False
        for size in range(0xff):
            apdu[4] = size
            response, sw1, sw2 = sendAPDU(connection, apdu)
            if statusIsOK(sw1, sw2):
                good = True
            elif good:
                size -= 1
                break

    apdu = [cla, 0xb0, 0, 0, size]
    return sendAPDU(connection, apdu)


def readRecord(connection, number, length=0, mode = 0x04):
    """Reads a record in a selected EF"""
    global cla, lastRecordSize
    ins = 0xb2
    if length == 0:
        length = lastRecordSize
    apdu = [cla, ins, number, mode, length]
    response, sw1, sw2 = sendAPDU(connection, apdu)
    if statusBadLengthWithCorrection(sw1, sw2):
        apdu[4] = sw2
        response, sw1, sw2 = sendAPDU(connection, apdu)
    elif statusBadLength(sw1, sw2):
        if length == 1:
            length = 0x100
        response, sw1, sw2 = readRecord(connection, number, length-1, mode)
    else:
        lastRecordSize = length
    return response, sw1, sw2


def getATR(connection):
    return connection.getATR()

def statusIsOK(sw1, sw2):
    """Return True if the status (sw1, sw2) is OK."""
    return (sw1 == 0x90 and sw2 == 0)

def statusSecurityNotOK(sw1, sw2):
    """Returns True if the security status (sw1, sw2) is not OK."""
    return (sw1 == 0x69 and sw2 == 0x82)

def statusRecordNotFound(sw1, sw2):
    """Returns True if (sw1, sw2) indicates the record is not found."""
    return (sw1 == 0x6a and sw2 == 0x83)

def statusCommandNotAllowed(sw1, sw2):
    """Returns True if (sw1, sw2) indicates the command is not allowed."""
    return (sw1 == 0x69 and sw2 == 0x86)

def statusFileNotFound(sw1, sw2):
    """Returns True if the file was not found."""
    return (sw1 == 0x6a and sw2 == 0x82)

def statusWrongParameters(sw1, sw2):
    """Returns True if the parameters were not correct."""
    return (sw1 == 0x6a and sw2 == 0x86)

def statusBadLength(sw1, sw2):
    """Returns True if the length specified in the read command did
    not match the actual length of the record, and the correct length
    was NOT returned in the response."""
    return sw1 == 0x67 #and sw2==0x00

def statusBadLengthWithCorrection(sw1, sw2):
    """Returns True if the length specified in the read command did
    not match the actual length of the record, and the correct length
    was returned in the response."""
    return sw1 == 0x6c

def statusHasResponse(sw1, sw2):
    """Returns True if the SELECT response provides additional
    information (EF size)."""
    return sw1 == 0x9f

def statusPinRequired(sw1, sw2):
    """Returns True if a PIN authentication is necessary."""
    return sw1 == 0x98 and (sw2 == 0x04 or sw2 == 0x40)
