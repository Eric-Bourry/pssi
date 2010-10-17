# -*- coding: utf-8 -*-


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



import structures
import math

from final_types import FinalType
from codes import MCCs, MNCs

# TODO : rendre les interpréteurs SAFE    

mncBase = ""
tonNPI = 0
dcs = -1
contact = ""
annuaire = {}
smsHeader = False

   
def interpretUnknown(value):
    return interpretHexString(value)
    
    
def interpretHexString(value):
    txt = ""
    for c in value:
        if c == 0xff:
            break
        txt += "%02x" % c
    if len(txt) == 0:
        return "No information"
    return txt
    
    
def interpretRevHexString(value):
    txt = ""
    for c in value:
        if c == 0xff:
                break
        txt += "%1x%1x" % (c%16, c>>4)
    if len(txt) == 0:
        return "No information"
    return txt


def interpretInteger(value):
    n = 0
    for c in value:
        n = n*256 + c
    return str(n)
    
    
def interpretIMSIMCC(value):
    global mncBase
    code = (value[0]>>4)
    code = 10*code + value[1]%16
    code = 10*code + (value[1]>>4)
    mncBase = str(code)+'-'
    # TODO : Ça se passe comment si le MNC est à 3 chiffres ?
    return matchWithIntCode(MCCs, code)
    
    
def interpretPLMNMCC(value):
    global mncBase
    code = interpretRevHexString(value)
    mncBase = code[0:3]+'-'
    if code[3] != 'f': # Le MNC est à 3 chiffres
        mncBase += code[3]
    code = int(code[0:3])
    return matchWithIntCode(MCCs, code)
    
    
def interpretMNC(value):
    global mncBase
    code = mncBase + interpretRevHexString(value)
    return matchWithIntCode(MNCs, code)


def interpretDisplayCondition(value):
    bit = value[0] % 2
    base = "display of registered PLMN "
    if bit == 1:
        return base + "REQUIRED"
    return base + "NOT REQUIRED"
    
def interpretString(value):
    txt = ""
    for c in value:
        if c == 0xff:
            break
        txt += chr(c)
    return txt
    
    
def interpretBinaryString(value):
    txt = ''
    blen = len(value) * 8
    for b in range(0,blen):
        txt = txt + "%d" % (((value[b/8] >> ((7-b)%8))) & 1)
    return txt




locationUpdateStatuses = {
    0:  "updated",
    1:  "not updated",
    2:  "PLMN not allowed",
    3:  "Location Area not allowed",
    7:  "reserved"
}

def interpretLocationUpdateStatus(value):
    code = value[0]%8
    return matchWithIntCode(locationUpdateStatuses, code)
    
    
    
operationModes = {
    0x00:   "Normal operation",
    0x80:   "Type approval operations",
    0x01:   "Normal operation + specific facilities",
    0x81:   "Type approval operations + specific facilities",
    0x02:   "Maintenance (off line)",
    0x04:   "Cell test operation"
}    
    
def interpretOperationMode(value):
    return matchWithIntCode(operationModes, value[0])
 
    
    
phaseValues = {
    0x00:   "Phase 1",
    0x02:   "Phase 2",
}    
    
def interpretPhase(value):
    return matchWithIntCode(phaseValues, value[0])
        

def interpretNumRevHexString(value):
    global tonNPI, contact, annuaire
    txt = interpretRevHexString(value)
    number = ""
    if tonNPI == 0x91:
        number += '+'
    for c in txt:
        if '0' <= c <= '9':
            number += c
        elif c == 'A':
            number += '*'
        elif c == 'B':
            number += '#'
        elif c == 'C':
            number += '-'
        elif c == 'D':
            number += '?'
        else:
            break
            
    if len(number) == 0:
        return "Empty number"
    if number[0] == '+':
        entry = number[3:]
    elif number[0]=='0' and number[1]=='0':
        entry = number[4:]
    else:
        entry = number[1:]
    if len(contact)>0:
        annuaire[entry] = contact
        contact = ""
    else:
        if entry in annuaire:
            number += " (%s)" % annuaire[entry]
    return number
    

def interpretTonNpi(value):
    global tonNPI
    val = value[0]
    npi = val % 16
    ton = (val>>4) % 8
    tonNPI = val
    return "Number Plan Identifier: %u, Type Of Number: %u" % (npi, ton)


SMSStatuses = {
    0: "Free space",
    1: "Message received and read",
    3: "MEssage received but not read yet",
    5: "Message sent",
    7: "Message to be sent"    
}

def interpretSMSStatus(value):
    code = value[0] % 8
    return matchWithIntCode(SMSStatuses, code)


MTIs = {
    0: "SMS‑DELIVER",	
    2: "SMS‑STATUS‑REPORT",	
    1: "SMS‑SUBMIT‑REPORT",
    3: "Reserved"
}

MMSs = {
    0: "More messages left",
    1: "Last message"
}

RPs = {
    0: "No reply path",
    1: "Reply path set"
}

UDHIs = {
    0: "No header",
    1: "Header provided"
}

SRIs = {
    0: "No status report",
    1: "With status report"
}

# TODO : Lequel est le bon ? Le premier est de moi, le deuxième de SIM Reader...
def interpretSMSInfo(value):
    global smsHeader
    code = value[0]
    mti = matchWithIntCode(MTIs, code % 4)
    mms = matchWithIntCode(MMSs, (code>>2) % 2)
    rp = matchWithIntCode(RPs, (code>>7) % 2)
    udhi = matchWithIntCode(UDHIs, (code>>6) % 2)
    if (code>>6) % 2 == 0:
        smsHeader = False
    else:
        smsHeader = True
    sri = matchWithIntCode(SRIs, (code>>5) % 2)
    return "Type: %s, %s, %s, %s, %s" % (mti, mms, rp, udhi, sri)

