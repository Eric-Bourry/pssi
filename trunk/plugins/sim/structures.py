# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures

from final_types import FinalType, FieldType

fieldLength = [0]


structICC = [
    ("ID number", FieldType.Final, 10, "Card identification number", FinalType.RevHexString)
]


structLP = [
    ("Language code", FieldType.FinalRepeated, 1, "", FinalType.Integer)
]


structIMSI = [
    ("IMSI length", FieldType.Final, 1, "", FinalType.Integer),
    ("MCC", FieldType.Final, 2, "Mobile Country Code", FinalType.IMSIMCC),
    ("MNC", FieldType.Final, 1, "Mobile Network Code", FinalType.MNC),
    ("HLR number", FieldType.Final, 1, "Home Location Register number", FinalType.RevHexString),
    ("MSIN", FieldType.Final, 4, "Mobile Subscriber Identification Number", FinalType.RevHexString),
]


structKc = [
    ("Key", FieldType.Final, 8, "Ciphering key Kc", FinalType.HexString),
    ("Sequence number", FieldType.Final, 1, "Ciphering key sequence number", FinalType.Integer)
]


structPLMN = [
    ("MCC", FieldType.Final, 2, "Mobile Country Code", FinalType.PLMNMCC),
    ("MNC", FieldType.Final, 1, "Mobile Network Code", FinalType.MNC),
]

# Public Land Mobile Network
structPLMNsel = [
    ("Prefered PLMN (Public Land Mobile Network) list", FieldType.StructRepeated, 3, structPLMN)
]


# TODO : valeur de N ?
structHPLMN = [
    ("Home PLMN search period", FieldType.Final, 1, "Interval of time between searches for the HPLMN, in interger multiple of N minutes", FinalType.Integer),
]

structACMmax = [
    ("ACM max value", FieldType.Final, 3, "maximum value of the Accumulated Call Meter", FinalType.Integer),
]

structACM = [
    ("ACM value", FieldType.Final, 3, "value of the Accumulated Call Meter", FinalType.Integer),
]

structGID = [
    ("GID", FieldType.FinalRepeated, 1, "Group Identifier", FinalType.Integer),
]

structSPN = [
    ("Display condition", FieldType.Final, 1, "", FinalType.DisplayCondition),
    ("SPN", FieldType.Final, 16, "Service Provider Name", FinalType.String),
]

structPUCT = [
    ("Cuurency code", FieldType.Final, 3, "", FinalType.Integer),
    ("PPU", FieldType.Final, 2, "Price per unit", FinalType.Integer),
]

structCBMI = [
    ("CBMI", FieldType.FinalRepeated, 2, "Cell Broadcast Message Identifier", FinalType.HexString),
]

structBCCH = [
    ("BCCH information", FieldType.Final, 16, "Broadcast Control CHannel", FinalType.HexString),
]

structACC = [
    ("Access control classes", FieldType.Final, 2, "", FinalType.BinaryString),
]

structForbiddenPLMN = [
    ("Forbidden PLMN (Public Land Mobile Network) list", FieldType.ReversedStructRepeated, 3, structPLMN)
]

structLOCI = [
    ("TMSI", FieldType.Final, 4, "Temporary Mobile Subscriber Identity", FinalType.HexString),
    #("LAI", FieldType.Final, 5, "Location Area Information", FinalType.Integer),
    ("MCC", FieldType.Final, 2, "Mobile Country Code", FinalType.PLMNMCC),
    ("MNC", FieldType.Final, 1, "Mobile Network Code", FinalType.MNC),
    ("LAC", FieldType.Final, 2, "", FinalType.HexString),   # TODO : C'est quoi ?
    ("TMSI time", FieldType.Final, 1, "Current value of Periodic Location Updating Timer", FinalType.Integer),
    ("Location update status", FieldType.Final, 1, "", FinalType.LocationUpdateStatus),
]

structAD = [
    ("MS operation mode", FieldType.Final, 1, "", FinalType.OperationMode),
    # TODO : Incomplet ? Le reste des valeurs est manufacturer specific...
]

structPhase = [
    ("SIM Phase", FieldType.Final, 1, "", FinalType.Phase),
]

