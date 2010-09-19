#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -- pssi.py
# Main file

import sys
import getopt
import card_interface
import display
import bruteforce

optionsList = [
    ("-a", "apdu mode, show the APDUs"),
    ("-b", "choose bruteforce mode"),
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
    print "Usage: pssi [options] [plugin]"
    for opt, desc in sorted(optionsList):
        print "\t%-10s%s" % (opt, desc)
    sys.exit(2)


def main():
    options = ""
    for opt, dec in optionsList:
        options += opt[1:]

    try:
        opts, args = getopt.getopt(sys.argv[1:], options)
    except getopt.GetoptError, err:
        print str(err)
        usage()

    mode = UsageMode.Dumper
    
    # TODO : Faire une option pour spécifier le CLASS BYTE en paramètre dans le cas d'un BF
    for o, a in opts:
        if o == "-a":
            card_interface.apduMode = True
        elif o == "-h":
            usage()
        elif o == "-v":
            display.verboseMode = True
        elif o == "-r":
            bruteforce.recursiveMode = True
        elif o == "-b":
            mode = UsageMode.Bruteforce
        elif o == "-l":
            mode = UsageMode.Loop
        elif o == "-d":
            mode = UsageMode.Dumper
        else:
            assert False, "unhandled option: %s" % (o)

    if len(args) < 1:
        # TODO : Should be a different error
        usage()
        
    sys.path.append(args[0])
    import plugin
    card_interface.cla = plugin.getClassByte()

    if mode == UsageMode.Dumper:
        import dumper
        dumper.startDump()

    elif mode == UsageMode.Loop:
        import loop
        loop.startLoop()

    elif mode == UsageMode.Bruteforce:
        bruteforce.startBruteforce()


if __name__ == '__main__':
    main()
