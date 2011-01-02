# -*- coding: utf-8 -*-

# -- interpreters.py
# Defines the interpreters


# Copyright © 2010, 2011 Laurent Léonard

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


from final_types import FinalType

def interpretHexString(value):
    return "".join(["%02x" % c for c in value])

def interpretString(value):
    return "".join([chr(c) for c in value])

def interpretCardNumber(value):
    s = interpretString(value)
    return s[:3] + '-' + s[3:10] + '-' + s[10:]

def interpretNationalNumber(value):
    s = interpretString(value)
    return s[:2] + '.' + s[2:4] + '.' + s[4:6] + '-' + s[6:9] + '.' + s[9:]

Sex = {
    "F": "Woman",
    "M": "Man",
    "V": "Woman",
    "W": "Woman"
}

def interpretSex(value):
    return matchWithCode(Sex, chr(value[0]))

DocumentType = {
    1: "Belgian citizen",
    2: "European Community citizen",
    3: "Non European Community citizen",
    7: "Bootstrap card",
    8: "“Habilitation/machtigings” card"
}

def interpretDocumentType(value):
    return matchWithCode(DocumentType, int(interpretString(value)))

SpecialStatus = {
    0: "No status",
    1: "White cane (blind people)",
    2: "Extended minority",
    3: "White cane + extended minority",
    4: "Yellow cane (partially sighted people)",
    5: "Yellow cane + extended minority"
}

def interpretSpecialStatus(value):
    return matchWithCode(SpecialStatus, int(interpretString(value)))

def interpretUnknown(value):
    return value

interpretingFunctions = {
    FinalType.HexString: interpretHexString,
    FinalType.String: interpretString,
    FinalType.CardNumber: interpretCardNumber,
    FinalType.NationalNumber: interpretNationalNumber,
    FinalType.Sex: interpretSex,
    FinalType.DocumentType: interpretDocumentType,
    FinalType.SpecialStatus: interpretSpecialStatus,
    
    FinalType.Unknown: interpretUnknown
}

def matchWithCode(codes, code):
    # Returns the value associated with a code in a dictionary
    if code in codes:
        res = codes[code]
    else:
        res = "Unknown --> %s" % (code)
    return res
