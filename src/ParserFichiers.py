#! /usr/bin/env python
import os.path
import sqlite3
import sys
import ParserDonnee as pars
from src.PolyMorph_Lecture import *

# ------------------- Fonctions parsant les différents fichiers -------------------


DB_PATH = "../bdd/project.db"


def UploadInscription(file: list):
    name = file[0]
    if name.split("/")[-1] != "Inscription.xlsx":
        print("Attention, ce n'est peut-être pas le bon fichier", file=sys.stderr)
    nom_champs = file[2]  # En-tête : contient le nom de chaque colonne (fichier[1] vide)
    list_champ = []
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for line in file[3:]:
        champ = {"code": line[0],  # int,
                 "civ_lib": line[4],  # int
                 "nom": line[1],
                 "prenom": line[2],
                 "autre_prenoms": line[3],
                 "date_naissance": line[5],
                 "arr_naissance": line[51],  # int,
                 "ville_naissance": AddCommune(line[6]),
                 "code_pays_naissance": AddCountry(line[8]),
                 # "code_pays_naissance": line[7],  # int
                 # "pays_naissance": line[8],
                 "francais": line[9],  # int,
                 "ad_1": line[12],
                 "ad_2": line[13],
                 "cod_pos": line[14],  # int,
                 "com": AddCommune(line[15]),
                 "code_pay_natio": line[10],  # int,
                 "autre_natio": line[11],
                 "code_pays": line[16],  # int,
                 "lib_pays": line[17],
                 "tel": pars.telephone(line[18]),
                 "por": pars.telephone(line[19]),
                 "email": line[20],
                 # "classe": line[21],
                 # "puissance": line[22],
                 "code_etabl": AddEtabl(line[23], line[24], line[25]),  # int,
                 # "etabl": line[24],
                 # "ville_etabl": line[25],
                 "epr1": line[26],
                 "opt1": line[27],
                 "epr2": line[28],
                 "opt2": line[29],
                 "epr3": line[30],
                 "opt3": line[31],
                 "epr4": line[32],
                 "opt4": line[33],
                 "lib_ville_ecrit": line[34],
                 "code_concours": line[35],  # int,
                 "lib_concours": line[36],
                 "voie": line[37],
                 "ann_bac": line[38],  # int,
                 "mois_bac": line[39],  # int,
                 "code_serie": line[40],  # int,
                 "serie": line[41],
                 "mention": line[42],
                 "sujet_tipe": line[43],
                 "ine": line[44],
                 "cod_csp_pere": line[45],  # int,
                 # "lib_csp_pere": line[46],
                 "cod_csp_mere": line[47],  # int,
                 # "lib_csp_mere": line[48],
                 "code_etat_dossier": line[49],  # int,
                 # "lib_etat_dossier": line[50],
                 "handicap": line[52],
                 "qualite": line[53],
                 "can_dep_bac": line[54],  # int
                 }

        AddCSP(champ["cod_csp_pere"], line[46])
        AddCSP(champ["cod_csp_mere"], line[48])

        # Il faut verifier si l'entrée existe déjà (avec le code_candidat)
        # Si oui: on met à jour. Sinon: on crée et on rempli le champ

        # Avant d'inserer le champ, il faut remplir les tables auxiliaires, afin d'avoir éventuellement l'index associé
        # a mettre dans l'entrée de "candidat"

        str_excl = "(" + "?, " * len(champ.keys())
        str_excl = str_excl[:-2] + ")"  # Donne "(?, ?, ?, ?, ?)" avec autant de "?" que de données

        cur.execute(f"insert into candidat {tuple(champ.keys())} values {str_excl}", tuple(champ.values()))
        list_champ.append(champ)

    con.commit()
    con.close()
    return nom_champs, list_champ


def UploadEtabli(file: list):
    name = file[0]
    if name.split("/")[-1] != "listeEtablissements.xlsx":
        print("Attention, ce n'est peut-être pas le bon fichier", file=sys.stderr)
    nom_champs = file[2]  # En-tête : contient le nom de chaque colonne (fichier[1] vide)
    list_champ = []
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for line in file[3:]:
        champ = {
            "rne": line[0],
            "type": line[1],
            "nom": line[2],
            "code_postal": line[3],
            "ville": line[4],
            "pays": line[5]
        }

        cur.execute("SELECT rne FROM etablissement WHERE rne=?", (champ["rne"],))
        res = cur.fetchall()
        #       if we already have the school, we juste update it's value
        if res:
            for e in champ.keys():
                res += e + " = ?,"
            res = res[:-1]
            cur.execute(f"UPDATE etablissement SET {res}", tuple(champ.values()))
        else:
            str_excl = "(" + "?, " * len(champ.keys())
            str_excl = str_excl[:-2] + ")"  # Ne marche pas sinon
            cur.execute(f"INSERT INTO etablissement {tuple(champ.keys())} VALUES {str_excl}", tuple(champ.values()))
        list_champ.append(champ)
    con.commit()
    con.close()
    return nom_champs, list_champ


def UploadListeVoeux(liste):
    assert os.path.exists(DB_PATH), "database not found"

    data = liste[2:]

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for line in data:
        query = "INSERT INTO voeux_ecole(can_code, voe_rang, voe_ord, eco_code) VALUES(?,?,?,?)"
        cur.execute(query, (line[0], line[1], line[2], line[3]))
    con.commit()
    con.close()



