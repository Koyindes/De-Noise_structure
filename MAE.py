#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pymatgen
import periodictable
from pymatgen.io.cif import CifParser
import matplotlib.pyplot as plt

filePath = "" 
filenameList = []
elementList = []
disList = []
elementSum = []
cmList = []

class Cifmolecular:
    filename = ""
    dis = 0
    element = []

    def __init__(self, name):
        self.filename = name
        self.dis = 0
        self.element = []
    
def getDis(filename):
    pattern = re.compile(r"[+-]?[\d]+[\.]?[\d]*[Ee]?[+-]?[\d]*")
    l = pattern.findall(filename)
    return float(l[0])
    
def initList():
    for el in periodictable.elements:
        elementList.append(el.symbol)
        disList.append(0)
        elementSum.append(0)
    del elementList[0]
    del disList[0]
    del elementSum[0]

def dealList():
    for cm in cmList:
        for element in cm.element:
            index = elementList.index(element)
            disList[index] = disList[index] + cm.dis
            elementSum[index] = elementSum[index] + 1

def classCif():
    pattern = re.compile(r'[a-zA-Z]+')
    for filename in filenameList:
        cm = Cifmolecular(filename)
        cm.dis = getDis(filename)
        
        parser = CifParser(filePath + "/" + filename)
        structure = parser.get_structures()[0]
        species = structure.species
        for i in species:
            element = pattern.findall(str(i))[0]
            if not element in cm.element:
                cm.element.append(element)
                
        cmList.append(cm)

def delList():
    i = 0
    while i < len(elementList):
        if elementSum[i] == 0:
            del elementList[i]
            del disList[i]
            del elementSum[i]
        else:
            disList[i] = disList[i] / elementSum[i]
            i = i + 1
    
if __name__=='__main__':
    filePath = "../data/cif_files" 
    filenameList = os.listdir(filePath)

    initList()
    classCif()
    dealList()
    delList()
    
    plt.xticks(rotation = 60)
    plt.bar(elementList, disList)
    plt.title('MAE')
    plt.show()

    
