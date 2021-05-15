import sqlite3
import sys
import ParserDonnee as pars

# ------------------- Fonctions parsant les différents fichiers -------------------

DB_PATH = "../bdd/project.db"


def pars_inscription(file: list):
    name = file[0]
    if name.split("/")[-1] != "Inscription.xlsx":
        print("Attention, ce n'est peut-être pas le bon fichier", file=sys.stderr)
    nom_champs = file[2]  # En-tête : contient le nom de chaque colonne (fichier[1] vide)
    list_champ = []
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    for line in file[3:]:
        champ = {"code": line[0],  # int,
                 "nom": line[1],
                 "prenom": line[2],
                 "autre_prenoms": line[3],
                 "civ_lib": line[4],  # int
                 "date_naissance": line[5],
                 "ville_naissance": line[6],
                 "code_pays_naissance": line[7],  # int
                 "pays_naissance": line[8],
                 "francais": line[9],  # int,
                 "code_pay_natio": line[10],  # int,
                 "autre_natio": line[11],
                 "ad_1": line[12],
                 "ad_2": line[13],
                 "cod_pos": line[14],  # int,
                 "ville": line[15],
                 "code_pays": line[16],  # int,
                 "lib_pays": line[17],
                 "tel": pars.telephone(line[18]),
                 "por": pars.telephone(line[19]),
                 "mel": line[20],
                 "classe": line[21],
                 "puissance": line[22],
                 "code_etabl": line[23],  # int,
                 "etabl": line[24],
                 "ville_etabl": line[25],
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
                 "lib_csp_pere": line[46],
                 "cod_csp_mere": line[47],  # int,
                 "lib_csp_mere": line[48],
                 "code_etat_dossier": line[49],  # int,
                 "lib_etat_dossier": line[50],
                 "arr_naissance": line[51],  # int,
                 "handicap": line[52],
                 "qualite": line[53],
                 "can_dep_bac": line[54],  # int
                 }
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
