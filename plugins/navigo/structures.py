# -*- coding: utf-8 -*-

# -- structures.py
# Defines the different structures

from final_types import FinalType, FieldType

structEnv = [
    ("EnvApplicationVersionNumber", FieldType.Final, 6, "Numéro de version de l’application Billettique", FinalType.ApplicationVersionNumber),
    ("Bitmap générale", FieldType.Bitmap, 7,
    [
        ("EnvNetworkId", FieldType.Final, 24, "Identification du réseau", FinalType.Integer),
        ("EnvApplicationIssuerId", FieldType.Final, 8, "Identification de l’émetteur et créateur de l’application Billettique", FinalType.Integer),
        ("EnvApplicationValidityEndDate", FieldType.Final, 14, "Date de fin de validité de l’application Billettique", FinalType.Date),
        ("EnvPayMethod", FieldType.Final, 11, "", FinalType.PayMethod),
        ("EnvAuthenticator", FieldType.Final, 16, "", FinalType.Integer),
        ("EnvSelectList", FieldType.Final, 32, "Bitmap de tableau de paramètre multiple", FinalType.Unknown),
        ("EnvData", FieldType.Bitmap, 2,
        [
            ("EnvDataCardStatus", FieldType.Final, 1, "Statut de la carte", FinalType.Unknown),
            ("EnvData2", FieldType.Final, 0, "Données supplémentaires", FinalType.Unknown)
        ])
    ])
]

structHolder = [
    ("Bitmap générale", FieldType.Bitmap, 8,
    [
        ("HolderName", FieldType.Bitmap, 2,
        [
            ("HolderSurname", FieldType.Final, 85, "Nom du porteur", FinalType.Unknown),
            ("HolderForename", FieldType.Final, 85, "Prénom de naissance du porteur", FinalType.Unknown),
        ]),
        ("HolderBirth", FieldType.Bitmap, 2,
        [
            ("HolderBirthDate", FieldType.Final, 32, "Date de naissance", FinalType.Date),
            ("HolderBirthPlace", FieldType.Final, 115, "Lieu de naissance (23 caractères)", FinalType.Unknown),
        ]),
        ("HolderBirthName", FieldType.Final, 85, "Nom de naissance du porteur (17 caractères)", FinalType.Unknown),
        ("HolderIdNumber", FieldType.Final, 32, "Identifiant Porteur", FinalType.Integer),
        ("HolderCountryAlpha", FieldType.Final, 24, "Pays du titulaire", FinalType.Unknown),
        ("HolderCompany", FieldType.Final, 32, "Société du titulaire", FinalType.Unknown),
        ("HolderProfiles", FieldType.Counter, 4,
        [
            ("HolderProfileBitmap", FieldType.Bitmap, 3,
            [
                ("HolderNetworkId", FieldType.Final, 24, "Réseau", FinalType.Unknown),
                ("HolderProfileNumber", FieldType.Final, 8, "Numéro du statut", FinalType.Integer),
                ("HolderProfileDate", FieldType.Final, 14, "Date de fin de validité du statut", FinalType.Date),
            ])
        ]),
        ("HolderData", FieldType.Bitmap, 12,
        [
            ("HolderDataCardStatus", FieldType.Final, 4, "Type de carte", FinalType.HolderDataCardStatus),
            ("HolderDataTeleReglement", FieldType.Final, 4, "Télérèglement", FinalType.Unknown),
            ("HolderDataResidence", FieldType.Final, 17, "Ville du domicile", FinalType.Unknown),
            ("HolderDataCommercialID", FieldType.Final, 6, "Produit carte", FinalType.Integer),
            ("HolderDataWorkPlace", FieldType.Final, 17, "Lieu de travail", FinalType.Unknown),
            ("HolderDataStudyPlace", FieldType.Final, 17, "Lieu d'étude", FinalType.Unknown),
            ("HolderDataSaleDevice", FieldType.Final, 16, "Numéro logique de SAM", FinalType.Integer),
            ("HolderDataAuthenticator", FieldType.Final, 16, "Signature", FinalType.Unknown),
            ("HolderDataProfileStartDate1", FieldType.Final, 14, "Date de début de validité du statut", FinalType.Date),
            ("HolderDataProfileStartDate2", FieldType.Final, 14, "Date de début de validité du statut", FinalType.Date),
            ("HolderDataProfileStartDate3", FieldType.Final, 14, "Date de début de validité du statut", FinalType.Date),
            ("HolderDataProfileStartDate4", FieldType.Final, 14, "Date de début de validité du statut", FinalType.Date),
        ])
    ])
]


