#! /usr/bin/env python
import openpyxl as xl  # module de lecture des fichiers excel (microsoft)
import csv
from abc import *

class FileReading(ABC):
    @abstractmethod
    def read(self, NOM : str):
        pass


class XLRS(FileReading):
    def __init__(self):
        pass

    def read(self, NOM : str):
        """fonction de lecture de fichiers excel utilisant le module xlrd,
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

class CVS(FileReading):
    def __init__(self):
        pass

    def read(self, NOM : str):
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