structGSM = [
    ("Language preference", FieldType.TransparentEF, [0x6f, 0x05], structLP),
    ("IMSI", FieldType.TransparentEF, [0x6f, 0x07], structIMSI),
    ("Kc", FieldType.TransparentEF, [0x6f, 0x20], structKc),
    ("PLMN selector", FieldType.TransparentEF, [0x6f, 0x30], structPLMNsel),
    ("HPLMN search period", FieldType.TransparentEF, [0x6f, 0x31], structHPLMN),
    ("ACM max", FieldType.TransparentEF, [0x6f, 0x37], structACMmax), # TODO : a tester, je ne l'ai pas
    # TODO : EFsst = sim service table
    ("ACM", FieldType.TransparentEF, [0x6f, 0x39], structACM),  # TODO : a tester, je ne l'ai pas
    ("Group Identifier level 1", FieldType.TransparentEF, [0x6f, 0x3e], structGID),
    ("Group Identifier level 2", FieldType.TransparentEF, [0x6f, 0x3f], structGID),
    ("SPN", FieldType.TransparentEF, [0x6f, 0x46], structSPN),
    ("PUCT", FieldType.TransparentEF, [0x6f, 0x41], structPUCT), # TODO : Pas la bonne structure, je ne l'ai pas sur mon tel
    ("CBMI", FieldType.TransparentEF, [0x6f, 0x45], structCBMI),
    ("BCCH", FieldType.TransparentEF, [0x6f, 0x74], structBCCH),  # TODO : page 260 de 0408_4n1.doc
    ("ACC", FieldType.TransparentEF, [0x6f, 0x78], structACC),
    ("FPLMN", FieldType.TransparentEF, [0x6f, 0x7b], structForbiddenPLMN),
    ("Location information", FieldType.TransparentEF, [0x6f, 0x7e], structLOCI),
    ("Administrative data", FieldType.TransparentEF, [0x6f, 0xad], structAD),
    ("Phase identification", FieldType.TransparentEF, [0x6f, 0xae], structPhase),
]




#################################################################

structNumber = [
    ("Alpha identifier", FieldType.Final, -14, "Name of the contact", FinalType.Contact),
    ("Length of relevant information", FieldType.Final, 1, "In bytes", FinalType.Integer),
    ("TON and NPI", FieldType.Final, 1, "", FinalType.TonNpi),
    ("Dialling number", FieldType.Final, 10, "Telephone number of the contact", FinalType.NumRevHexString),
    ("Capability/Configuration identifier", FieldType.Final, 1, "", FinalType.Integer),
    ("Extension1 record identifier", FieldType.Final, 1, "", FinalType.Integer),
]


structSMS = [
    ("Status", FieldType.Final, 1, "", FinalType.SMSStatus),
    ("SMSC number length", FieldType.Final, 1, "In bytes", FinalType.NumberLengthBytes),
    ("SMSC TON and NPI", FieldType.Final, 1, "", FinalType.TonNpi),
    ("SMSC number", FieldType.Final, fieldLength, "Telephone number of SMS Center", FinalType.NumRevHexString),
    ("Information", FieldType.Final, 1, "", FinalType.SMSInfo),
    ("Sender number length", FieldType.Final, 1, "In bytes", FinalType.NumberLengthDigits),
    ("Sender TON and NPI", FieldType.Final, 1, "", FinalType.TonNpi),
    ("Sender number", FieldType.Final, fieldLength, "Telephone number of the sender", FinalType.NumRevHexString),

    # TODO : Meilleure interprétation ?
    ("Protocol Identifier", FieldType.Final, 1, "", FinalType.Integer),

    ("Data Coding Scheme", FieldType.Final, 1, "", FinalType.DCS),
    ("Timestamp", FieldType.Final, 7, "Date and time when the message was sent", FinalType.TimeStamp),
    ("User data length", FieldType.Final, 1, "", FinalType.SMSLength),
    ("SMS", FieldType.Final, fieldLength, "", FinalType.SMS),
]

# TODO : incomplet
structDFTel = [
    ("Abbreviated dialling numbers", FieldType.RecordEF, [0x6f, 0x3a], structNumber),
    ("Fixed dialling numbers", FieldType.RecordEF, [0x6f, 0x3b], structNumber),
    ("SMS (Short messages)", FieldType.RecordEF, [0x6f, 0x3c], structSMS),
    ("Mobile Station international ISDN numbers", FieldType.RecordEF, [0x6f, 0x40], structNumber),
    ("Last numbers dialled", FieldType.RecordEF, [0x6f, 0x44], structNumber),
]


#####################################################################

structSIM = [
    ("ICC identification", FieldType.TransparentEF, [0x2f, 0xe2], structICC),
    ("DF GSM", FieldType.DF, [0x7f, 0x20], structGSM),
    ("DF Télécom", FieldType.DF, [0x7f, 0x10], structDFTel),
]
