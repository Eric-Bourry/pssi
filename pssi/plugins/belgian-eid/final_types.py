# -*- coding: utf-8 -*-

# -- final_types.py
# Defines the data types


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


class FinalType:
    Unknown = 0.1
    HexString = 0.2
    String = 0.3
    CardNumber = 0.4
    NationalNumber = 0.5
    Sex = 0.6
    DocumentType = 0.7
    SpecialStatus = 0.8
