#! /usr/bin/env python

import openpyxl as xl  # module de lecture des fichiers excel (microsoft)
import os
import csv


def lectxl(NOM):
    """fonction de lecture de fichiers excel utilisant le module openpyxl,
    prenant en argument le nom du fichier et retourne une liste de liste des 
    lignes du fichier"""
    # NOM=input("nom du fichier:")#interactif
    # NOM=str(NOM +".xlsx")
    workbook = xl.load_workbook(NOM, read_only=True)  # Lecture seul pour économiser les ressources
    worksheet = workbook.active
    f = [NOM]
    for curr_row in worksheet.iter_rows():
        row = []
        for curr_cell in curr_row:
            row.append(curr_cell.value)
        f.append(row)
    return f


def lectcsv(NOM):
    """fonction de lecture des fichiers csv utilisant le module csv,
    prenant en argument le nom du fichier csv et retourne une liste de liste 
    des fichiers"""
    # NOM=input("nom du fichier:")#interactif
    # NOM=str(NOM +".csv")
    c = [NOM]
    # ouverture du fichier et recuperation du contenu
    with open(NOM) as f:
        contenu = csv.reader(f, delimiter=' ', quotechar='|')
        for row in contenu:
            c.append(row[0].split(';'))  # separation du string
    return c


def allfiles():
    """fonction de lecture qui lit tous les fichier en distinguant 
    les différents types ( csv versus excel)et retourne une liste de listes 
    de listes contenat les contenus de tous les fichiers"""

    # recuperation des noms de fichiers dans ../data/public
    list_name = os.listdir('../data/public')
    # initialisation liste
    fil = []
    for name in list_name:
        Chemin = str("../data/public/" + name)
        enorme = []
        if '.xlsx' in name:
            enorme.append(lectxl(Chemin))
        else:
            enorme.append(lectcsv(Chemin))
        fil.append(enorme)
    return fil
