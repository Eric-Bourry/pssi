# -*- coding: utf-8 -*-

import interpreters


def getClassByte():
    return 0x94
	

def getRootStructure():
    return interpreters.currentStructure[1]


def getInterpretersTable():
    return interpreters.interpretingFunctions
