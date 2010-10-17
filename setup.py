#!/usr/bin/env python
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



from distutils.core import setup

files = [
    "plugins/emv/*",
    "plugins/sim/*",
    "plugins/navigo/*"
]

setup(
    name='Pssi',
    version='1.0',
    description='Python Simple Smartcard Interpreter',
    author='Eric Bourry & Julien Flaissy',
    author_email = 'eric.bourry@gmail.com & julien.flaissy@gmail.com',
    url='http://code.google.com/p/pssi/',
    package_data = {'pssi' : files },
    packages=['pssi'],
)