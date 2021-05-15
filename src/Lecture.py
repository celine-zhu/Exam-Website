#! /usr/bin/python3
import xlrd # module de lecture des fichiers excel (microsoft)
import click
import os
import csv

def lectxl(NOM):
    """fonction de lecture de fichiers excel utilisant le module xlrd,
    prenant en argument le nom du fichier et retourne une liste de liste des 
    lignes du fichier"""
    #NOM=input("nom du fichier:")#interactif
    #NOM=str(NOM +".xlsx")
    workbook = xlrd.open_workbook(NOM)
    SheetNameList = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(SheetNameList[0])
    num_rows = worksheet.nrows 
    f=[NOM]
    for curr_row  in range(0,num_rows):
        row = worksheet.row(curr_row)
        f.append(row)
    return f

def lectcsv(NOM):
    """fonction de lecture des fichiers csv utilisant le module csv,
    prenant en argument le nom du fichier csv et retourne une liste de liste 
    des fichiers"""
    #NOM=input("nom du fichier:")#interactif
    #NOM=str(NOM +".csv")
    c=[NOM]
    #ouverture du fichier et recuperation du contenu
    with open(NOM) as f:
       contenu = csv.reader(f, delimiter=' ', quotechar='|')
       for row in contenu:
           c.append(row[0].split(';'))#separation du string 
    return c

def allfiles():
    """fonction de lecture qui lit tous les fichier en distinguant 
    les différents types ( csv versus excel)et retourne une liste de listes 
    de listes contenat les contenus de tous les fichiers"""
    
    #recuperation des noms de fichiers dans ../data/public
    name=os.listdir('../data/public')
    #initialisation liste
    fil=[]
    for k in range(0, len(name)):
        Chemin=str("../data/public/" + name[k])
        if '.xlsx' in name[k]:
            fil.append(lectxl(Chemin))
        else:
            fil.append(lectcsv(Chemin))
    return fil