def UploadAdm(liste, resulttype: str = "Admissible"):
    assert os.path.exists(DB_PATH), "database not found"

    data = liste[2:]
    m = AddCivilite("M.")
    mme = AddCivilite("Mme")
    cividico = {
        "M.": m,
        "Mme": mme
    }
    code_resultat = AddResultat(resulttype)

    for line in data:
        # we check if the data exist already

        id_commune = AddCommune(line[7])
        id_contry = AddCountry(line[8])

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT code FROM candidat WHERE code=?", (line[0],))

        res = cur.fetchall()

        #       if we already have a candidate, we juste update it's value
        if res:
            # value de rang?
            # virer les not null qui sont partout
            query = "UPDATE candidat SET civ_lib=?, nom=?, prenom=?, ad_1=?, ad_2=?, cod_pos=?, com=?, pay_adr=?, mel=?, tel=?, por=?, resultat=? WHERE code=?"
            cur.execute(query, (
            line[1], cividico.get(line[2]), line[3], line[4], line[5], line[6], id_commune, id_contry, line[9],
            pars.telephone(line[10]),pars.telephone(line[11]),code_resultat, line[0],))
            # else we create a new one
        else:
            query = "INSERT INTO candidat(code, civ_lib, nom, prenom, ad_1, ad_2, cod_pos, com, pay_adr, mel, tel, por, resultat) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cur.execute(query, (
            line[0], line[1], cividico.get(line[2]), line[3], line[4], line[5], line[6], id_commune, id_contry, line[9],
            pars.telephone(line[10]), pars.telephone(line[11]), code_resultat,))
        con.commit()
        con.close()




def UploadEcole(liste):
    # pas de champs rang dans la bdd
    assert os.path.exists(DB_PATH), "database not found"

    data = liste[2:]

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for line in data:
        # we check if the data exist already
        query = "INSERT INTO ecole(code, nom) VALUES(?,?)"
        cur.execute(query, (line[0], line[1],))
    con.commit()
    con.close()

#fonction a utiliser pour upload les fichiers de ResulttatEcrit, ResultatOral et CMT_Oral
def UploadNote(liste, typeExam: str):
    # type exam is a string that correspond to a type of exam such a written, oral, ...
    assert os.path.exists(DB_PATH), "database not found"

    data = liste[3:]

    id_matiere = []
    typeE = AddTypeExam(typeExam)
    for i in range(1, len(liste[1])):
        if liste[1][i]:
            print(liste[1][i], liste[2][i])
            id_matiere.append(AddMatiere(liste[1][i], liste[2][i]))

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "INSERT INTO notes(can_code, matiere_id,type_id, value) VALUES(?,?,?,?)"
    for line in data:
        for i in range(1, len(line)):
            if line[i]:
                cur.execute(query, (line[0], id_matiere[i - 1], typeE, line[i],))
    con.commit()
    con.close()


def AddCSP(code: int, lib: str):
    """Add the CSP to the DB if doesn't exist, using his code as index. return its code"""
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT csp FROM csp WHERE code_csp=?", (code,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO csp(code_csp, csp) VALUES(?, ?)", (code, lib,))
    con.commit()

    con.close()
    return code


def AddTypeExam(name: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT type_id FROM typeExam WHERE label=?", (name,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO typeExam(label) VALUES(?)", (name,))
        cur.execute("SELECT type_id FROM typeExam WHERE label=?", (name,))
        res = cur.fetchall()
    con.commit()

    con.close()
    return res[0][0]


def AddMatiere(name: str, code=None):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT matiere_id FROM matiere WHERE label=?", (name,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO matiere(label,code) VALUES(?,?)", (name, code,))
        cur.execute("SELECT matiere_id FROM matiere WHERE label=?", (name,))
        res = cur.fetchall()
    con.commit()

    con.close()
    return res[0][0]


def AddCommune(name: str):
    # add the commune to the bdd if it doesn't exist and return it's code
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT commune_index FROM commune WHERE commune=?", (name,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO commune(commune) VALUES(?)", (name,))
        cur.execute("SELECT commune_index FROM commune WHERE commune=?", (name,))
        res = cur.fetchall()
    con.commit()

    con.close()
    return res[0][0]


def AddCountry(name: str):
    # add the country to the bdd if it doesn't exist and return it's code
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT pays_code FROM pays WHERE liste_pays=?", (name,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO pays(liste_pays) VALUES(?)", (name,))
        cur.execute("SELECT pays_code FROM pays WHERE liste_pays=?", (name,))
        res = cur.fetchall()
    con.commit()

    con.close()
    return res[0][0]


def AddResultat(name: str):
    # add the result of the admission to the bdd if it doesn't exist and return it's code
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT resultat_index FROM resultat WHERE resultat=?", (name,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO resultat(resultat) VALUES(?)", (name,))
        cur.execute("SELECT resultat_index FROM resultat WHERE resultat=?", (name,))
        res = cur.fetchall()
    con.commit()

    con.close()
    return res[0][0]


def AddEtabl(code: str, name: str, ville: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT rne FROM etablissement WHERE nom=?", (name,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO etablissement(rne, nom, ville) VALUES(?, ?, ?)", (code, name, ville,))
        cur.execute("SELECT rne FROM etablissement WHERE nom=?", (name,))
        res = cur.fetchall()

    con.commit()
    con.close()
    return res[0][0]

def AddCivilite(name: str):
    # add the commune to the bdd if it doesn't exist and return it's code
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("SELECT civilite_index FROM civilite WHERE civilite=?", (name,))
    res = cur.fetchall()
    if not res:
        cur.execute("INSERT INTO civilite(civilite) VALUES(?)", (name,))
        cur.execute("SELECT civilite_index FROM civilite WHERE civilite=?", (name,))
        res = cur.fetchall()
    con.commit()

    con.close()
    return res[0][0]
