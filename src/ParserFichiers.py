#! /usr/bin/env python
import os.path
import sqlite3
import sys
import ParserDonnee as pars
from src.PolyMorph_Lecture import *
from AjoutDonnee import *

# ------------------- Fonctions parsant les différents fichiers -------------------


DB_PATH = "../bdd/project.db"


def UploadInscription(file: list):
    name = file[0]
    if name.split("/")[-1] != "Inscription.xlsx":
        print("Attention, ce n'est peut-être pas le bon fichier", file=sys.stderr)
    nom_champs = file[2]  # En-tête : contient le nom de chaque colonne (fichier[1] vide)
    list_champ = []
    con = sqlite3.connect(DB_PATH)

    for line in file[3:]:

        liste_int = [0, 4, 7, 9, 10, 14, 16, 35, 38, 39, 40, 45, 47, 49, 51]  # liste des champs contenant des entiers
        for i in liste_int:  # Passe les nombres en int
            if not line[i] is None:
                line[i] = int(line[i])
        if line[54] == "2A":
            line[54] = "201"
        if line[54] == "2B":
            line[54] = "202"
        elif not line[54] is None:
            line[54] = int(line[54])

        code_ville_naissance = AddCommune(line[6], con)
        code_pays_naissance = AddCountry(line[8], con, line[7])
        code_com = AddCommune(line[15], con)
        code_puissance = AddPuissance(line[22], con)
        code_etabl = AddEtabl(line[23], line[24], line[25], con)
        code_ville_ecr = AddCommune(line[34], con)
        code_concours = AddConcours(line[35], line[36], con)
        code_voie = AddVoie(line[37], con)
        code_serie = AddSerie(line[40], line[41], con)
        code_mention = AddMention(line[42], con)
        code_csp_pere = AddCSP(line[45], line[46], con)
        code_csp_mere = AddCSP(line[47], line[48], con)
        code_etat_dossier = AddEtatDossier(line[49], line[50], con)
        code_handicap = AjoutHandicap(line[52])
        code_qualite = AddQualite(line[53], con)

        epreuve_1 = AddEpreuve(line[26], con)
        option_1 = AddEpreuve(line[27], con)
        epreuve_2 = AddEpreuve(line[28], con)
        option_2 = AddEpreuve(line[29], con)
        epreuve_3 = AddEpreuve(line[30], con)
        option_3 = AddEpreuve(line[31], con)
        epreuve_4 = AddEpreuve(line[32], con)
        option_4 = AddEpreuve(line[33], con)

        champ = {"code": line[0],  # int,
                 "civ_lib": line[4],  # int
                 "nom": line[1],
                 "prenom": line[2],
                 "autre_prenoms": line[3],
                 "date_naissance": line[5],
                 "arr_naissance": line[51],  # int,
                 "code_ville_naissance": code_ville_naissance,
                 "code_pays_naissance": code_pays_naissance,
                 # "code_pays_naissance": line[7],  # int
                 # "pays_naissance": line[8],
                 "francais": line[9],  # int,
                 "ad_1": line[12],
                 "ad_2": line[13],
                 "cod_pos": line[14],  # int,
                 "com": code_com,
                 "code_pay_natio": line[10],  # int,
                 # "autre_natio": line[11],
                 # "code_pays": line[16],  # int,
                 # "lib_pays": line[17],
                 "tel": pars.telephone(line[18]),
                 "por": pars.telephone(line[19]),
                 "email": line[20],
                 # "classe": line[21],
                 "code_puissance": code_puissance,
                 "code_etabl": code_etabl,  # int
                 # "etabl": line[24],
                 # "ville_etabl": line[25],
                 "epreuve_1": epreuve_1,
                 "option_1": option_1,
                 "epreuve_2": epreuve_2,
                 "option_2": option_2,
                 "epreuve_3": epreuve_3,
                 "option_3": option_3,
                 "epreuve_4": epreuve_4,
                 "option_4": option_4,
                 "code_ville_ecr": code_ville_ecr,
                 "code_concours": code_concours,  # int,
                 # "lib_concours": line[36],
                 "code_voie": code_voie,
                 "bac_date": int(str(line[38]) + str(line[39]).zfill(2)),  # Date au format "AAAAMM"
                 # "ann_bac": line[38],  # int,
                 # "mois_bac": line[39],  # int,
                 "code_serie": code_serie,  # int,
                 # "serie": line[41],
                 "code_mention": code_mention,
                 "sujet_tipe": line[43],
                 "ine": line[44],
                 "code_csp_pere": code_csp_pere,  # int,  # Ajout effectué en dessous
                 # "lib_csp_pere": line[46],
                 "code_csp_mere": code_csp_mere,  # int,
                 # "lib_csp_mere": line[48],
                 "code_etat_dossier": code_etat_dossier,  # int,
                 # "lib_etat_dossier": line[50],
                 "handicap": code_handicap,
                 "code_qualite": code_qualite,  # int
                 "can_dep_bac": line[54],  # int
                 }

        # Il faut verifier si l'entrée existe déjà (avec le code_candidat)
        # Si oui: on met à jour. Sinon: on crée et on rempli le champ

        # Avant d'inserer le champ, il faut remplir les tables auxiliaires, afin d'avoir éventuellement l'index associé
        # a mettre dans l'entrée de "candidat"

        InsertOrUpdateData(champ, "code", "candidat", "code", con)
        list_champ.append(champ)

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

        pays_id = AddCountry(line[5], con)
        ville = AddCommune(line[4], con)

        champ = {
            "rne": line[0],
            "type": line[1],
            "nom": line[2],
            "code_postal": line[3],
            "ville": ville,
            "code_pays": pays_id
        }

        str_excl = "(" + "?, " * len(champ.keys())
        str_excl = str_excl[:-2] + ")"  # Ne marche pas sinon
        cur.execute(f"INSERT OR REPLACE INTO etablissement {tuple(champ.keys())} VALUES {str_excl}", tuple(champ.values()))
        list_champ.append(champ)
        con.commit()
    con.close()

    return nom_champs, list_champ

