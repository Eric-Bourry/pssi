# -*- coding: utf-8 -*-

# -- interpreters.py
# Defines the interpreters

# Lots of things in french, because it is a french card

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


from final_types import FinalType
from stations import *

from datetime import timedelta, date
import structures

globalValues = {}

globalFields = [
    "EventServiceProvider",
    "EventCode"
]

currentStructure = structures.defaultNavigoStructure


def interpretDate(value):
    if len(value)==0:
        return "Empty date"
    try:
        date_int = int(value, 2)
        time_add = timedelta(days=date_int)
        ref = date(1997, 1, 1)
        real_date = ref + time_add
    except:
        return "Incorrect date"
    return str(real_date)

def interpretTime(value):
    time = int(value, 2)
    res = "%02uh%02u" % (int(time/60.0), time % 60)
    return res

def interpretZones(value):
    length = len(value)
    res = ""
    for i in reversed(range(length)):
        if value[i]=='1':
            res += "%u," % (length-i)
    res = res[0:len(res)-1]
    zones = "Zone"
    if len(res) > 1:
        zones += 's'
    zones += ' '
    return zones + res

def interpretApplicationVersionNumber(value):
    intercodeVersion = value[0:3]
    if intercodeVersion == "000":
        res = "Intercode I"
    elif intercodeVersion == "001":
        res = "Intercode II"
    else:
        res = "Unknown"
    res += " - v%u" % (int(value[3:],2))
    return res


def matchWithCode(codes, value):
    # Returns the value associated with a code in a dictionary
    code = int(value, 2)
    if code in codes:
        res = codes[code]
    else:
        res = "Unknown --> %s" % (code)
    return res

def interpretInteger(value):
    """Codage : un entier (décimal)."""
    if len(value)==0:
        return "Empty Integer"
    return str(int(value, 2))

# Codages de la norme
def interpretAmount(value):
    """Codage : Amount. Montants en centimes. (p7)"""
    cents = int(value, 2)
    return "%.2f euros" % (cents/100.0)

def interpretPayMethod(value):
    """Codage : PayMethod. (p6)"""
    codes = { 0x80: "Débit PME",
          0x90: "Espèce",
          0xA0: "Chèque mobilité",
          0xB3: "Carte de paiement",
          0xA4: "Chèque",
          0xA5: "Chèque vacance",
          0xB7: "Télépaiement",
          0xD0: "Télérèglement",
          0xD7: "Bon de caisse, Versement préalable, Bon d’échange, Bon Voyage",
          0xD9: "Bon de réduction" }
    return matchWithCode(codes, value)


# Codage de champs specifiques
def interpretBestContractTariff(value):
    """Champ : BestContractTariff. (p37, p10, p39, p59)"""
    contractKey = value[0:4]
    contractType = value[4:12]
    contractPriority = value[12:16]
    res = "Clé de tri : %s, Type : " % contractKey
    if contractType == '11111111':
        res += "Contract"
    else:
        res += str(int(contractType, 2))
    res += ", Priorité : " + ("%x" % int(contractPriority, 2))
    return res


def interpretSpecialEventSeriousness(value):
    """Champ : SpecialEventSeriousness. (p32)"""
    codes = { 0 : "Aucune sévérité",
          1 : "Événement d’information",
          2 : "Événement de mise en garde",
          3 : "Évènement relatif à une faute" }
    return matchWithCode(codes, value)

def interpretEventCode(value):
    """Champ : EventCode. (p19)"""
    mode = value[0:4]
    transaction = value[4:8]
    modes = { 1 : "Bus urbain",
          2 : "Bus interurbain",
          3 : "Métro",
          4 : "Tram",
          5 : "Train",
          8 : "Parking" }
    transactions = { 0x1 : "Validation en entrée",
             0x2 : "Validation en sortie",
             0x4 : "Contrôle volant (à bord)",
             0x5 : "Validation de test",
             0x6 : "Validation en correspondance (entrée)",
             0x7 : "Validation en correspondance (sortie)",
             0x9 : "Annulation de validation",
             0xD : "Distribution",
             0xF : "Invalidation" }
    res = matchWithCode(modes, mode) + " : " \
        + matchWithCode(transactions, transaction)
    return res

def interpretEventServiceProvider(value):
    """Champ : EventServiceProvider. Pas de table. (p27)"""
    providers = { 2 : "SNCF",
              3 : "RATP",
            115: "CSO (VEOLIA)",
            116: "R'Bus (VEOLIA)",
              156 : "Phébus" }
    return matchWithCode(providers, value)

def interpretEventResult(value):
    """Champ : EventResult. Empirique. (p24 pour SNCF)"""
    # codes metro
    results = { 48 : "Double validation en entrée",
        49 : "Zone invalide",
            53 : "Abonnement périmé",
        69 : "Double validation en sortie"}
    return matchWithCode(results, value)