structEvent = [
    ("EventDateStamp", FieldType.Final, 14, "Date de l’événement", FinalType.Date),
    ("EventTimeStamp", FieldType.Final, 11, "Heure de l’événement", FinalType.Time),
    ("EventBitmap", FieldType.Bitmap, 28,
    [
        ("EventDisplayData", FieldType.Final, 8, "Données pour l’affichage", FinalType.Unknown),
        ("EventNetworkId", FieldType.Final, 24, "Réseau", FinalType.Integer),
        ("EventCode", FieldType.Final, 8, "Nature de l’événement", FinalType.EventCode),
        ("EventResult", FieldType.Final, 8, "Code Résultat", FinalType.EventResult),
        ("EventServiceProvider", FieldType.Final, 8, "Identité de l’exploitant", FinalType.EventServiceProvider),
        ("EventNotokCounter", FieldType.Final, 8, "Compteur évènements anormaux", FinalType.Unknown),
        ("EventSerialNumber", FieldType.Final, 24, "Numéro de série de l’événement", FinalType.Unknown),
        ("EventDestination", FieldType.Final, 16, "Destination de l’usager", FinalType.Unknown),
        ("EventLocationId", FieldType.Final, 16, "Lieu de l’événement", FinalType.LocationId),
        ("EventLocationGate", FieldType.Final, 8, "Identification du passage", FinalType.Unknown),
        ("EventDevice", FieldType.Final, 16, "Identificateur de l’équipement", FinalType.EventDevice),
        ("EventRouteNumber", FieldType.Final, 16, "Référence de la ligne", FinalType.RouteNumber),
        ("EventRouteVariant", FieldType.Final, 8, "Référence d’une variante de la ligne", FinalType.Unknown),
        ("EventJourneyRun", FieldType.Final, 16, "Référence de la mission", FinalType.Integer),
        ("EventVehicleId", FieldType.Final, 16, "Identificateur du véhicule", FinalType.Integer),
        ("EventVehicleClass", FieldType.Final, 8, "Type de véhicule utilisé", FinalType.Unknown),
        ("EventLocationType", FieldType.Final, 5, "Type d’endroit (gare, arrêt de bus), ", FinalType.Unknown),
        ("EventEmployee", FieldType.Final, 240, "Code de l’employé impliqué", FinalType.Unknown),
        ("EventLocationReference", FieldType.Final, 16, "Référence du lieu de l’événement", FinalType.Unknown),
        ("EventJourneyInterchanges", FieldType.Final, 8, "Nombre de correspondances", FinalType.Unknown),
        ("EventPeriodJourneys", FieldType.Final, 16, "Nombre de voyage effectué", FinalType.Unknown),
        ("EventTotalJourneys", FieldType.Final, 16, "Nombre total de voyage autorisé", FinalType.Unknown),
        ("EventJourneyDistance", FieldType.Final, 16, "Distance parcourue", FinalType.Unknown),
        ("EventPriceAmount", FieldType.Final, 16, "Montant en jeu lors de l’événement", FinalType.Unknown),
        ("EventPriceUnit", FieldType.Final, 16, "Unité de montant en jeu", FinalType.Unknown),
        ("EventContractPointer", FieldType.Final, 5, "Référence du contrat concerné", FinalType.Integer),
        ("EventAuthenticator", FieldType.Final, 16, "Code de sécurité", FinalType.Unknown),
        ("EventData", FieldType.Bitmap, 5,
        [
            ("EventDataDateFirstStamp", FieldType.Final, 14, "Date de la première montée", FinalType.Date),
            ("EventDataTimeFirstStamp", FieldType.Final, 11, "Heure de la première montée", FinalType.Time),
            ("EventDataSimulation", FieldType.Final, 1, "Dernière validation (0=normal, 1=dégradé), ", FinalType.Unknown),
            ("EventDataTrip", FieldType.Final, 2, "Tronçon", FinalType.Unknown),
            ("EventDataRouteDirection", FieldType.Final, 2, "Sens", FinalType.Unknown)
        ])
    ])
]