def UploadClasse(liste):
    assert os.path.exists(DB_PATH), "database not found"
    i = 0
    while liste[i][0] != "login":
        i = i+1
    data = liste[i:]

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    ecrit_mat = []
    i = 13
    while "(" in data[0][i]:
        tmp = pars.ParsMatName(data[0][i])
        ecrit_mat.append(AddMatiere(tmp[1], con, tmp[0]))
        i = i + 1
    ecrit_mat.append(AddMatiere("bonification", con))
    ecrit_mat.append(AddMatiere("total", con))
    ecrit_mat.append(AddMatiere("rang", con))
    ecrit = AddTypeExam("ecrit", con)



    oral = AddTypeExam("oral", con)
    other_mat = []
    other_mat.append( [AddMatiere("Mathématique harmonisé", con, 400), len(data[0])-13] )
    other_mat.append( [AddMatiere("Mathématiques affiché", con, 401), len(data[0])-12] )
    other_mat.append( [AddMatiere("bonification", con), len(data[0])-9] )
    other_mat.append( [AddMatiere("total", con), len(data[0])-8] )
    #i = i + 2
    #pos = 1
    #oral_mat = []
    #while pos == int(data[0][i + pos].split()[0]):
    #    oral_mat.append(pars.ParsMatName(data[0][i + pos]))
    #    pos = pos + 1
    adminTypeDico = {
        "A": "admissible",
        "B": "admissible-spe"
    }

    for line in data[1:]:
        fil = AddVoie(line[3], con)
        type_admin = adminTypeDico.get(line[4])
        commune = AddCommune(line[8], con)
        country = AddCountry(line[9], con)

        res = cur.execute("SELECT code FROM candidat WHERE code=?",(line[0],)).fetchall()
        if res:
            query = "UPDATE candidat SET nom=?, prenom=?, code_voie=?, resultat=?, email=?, ad_1=?, cod_pos=?, com=?, pay_adr=?, por=?, date_naissance=?, n_demi=?, bonus_interclassement=?, rang_classe=? WHERE code=?"
            cur.execute(query, (line[1], line[2], fil, type_admin, line[5], line[6], line[7], commune, country, line[10], line[11], line[12], line[len(line)-6], line[len(line)-1], line[0],))
        else:
            query = "INSERT INTO candidat(code, nom, prenom, code_voie, resultat, email, ad_1, cod_pos, com, pay_adr, por, date_naissance, n_demi, bonus_interclassement, rang_classe) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cur.execute(query, (line[0], line[1], line[2], fil, type_admin, line[5], line[6], line[7], commune, country, line[10], line[11], line[12], line[len(line)-6], line[len(line)-1],))
        j = 0
        while j < len(ecrit_mat):
            query = "INSERT OR REPLACE INTO notes(can_code, matiere_id,type_id, value) VALUES(?,?,?,?)"
            if line[13+j]:
                cur.execute(query, (line[0], ecrit_mat[j], ecrit, line[13+j]))
            j = j + 1
        for j in other_mat:
            query = "INSERT OR REPLACE INTO notes(can_code, matiere_id,type_id, value) VALUES(?,?,?,?)"
            if line[j[1]]:
                cur.execute(query, (line[0], j[0], oral, line[j[1]],))

        con.commit()
    con.close()

