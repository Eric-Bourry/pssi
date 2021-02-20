#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -- pssi.py
# Main file


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


import sys
import getopt
import card_interface
import display
import bruteforce

optionsList = [
    ("-a", "apdu mode, show the APDUs"),
    ("-b", "choose bruteforce mode"),
    ("-c:", "specify the class byte for the bruteforce mode, in hexadecimal"),
    ("-d", "choose dump mode (default, specify a plugin)"),
    ("-h", "show this help"),
    ("-l", "choose loop mode (specify a plugin)"),
    ("-r", "enable recursive mode in the bruteforce mode"),
    ("-v", "verbose mode, show the raw data along with the interpretation")
]

class UsageMode:
    Dumper = 0
    Bruteforce = 1
    Loop = 2

def usage():
    print("Usage: pssi [options] plugin_path")
    print("Example: ./pssi.py plugins/sim")
    for opt, desc in sorted(optionsList):
        print(("\t%-10s%s" % (opt, desc)))
    sys.exit(2)


def main():
    # Build the list of options e.g. 'abdhlrv'.
    options = ''.join([o[1:] for o, d in optionsList])
    try:
        opts, args = getopt.getopt(sys.argv[1:], options)
    except getopt.GetoptError as err:
        print((str(err)))
        usage()

    mode = UsageMode.Dumper

    for o, a in opts:
        if o == "-a":
            card_interface.apduMode = True
        elif o == "-h":
            usage()
        elif o == "-v":
            display.verboseMode = True
        elif o == "-r":
            bruteforce.recursiveMode = True
        elif o == "-c":
            card_interface.cla = int(a, 16)
        elif o == "-b":
            mode = UsageMode.Bruteforce
        elif o == "-l":
            mode = UsageMode.Loop
        elif o == "-d":
            mode = UsageMode.Dumper
        else:
            assert False, "unhandled option: %s" % o

    if mode == UsageMode.Bruteforce:
        bruteforce.startBruteforce()

    else:
        if len(args) < 1:
            print("--> You forgot to specify a plugin.\n")
            usage()

        sys.path.append(args[0])
        try:
            import plugin
        except ImportError:
            print(("--> The plugin '%s' cannot be found" % args[0]))
            usage()
        card_interface.cla = plugin.getClassByte()

        if mode == UsageMode.Dumper:
            import dumper
            dumper.startDump()

        elif mode == UsageMode.Loop:
            import loop
            loop.startLoop()


if __name__ == '__main__':
    main()