structContract = [
    ("Contract", FieldType.Bitmap, 20,
    [
        ("ContractNetworkId", FieldType.Final, 24, "Identification du réseau", FinalType.Integer),
        ("ContractProvider", FieldType.Final, 8, "Identification de l’exploitant", FinalType.Integer),
        ("ContractTariff", FieldType.Final, 16, "Code tarif", FinalType.Integer),
        ("ContractSerialNumber", FieldType.Final, 32, "Numéro TCN", FinalType.Integer),
        ("ContractCustomerInfoBitmap", FieldType.Bitmap, 2,
        [
            ("ContractCustomerProfile", FieldType.Final, 6, "Statut du titulaire ou Taux de réduction applicable", FinalType.Unknown),
            ("ContractCustomerNumber", FieldType.Final, 32, "Numéro de client", FinalType.Unknown)
        ]),
        ("ContractPassengerInfoBitmap", FieldType.Bitmap, 2,
        [
            ("ContractPassengerClass", FieldType.Final, 8, "Classe de service des voyageurs", FinalType.Unknown),
            ("ContractPassengerTotal", FieldType.Final , 8, "Nombre total de voyageurs", FinalType.Unknown)
        ]),
        ("ContractVehicleClassAllowed", FieldType.Final , 6, "Classes de véhicule autorisé", FinalType.Unknown),
        ("ContractPaymentPointer", FieldType.Final ,32, "Pointeurs sur les événements de paiement", FinalType.Unknown),
        ("ContractPayMethod", FieldType.Final , 11, "Code mode de paiement", FinalType.PayMethod),
        ("ContractServices", FieldType.Final ,16 ,"Services autorisés", FinalType.Unknown),
        ("ContractPriceAmount", FieldType.Final ,16, "Montant total", FinalType.Amount),
        ("ContractPriceUnit", FieldType.Final ,16, "Code de monnaie", FinalType.Unknown),
        ("ContractRestrictionBitmap", FieldType.Bitmap, 7,
        [
            ("ContractRestrictStart", FieldType.Final, 11, "", FinalType.Unknown),
            ("ContractRestrictEnd", FieldType.Final, 11, "", FinalType.Unknown),
            ("ContractRestrictDay", FieldType.Final, 8, "", FinalType.Unknown),
            ("ContractRestrictTimeCode", FieldType.Final, 8, "", FinalType.Unknown),
            ("ContractRestrictCode", FieldType.Final, 8, "Code de restriction", FinalType.Unknown),
            ("ContractRestrictProduct", FieldType.Final, 16, "Produit de restriction", FinalType.Unknown),
            ("ContractRestrictLocation", FieldType.Final, 16, "Référence du lieu de restriction", FinalType.Unknown)
        ]),
        ("ContractValidityInfoBitmap", FieldType.Bitmap, 9,
        [
            ("ContractValidityStartDate", FieldType.Final, 14,"Date de début de validité", FinalType.Date),
            ("ContractValidityStartTime", FieldType.Final, 11,"Heure de début de validité", FinalType.Time),
            ("ContractValidityEndDate", FieldType.Final, 14,"Date de fin de validité", FinalType.Date),
            ("ContractValidityEndTime", FieldType.Final, 11,"Heure de fin de validité", FinalType.Time),
            ("ContractValidityDuration", FieldType.Final, 8,"Durée de validité", FinalType.Unknown),
            ("ContractValidityLimiteDate", FieldType.Final, 14,"Date limite de première utilisation", FinalType.Date),
            ("ContractValidityZones", FieldType.Final, 8,"Numéros des zones autorisées", FinalType.Zones),
            ("ContractValidityJourneys", FieldType.Final, 16,"Nombre de voyages autorisés", FinalType.Unknown),
            ("ContractPeriodJourneys", FieldType.Final, 16,"Nombre de voyages autorisés par période", FinalType.Unknown)
        ]),
        ("ContractJourneyData", FieldType.Bitmap, 8,
        [
            ("ContractJourneyOrigin", FieldType.Final, 16,"Code lieu d’origine", FinalType.Unknown),
            ("ContractJourneyDestination", FieldType.Final, 16,"Code lieu de destination", FinalType.Unknown),
            ("ContractJourneyRouteNumbers", FieldType.Final, 16 ,"Numéros des lignes autorisées", FinalType.Unknown),
            ("ContractJourneyRouteVariants", FieldType.Final, 8,"Variantes aux numéros des lignes autorisées", FinalType.Unknown),
            ("ContractJourneyRun", FieldType.Final, 16 ,"Référence du voyage", FinalType.Unknown),
            ("ContractJourneyVia", FieldType.Final, 16, "Code lieu du via", FinalType.Unknown),
            ("ContractJourneyDistance", FieldType.Final, 16, "Distance", FinalType.Unknown),
            ("ContractJourneyInterchanges", FieldType.Final, 8, "Nombre de correspondances autorisées", FinalType.Unknown)
        ]),
        ("ContractSaleData", FieldType.Bitmap, 4,
        [
            ("ContractValiditySaleDate", FieldType.Final, 14, "Date de vente", FinalType.Date),
            ("ContractValiditySaleTime", FieldType.Final, 11, "Heure de vente", FinalType.Time),
            ("ContractValiditySaleAgent", FieldType.Final, 8, "Identification de l’exploitant de vente", FinalType.Integer),
            ("ContractValiditySaleDevice", FieldType.Final, 16, "Identification du terminal de vente", FinalType.Integer)
        ]),
        ("ContractStatus", FieldType.Final, 8, "État du contrat", FinalType.Unknown),
        ("ContractLoyaltyPoints", FieldType.Final, 16, "Nombre de points de fidélité", FinalType.Unknown),
        ("ContractAuthenticator", FieldType.Final, 16, "Code de contrôle de l’intégrité des données", FinalType.Integer),
        ("ContractData(0..255)", FieldType.Final, 0, "Données complémentaires", FinalType.Unknown)
    ])
]

