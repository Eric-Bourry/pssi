# -*- coding: utf-8 -*-

import interpreters
import structures


def getClassByte():
    return 0xA0
	

def getRootStructure():
    #return interpreters.currentStructure[1]
    return structures.structSIM
    #return []

'''
hihi = {
    "ATR": parseATRhihi
}
'''

def getInterpretersTable():
    return interpreters.interpretingFunctions
    #return {}