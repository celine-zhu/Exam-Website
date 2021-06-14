import sqlite3

# Fichier contenant des fonctions de statistiques

DB_PATH = "../bdd/project.db"


def moyenne_epreuve(epreuve, ville_nai_=None, ville_res_=None, ville_ecrit_=None,
                    pays_nai_=None, pays_res_=None,
                    serie_bac_=None,
                    mention_bac_=None):
    """Fonction qui renvoie la moyenne pour une épreuve donné

    :param epreuve: Nom de l'épreuve ou code de l'épreuve
    :param ville_nai_: Ville de naissance du candidat
    :param ville_res_: Ville de résidence du candidat
    :param ville_ecrit_: Lieu où a été passé l'épreuve
    :param pays_nai_: Pays de naissance
    :param pays_res_: Pays de résidence
    :param serie_bac_: Série du bac
    :param mention_bac_: Mention obtenu au bac
    :return: Moyenne de l'épreuve ou -1 si il n'y a pas de notes pour ces paramètres
    """

    liste_can = select_candidat(ville_nai=ville_nai_, ville_res=ville_res_, ville_ecrit=ville_ecrit_,
                                pays_nai=pays_nai_, pays_res=pays_res_,
                                serie_bac=serie_bac_,
                                mention_bac=mention_bac_)

    code = False
    if type(epreuve) is str:
        if epreuve.isdecimal():
            code = True
            epreuve = int(epreuve)
    elif type(epreuve) is int:
        code = True
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    if code:
        cur.execute(f"SELECT matiere_id FROM matiere WHERE code=?", (epreuve,))
    else:
        cur.execute(f"SELECT matiere_id FROM matiere WHERE label=?", (epreuve,))
    res = cur.fetchall()

    code_epreuve = res[0]

    liste_note = []

    if len(liste_can) == 0:
        cur.execute(f"SELECT {'value'} FROM notes WHERE matiere_id=?", code_epreuve)
        res = cur.fetchall()

    else:
        str_excl = "(" + "?, " * len(liste_can)
        str_excl = str_excl[:-2] + ")"  # Ne marche pas sinon
        cur.execute(f"SELECT {'value'} FROM notes WHERE matiere_id=? AND "
                    f"can_code IN {str_excl}", (code_epreuve[0], *liste_can))
        res = cur.fetchall()

    for entrie in res:
        if entrie[0] != 99.99:
            liste_note.append(entrie[0])

    con.close()
    return round(sum(liste_note) / len(liste_note), 2)


"""test: (donne tous 14.36)
print(moyenne_epreuve("mathématiques"))
print(moyenne_epreuve("961"))
print(moyenne_epreuve(961))"""


def select_candidat(ville_nai=None, ville_res=None, ville_ecrit=None,
                    pays_nai=None, pays_res=None,
                    serie_bac=None,
                    mention_bac=None):
    list_can = []

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    if ville_nai is not None:
        cur.execute(f"SELECT code FROM candidat WHERE code_ville_naissance="
                    f"(SELECT commune_index FROM commune WHERE commune=?)", (ville_nai,))
        res = cur.fetchall()

        for entrie in res:
            list_can.append(entrie[0])

    if ville_res is not None:
        cur.execute(f"SELECT code FROM candidat WHERE com=(SELECT commune_index FROM commune WHERE commune=?)",
                    (ville_res,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    if ville_ecrit is not None:
        cur.execute(f"SELECT code FROM candidat WHERE code_ville_ecr="
                    f"(SELECT commune_index FROM commune WHERE commune=?)",
                    (ville_ecrit,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    if pays_nai is not None:
        cur.execute(f"SELECT code FROM candidat WHERE code_pays_naissance="
                    f"(SELECT pays_id FROM pays WHERE liste_pays=?)",
                    (pays_nai,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    if pays_res is not None:
        cur.execute(f"SELECT code FROM candidat WHERE pay_adr=(SELECT pays_id FROM pays WHERE liste_pays=?)",
                    (pays_res,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    if mention_bac is not None:
        cur.execute(f"SELECT code FROM candidat WHERE code_mention=(SELECT code_mention FROM mention WHERE mention=?)",
                    (mention_bac,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    if serie_bac is not None:
        cur.execute(f"SELECT code FROM candidat WHERE code_serie=(SELECT code_serie FROM seriebac WHERE serie=?)",
                    (serie_bac,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    con.close()
    return list_can


"""print(moyenne_epreuve(600, ville_ecrit_="Paris", pays_nai_="Maroc", mention_bac_="TB"))
print(moyenne_epreuve(600, ville_ecrit_="Paris", pays_nai_="Maroc", mention_bac_="B"))
print(moyenne_epreuve(600, ville_ecrit_="Paris", pays_nai_="Maroc", mention_bac_="AB"))
print(moyenne_epreuve(600, ville_ecrit_="Paris", pays_nai_="Maroc", mention_bac_="S"))"""
