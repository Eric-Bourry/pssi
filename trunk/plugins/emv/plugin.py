# -*- coding: utf-8 -*-

import interpreters
import structures


def getClassByte():
    return 0x00
	

def getRootStructure():
    #return interpreters.currentStructure[1]
    return structures.structEMV

'''
hihi = {
    "ATR": parseATRhihi
}
'''

def getInterpretersTable():
    return interpreters.interpretingFunctions
    #return {}