'''
def interpretSMSInfo(value):
    code = value[0]
    mti = matchWithIntCode(MTIs, (code >> 6) % 4)
    mms = matchWithIntCode(MMSs, (code>>5) % 2)
    rp = matchWithIntCode(RPs, (code>>2) % 2)
    udhi = matchWithIntCode(UDHIs, (code>>3) % 2)
    sri = matchWithIntCode(SRIs, (code>>4) % 2)
    return "Type: %s, %s, %s, %s, %s" % (mti, mms, rp, udhi, sri)
'''    
'''
def interpretNumberLength(value):
    structures.numberLength[0] = value[0]
    return interpretInteger(value)
'''

DCSs = {
    0: "7-bit default alphabet",
    1: "8-bit data",
    2: "16-bit UCS2",
    3: "Unknown alphabet"
}

def interpretDCS(value):
    global dcs
    compressed = False
    dcs = -1
    code = value[0]
    if code>>6 != 0:
        return "No valid interpretation"
    
    if (code>>5 % 2) == 0:
        txt = ", Uncompressed"
    else:
        txt = ", Compressed"
        compressed = True
    
    newDCS = (code>>2) % 4
    if not compressed:
        dcs = newDCS
    return matchWithIntCode(DCSs, newDCS)+txt
    
    
# TODO : ordre d'affichage des infos ?
def interpretTimeStamp(value):
    if value == [0xff]*len(value):
        return ""
    year = interpretRevHexString(value[0:1])
    month = interpretRevHexString(value[1:2])
    day = interpretRevHexString(value[2:3])
    hour = interpretRevHexString(value[3:4])
    minute = interpretRevHexString(value[4:5])
    second = interpretRevHexString(value[5:6])
    
    zone = interpretRevHexString(value[6:7])
    izone = int(zone, 16)
    if izone>>7 == 0:
        sign = '+'
    else:
        sign = '-'
    izone = (izone % 128) / 4
    
    return "%s/%s/%s - %sh%sm%ss  GMT%s%u" % (day, month, year, hour, minute, second, sign, izone)
    
    
ascii7 = u"@£$¥èéùìòÇ\nØø\rÅå∆_ΦΓΛΩΠΨΣΘΞ\x1bæÆßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà"


def interpretASCII7SMS(sms):
    res = ""
    saved = 0
    i = 0
    for c in sms:
        i += 1
        res += ascii7[saved + ((c % (1<<(8-i))) << (i-1))]
        saved = c >> (8-i)
        if i == 7:
            i = 0
            res += ascii7[saved]
            saved = 0
    return res
    
    
def interpretSMS(value):
    global dcs, smsHeader
    if smsHeader:
        return "Not yet able to understand SMS with headers"
    end = len(value)
    if 0xFF in value:
        end = value.index(0xFF)
    sms = value[0:end]
    if dcs == 0:
        return interpretASCII7SMS(sms)
    return "Not yet able to handle this encoding"
        
    
def interpretContact(value):
    global contact
    contact = interpretString(value)
    return contact
    
    
def interpretLength(value):
    length = interpretInteger(value)
    structures.fieldLength[0] = int(length)
    return length
    
    
def interpretSMSLength(value):
    global dcs
    length = interpretInteger(value)
    ilength = int(length)
    if dcs == 0:    # 7-bit encoding
        structures.fieldLength[0] = int(math.ceil(ilength*7/8.))
    else:
        structures.fieldLength[0] = ilength
    return length


def interpretNumberLengthBytes(value):
    if value[0] == 0xff:
        structures.fieldLength[0] = 1
        return ""
    value[0] -= 1
    return interpretLength(value)
    
    
def interpretNumberLengthDigits(value):
    if value[0] == 0xff:
        structures.fieldLength[0] = 1
        return ""
    value[0] = int(math.ceil(value[0]/2.))
    return interpretLength(value)


interpretingFunctions = {
    FinalType.RevHexString: interpretRevHexString,
    FinalType.HexString: interpretHexString,
    FinalType.Integer: interpretInteger,
    FinalType.IMSIMCC: interpretIMSIMCC,
    FinalType.PLMNMCC: interpretPLMNMCC,
    FinalType.MNC: interpretMNC,
    FinalType.DisplayCondition: interpretDisplayCondition,
    FinalType.String: interpretString,
    FinalType.BinaryString: interpretBinaryString,
    FinalType.LocationUpdateStatus: interpretLocationUpdateStatus,
    FinalType.OperationMode: interpretOperationMode,
    FinalType.Phase: interpretPhase,
    FinalType.NumRevHexString: interpretNumRevHexString,
    FinalType.TonNpi: interpretTonNpi,
    FinalType.SMSStatus: interpretSMSStatus,
    FinalType.SMSInfo: interpretSMSInfo,
   # FinalType.NumberLength: interpretNumberLength,
    FinalType.DCS: interpretDCS,
    FinalType.TimeStamp: interpretTimeStamp,
    FinalType.SMS: interpretSMS,
    FinalType.Contact: interpretContact,
    FinalType.Length: interpretLength,
    FinalType.SMSLength: interpretSMSLength,
    FinalType.NumberLengthBytes: interpretNumberLengthBytes,
    FinalType.NumberLengthDigits: interpretNumberLengthDigits,
    
    FinalType.Unknown: interpretUnknown,
}


def matchWithIntCode(codes, code):
    """Renvoie la valeur associée à un code.
    `codes' est un dictionnaire, les clés sont les codes entiers,
    `value' est une clé potentielle en binaire."""
    if code in codes:
        res = codes[code]
    else:
        res = "Inconnu --> %s" % (code)
    return res

