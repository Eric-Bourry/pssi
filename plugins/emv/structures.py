# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures


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



from final_types import FinalType, FieldType

aidList = []

structPayment = [
    ("Amount", FieldType.Final, 6, "", FinalType.Amount),
    ("CID", FieldType.Final, 1, "Cryptogram Information Data", FinalType.Integer),
    ("Country", FieldType.Final, 2, "Country where the terminal is located", FinalType.Country),
    ("Currency", FieldType.Final, 2, "", FinalType.Currency),
    ("Date", FieldType.Final, 3, "", FinalType.Date),
    ("Type", FieldType.Final, 1, "", FinalType.TransactionType),
]

structEMV = [
    ("Applications List", FieldType.DFName, "1PAY.SYS.DDF01", -1),
    ("Applications", FieldType.DFList, aidList, -1, structPayment)
]