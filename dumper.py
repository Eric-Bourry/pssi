# -*- coding: utf-8 -*-

# -- dump.py
# The dumper


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



import display
import structure_parser
import card_interface

def startDump():
    """Launch the dumping process: parse the card and print the
    results."""
    card = card_interface.getCard()
    if card:
        content = structure_parser.parseCard(card)
        display.prettyPrint(content)
