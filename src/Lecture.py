#! /usr/bin/env python
import xlrd # module de lecture des fichiers excel (microsoft)
import numpy as np #module mathematique numpy
import os
import csv
def lectxl(NOM):
    #NOM=input("nom du fichier:")#interactif
    #NOM=str(NOM +".xlsx")
    workbook = xlrd.open_workbook(NOM)
    SheetNameList = workbook.sheet_names()
    """for k in np.arange(len(SheetNameList)): 
        worksheet.append(workbook.sheet_by_name(SheetNameList[k]))"""
    worksheet = workbook.sheet_by_name(SheetNameList[0])
    num_rows = worksheet.nrows 
    f=[]
    for curr_row  in range(0,num_rows):
        row = worksheet.row(curr_row)
    #print row, len(row), row[0], row[1]
        f.append(row)
    return row
def lectcsv(NOM):
    #NOM=input("nom du fichier:")#interactif
    #NOM=str(NOM +".csv")
    with open(NOM) as f:
       contenu = csv.reader(f, delimiter=' ', quotechar='|')
    return contenu
def allfiles():
    name=os.listdir('../data/public')
    enorme=[]
    for k in range(0, len(name)):
        if '.xlsx' in name[k]:
            enorme.append(lectxl(name[k]))
        else:
            Chemin=str("../data/public/"+name[k])
            enorme.append(lectcsv(Chemin))
    return enorme