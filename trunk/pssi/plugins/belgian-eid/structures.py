# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures


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


from field_types import FieldType
from final_types import FinalType

structID = [
    ("Card Number", FieldType.FinalWithHeader, 2, 1, "", FinalType.CardNumber),
    ("Chip Number", FieldType.FinalWithHeader, 2, 1, "", FinalType.HexString),
    ("Card validity date begin", FieldType.FinalWithHeader, 2, 1, "DD.MM.YYYY", FinalType.String),
    ("Card validity date end", FieldType.FinalWithHeader, 2, 1, "DD.MM.YYYY", FinalType.String),
    ("Card delivery municipality", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("National Number", FieldType.FinalWithHeader, 2, 1, "", FinalType.NationalNumber),
    ("Name", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("2 first given names", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("First letter of 3rd given names", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("Nationality", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("Birth location", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("Birth date", FieldType.FinalWithHeader, 2, 1, "DD mmmm YYYY or DD.mmm.YYYY (German)", FinalType.String),
    ("Sex", FieldType.FinalWithHeader, 2, 1, "", FinalType.Sex),
    ("Noble condition", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("Document type", FieldType.FinalWithHeader, 2, 1, "", FinalType.DocumentType),
    ("Special status", FieldType.FinalWithHeader, 2, 1, "", FinalType.SpecialStatus),
    ("Hash photo", FieldType.FinalWithHeader, 2, 1, "SHA-1", FinalType.HexString)
]

structAddress = [
    ("Street + number", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("ZIP code", FieldType.FinalWithHeader, 2, 1, "", FinalType.String),
    ("Municipality", FieldType.FinalWithHeader, 2, 1, "", FinalType.String)
]

structDFID = [
    ("ID", FieldType.TransparentEF, [0x40, 0x31], structID),
    ("Address", FieldType.TransparentEF, [0x40, 0x33], structAddress)
]

structBEID = [
    ("DF ID", FieldType.DF, [0xdf, 0x01], structDFID)
]
