# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures

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