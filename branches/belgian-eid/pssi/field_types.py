# -*- coding: utf-8 -*-

# -- field_types.py
# Defines the different field types


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
    TransparentEF = 0.8
    FinalRepeated = 0.9
    StructRepeated = 0.01
    ReversedStructRepeated = 0.02
    FinalWithHeader = 0.03