def UploadSCEI(liste):
    assert os.path.exists(DB_PATH), "database not found"

    con = sqlite3.connect(DB_PATH)

    code_voie = AddVoie(pars.findVoie(liste[0]), con)

    data = liste[2:]
    cur = con.cursor()
    oral = AddTypeExam("oral", con)
    total = AddMatiere("total", con)
    for line in data:

        query = "INSERT OR REPLACE INTO ranginfo(rang_classe, code_voie, scei, etat, moyenne_generale) VALUES(?, ?, ?, ?, ?)"
        cur.execute(query, (line[6], code_voie, line[0], line[2], line[5],))
        res = cur.execute("SELECT code FROM candidat WHERE rang_classe=? and code_voie=?", (line[6], code_voie,)).fetchall()
        if res:
            cur.execute("INSERT OR REPLACE INTO notes(can_code, matiere_id,type_id, value) VALUES(?,?,?,?)", (res[0][0], total, oral, line[3],))
        con.commit()
    con.close()

def UploadListReponse(liste):
    assert os.path.exists(DB_PATH), "database not found"

    data = liste[2:]
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for line in data:
        query = "INSERT OR REPLACE INTO reponse(Ata_cod, Ata_lib) VALUES(?,?)"
        cur.execute(query, (line[0], line[1],))
        con.commit()
    con.close()


def UploadListeVoeux(liste):
    assert os.path.exists(DB_PATH), "database not found"

    data = liste[2:]

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for line in data:
        UpdateVoieCandidat(liste[0], line[0], con)
        query = "INSERT OR REPLACE INTO voeux_ecole(can_code, voe_rang, voe_ord, eco_code, Ata_cod) VALUES(?,?,?,?,?)"
        cur.execute(query, (line[0], line[1], line[2], line[3],-11))
        con.commit()
    con.close()


def UploadAdm(liste, resulttype: str = "admissible"):

    assert os.path.exists(DB_PATH), "database not found"

    resulttype = resulttype + '-spe'*("-spe" in liste[0].lower())

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    code_voie = AddVoie(pars.findVoie(liste[0]), con)
    data = liste[2:]
    m = AddCivilite("M.", con)
    mme = AddCivilite("Mme", con)
    cividico = {
        "M.": m,
        "Mme": mme
    }
    code_resultat = AddResultat(resulttype, con)

    for line in data:
        # we check if the data exist already

        id_commune = AddCommune(line[7], con)
        id_contry = AddCountry(line[8], con)


        cur.execute("SELECT code FROM candidat WHERE code=?", (line[0],))

        res = cur.fetchall()

        #       if we already have a candidate, we juste update it's value
        if res:
            # value de rang?
            query = "UPDATE candidat SET civ_lib=?, nom=?, prenom=?, ad_1=?, ad_2=?, cod_pos=?, com=?, pay_adr=?, email=?, tel=?, por=?, resultat=?, code_voie=?, rang=? WHERE code=?"
            cur.execute(query, (
                line[1], cividico.get(line[2]), line[3], line[4], line[5], line[6], id_commune, id_contry, line[9],
                pars.telephone(line[10]), pars.telephone(line[11]), code_resultat,code_voie, line[12], line[0],))
            # else we create a new one
        else:
            query = "INSERT INTO candidat(code, civ_lib, nom, prenom, ad_1, ad_2, cod_pos, com, pay_adr, email, tel, por, resultat, code_voie, rang) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cur.execute(query, (
                line[0], line[1], cividico.get(line[2]), line[3], line[4], line[5], line[6], id_commune, id_contry,
                line[9], pars.telephone(line[10]), pars.telephone(line[11]), code_resultat, code_voie, line[12],))
        con.commit()
    con.close()