structContractList = [
    ("BestContracts", FieldType.Counter, 4,
    [
        ("BestContract", FieldType.Bitmap, 3,
        [
            ("BestContractNetworkId", FieldType.Final, 24, "", FinalType.Integer),
            ("BestContractTariff", FieldType.Final, 16, "", FinalType.BestContractTariff),
            ("BestContractPointer", FieldType.Final, 5, "Pointeur sur le contrat", FinalType.Integer)
        ])
    ])
]

structSpecialEventList = [("SpecialEventNumber", FieldType.Counter, 4,
                [("SpecialEvent", FieldType.Bitmap, 4,
                  [("SpecialEventNetworkId", FieldType.Final, 24, \
                "", FinalType.Integer),
                   ("SpecialEventProvider",  FieldType.Final, 8, \
                "Exploitant", FinalType.Unknown),
                   ("SpecialEventSeriousness", FieldType.Final, 2, \
                    "Niveau de sévérité", FinalType.SpecialEventSeriousness),
                   ("SpecialEventPointer", FieldType.Final, 5, \
                    "Pointeur d'événement spécial", FinalType.Unknown)])])]


structCDFGTML = [
    (["Environment", "Holder next to Env"], FieldType.RecordEF, [0x20,0x01], [structEnv, structHolder]),
    ("EventLog", FieldType.RecordEF, [0x20, 0x10], structEvent),
    ("Contracts", FieldType.RecordEF, [0x20, 0x20], structContract),
    ("Contract List", FieldType.RecordEF, [0x20, 0x30], structContractList),
#       ("Counters", FieldType.RecordEF, [0x20, 0x69], structCounter),
    ("Special Events", FieldType.RecordEF, [0x20, 0x40], structEvent),
#       ("Special Event List", FieldType.RecordEF, [0x20, 0x03], structSpecialEventList)
]

structGTML = [
#       ("ICC", FieldType.RecordEF, [0x00, 0x02], structICC),
#       ("ID", FieldType.RecordEF, [0x00, 0x03], structID),
    ("Calypso DF", FieldType.DF, [0x20, 0x00], structCDFGTML)
]

structCDFCD97 = [
    (["Environment", "Holder next to Env"], FieldType.RecordEF, [0x20,0x01], [structEnv, structHolder]),
    ("EventLog", FieldType.RecordEF, [0x20, 0x10], structEvent),
    ("Contracts", FieldType.RecordEF, [0x20, 0x20], structContract),
    ("Contract List", FieldType.RecordEF, [0x20, 0x50], structContractList),
#       ("Counters", FieldType.RecordEF, [0x20, 0x69], structCounter),
    ("Special Events", FieldType.RecordEF, [0x20, 0x40], structEvent),
#       ("Special Event List", FieldType.RecordEF, [0x20, 0x03], structSpecialEventList)
]

structCD97 = [
#       ("ICC", FieldType.RecordEF, [0x00, 0x02], structICC),
#       ("ID", FieldType.RecordEF, [0x00, 0x03], structID),
    ("Calypso DF", FieldType.DF, [0x20, 0x00], structCDFCD97)
]

cardTypes = {
    "080303": ("GTML", structGTML),
    "080304": ("GTML2", structGTML),
    "0a0103": ("CD97", structCD97)
}

listOfStructs = [
    ("Environment", structEnv),
    ("Holder", structHolder),
    ("EventLog", structEvent),
    ("Contracts", structContract),
    ("Contract List", structContractList),
    ("Special Event List", structSpecialEventList)
]

#defaultNavigoStructure = structCD97
defaultNavigoStructure = ("GTML",structGTML)
