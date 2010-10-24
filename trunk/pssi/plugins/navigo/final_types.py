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



class FieldType:
    DF = 0.1
    RecordEF = 0.2
    Bitmap = 0.3
    Final = 0.4
    Counter = 0.5
    DFName = 0.6
    DFList = 0.7

class FinalType:
    Unknown = 0
    Date = 1
    Time = 2
    Zones = 3
    ApplicationVersionNumber = 4
    Amount = 5
    PayMethod = 6
    BestContractTariff = 7
    SpecialEventSeriousness = 8
    EventCode = 9
    EventServiceProvider = 10
    Integer = 11
    EventResult = 12
    RouteNumber = 13
    LocationId = 14
    EventDevice = 15
    HolderDataCardStatus = 16