def interpretRouteNumber(value):
    if not "EventServiceProvider" in globalValues:
        return interpretInteger(value)
    if globalValues["EventServiceProvider"].find("VEOLIA") != -1:
        return interpretInteger(value[0:8])
    elif "EventCode" in globalValues and globalValues["EventCode"].split()[0]=="Train" and int(value, 2)>16:
        return "RER  "+chr(ord('A')+int(value,2)-17)    
    else:
        line = interpretInteger(value)
        if line == "103":
            return "Ligne 3 bis"
        return "Ligne " + line 


def interpretLocationId(value):
    if not "EventCode" in globalValues:
        return "Erreur : impossible de trouver le type de transport"
    transport = globalValues["EventCode"].split()[0]
    if transport == "Métro":
        table = metroStations
    elif transport == "Train":
        table = trainStations
    elif transport == "Bus":
        return interpretInteger(value) 

    else:
        return "L'interprétation des lieux n'est pas encore disponible pour le "+transport

    zone = int(value[0:7], 2)
    location = int(value[7:12], 2)
    code = "%02u-%02u" % (zone, location)
    res = ""
    if not code in table:
        res += code + " (inconnu)"
        return res
    for station in table[code]:
        res += station + ", "
    return res[0:len(res)-2]


def interpretEventDevice(value):
    if (not "EventCode" in globalValues) or (not "EventServiceProvider" in globalValues):
        return interpretInteger(value)
    transport = globalValues["EventCode"].split()[0]
    if (not transport == "Bus") or (not globalValues["EventServiceProvider"]=="RATP"):
        return interpretInteger(value)
    device = int(value[8:],2)
    door = int(device/2.0)+1
    if device%2 == 0:
        side = "droite"
    else:
        side = "gauche"
    res = "Porte %u, validateur de %s" % (door, side)
    return res
    
    
def interpretHolderDataCardStatus(value):
    results = {
        1   : "Navigo découverte",
        2   : "Navigo standard",
        6 : " Navigo intégral",
        14 : "Imagine R (étudiant)"
    }
    return matchWithCode(results, value)
        

def interpretUnknown(value):
    return value


def updateGlobalFields(name, interpretation, type, value):
    if name in globalFields:
        globalValues[name] = interpretation


def parseATR(atrStruct):
    """Parse une partie de l'ATR et affiche quelques paramètres intéressants."""
    global currentStructure
    atr = {}
    historicalBytes = atrStruct.getHistoricalBytes()
    card_number = historicalBytes[11] + (historicalBytes[10] << 8) \
        + (historicalBytes[9] << 16) + (historicalBytes[8] << 24)
    atr["Card number"] = str(card_number)
    chipType = historicalBytes[2]
    atr["Chip type"] = "%02x" % chipType
    applicationType = historicalBytes[3]
    atr["Application type"] =  "%02x" % (applicationType)
    applicationSubtype = historicalBytes[4]
    atr["Application subtype"] =  "%02x" % (applicationSubtype)
    issuer = historicalBytes[5]
    atr["Issuer"] =  "%02x" % (issuer)
    rom = historicalBytes[6]
    atr["ROM"] =  "%02x" % (rom)
    eeprom = historicalBytes[7]
    atr["EEPROM"] =  "%02x" % (eeprom)
    
    currentStructure = structures.cardTypes[atr["Chip type"] + atr["Application type"] + atr["Application subtype"]]
    atr["Card type"] = currentStructure[0]
    
    atr["Keys"] = ["Card number", "Chip type", "Application type", "Application subtype", "Issuer", "ROM", "EEPROM", "Card type"]
    return atr


def hexListToBinaryString(tab):
    """retourne la chaine de la representation binaire de tab"""
    s = ''
    blen = len(tab) * 8
    for b in range(0,blen):
        s = s + "%d" % (((tab[b/8] >> ((7-b)%8))) & 1)
    return s


interpretingFunctions = {
    FinalType.Date: interpretDate,
    FinalType.Time: interpretTime,
    FinalType.Zones: interpretZones,
    FinalType.ApplicationVersionNumber: interpretApplicationVersionNumber,
    FinalType.Amount: interpretAmount,
    FinalType.PayMethod: interpretPayMethod,
    FinalType.BestContractTariff: interpretBestContractTariff,
    FinalType.SpecialEventSeriousness: interpretSpecialEventSeriousness,
    FinalType.EventCode: interpretEventCode,
    FinalType.EventServiceProvider: interpretEventServiceProvider,
    FinalType.EventResult: interpretEventResult,
    FinalType.RouteNumber: interpretRouteNumber,
    FinalType.LocationId: interpretLocationId,
    FinalType.EventDevice: interpretEventDevice,
    FinalType.HolderDataCardStatus: interpretHolderDataCardStatus,

    FinalType.Integer: interpretInteger,

    FinalType.Unknown: interpretUnknown,
        
        
    "ANY": updateGlobalFields,
    "ATR": parseATR,
    "FORMAT": hexListToBinaryString,
    }