def UploadOralEcrit(liste, typeExam : str = "ecrit"):
    assert os.path.exists(DB_PATH), "database not found"
    con = sqlite3.connect(DB_PATH)

    code_voie = AddVoie(pars.findVoie(liste[0]), con)
    data = liste[2:]
    m = AddCivilite("M.", con)
    mme = AddCivilite("Mme", con)
    cividico = {
        "M.": m,
        "Mme": mme
    }
    cur = con.cursor()
    for line in data:
        # we check if the data exist already

        id_commune = AddCommune(line[7], con)
        id_contry = AddCountry(line[8], con)


        cur.execute("SELECT code FROM candidat WHERE code=?", (line[0],))

        res = cur.fetchall()

        #       if we already have a candidate, we juste update it's value
        if res:
            # value de rang?
            query = "UPDATE candidat SET civ_lib=?, nom=?, prenom=?, ad_1=?, ad_2=?, cod_pos=?, com=?, pay_adr=?, email=?, tel=?, por=?,code_voie=? WHERE code=?"
            cur.execute(query, (
                line[1], cividico.get(line[2]), line[3], line[4], line[5], line[6], id_commune, id_contry, line[9],
                pars.telephone(line[10]), pars.telephone(line[11]), code_voie, line[0],))
            # else we create a new one
        else:
            query = "INSERT INTO candidat(code, civ_lib, nom, prenom, ad_1, ad_2, cod_pos, com, pay_adr, email, tel, por, code_voie) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cur.execute(query, (
                line[0], line[1], cividico.get(line[2]), line[3], line[4], line[5], line[6], id_commune, id_contry,
                line[9], pars.telephone(line[10]), pars.telephone(line[11]), code_voie,))
        # update du rang de la catégorie
        ty = AddTypeExam(typeExam, con)
        mat = AddMatiere("rang", con)

        cur.execute("INSERT OR REPLACE INTO notes(can_code, matiere_id, type_id, value) VALUES(?,?,?,?)", (line[0], mat, ty, line[12],))
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
        query = "INSERT OR REPLACE INTO ecole(code, nom) VALUES(?,?)"
        cur.execute(query, (line[0], line[1],))
        con.commit()
    con.close()


#
def UploadNote(liste, typeExam: str = "ecrit"):
    """fonction a utiliser pour upload les fichiers de ResulttatEcrit, ResultatOral et CMT_Oral
    type exam is a string that correspond to a type of exam such a written, oral, ..."""
    assert os.path.exists(DB_PATH), "database not found"

    data = liste[3:]
    con = sqlite3.connect(DB_PATH)

    id_matiere = []
    typeE = AddTypeExam(typeExam, con)
    for i in range(1, len(liste[1])):

        if liste[1][i]:
            id_matiere.append(AddMatiere(liste[1][i], con, liste[2][i]))

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "INSERT OR REPLACE INTO notes(can_code, matiere_id,type_id, value) VALUES(?,?,?,?)"
    for line in data:
        if typeExam == "cmt":
            UpdateVoieCandidat(liste[0],line[0])
        for i in range(1, len(line)):
            if line[i]:
                cur.execute(query, (line[0], id_matiere[i - 1], typeE, line[i],))
        con.commit()
    con.close()


def UpdateVoieCandidat(filename: str, can_code, connection):
    # add the commune to the bdd if it doesn't exist and return it's code
    voie = AddVoie(pars.findVoie(filename), connection)
    if not voie:
        return None


    cur = connection.cursor()

    cur.execute("SELECT code FROM candidat WHERE code=?", (can_code,))
    res = cur.fetchall()

    if not res:
        cur.execute("INSERT INTO candidat(code,code_voie) VALUES(?,?)", (can_code, voie,))
        res = cur.fetchall()
    else:
        cur.execute("UPDATE candidat SET code_voie=? WHERE code =?", (voie,can_code,))
    connection.commit()

    return res[0][0]
