import sqlite3
import statistics
import numpy

# Fichier contenant des fonctions de statistiques

DB_PATH = "../bdd/project.db"


def stats_epreuve(epreuve, ville_nai_=None, ville_res_=None, ville_ecrit_=None,
                  pays_nai_=None, pays_res_=None,
                  serie_bac_=None,
                  mention_bac_=None,
                  csp_pere_=None,
                  csp_mere_=None):
    """Fonction qui renvoie la moyenne pour une épreuve donné


    :param epreuve: Nom de l'épreuve ou code de l'épreuve
    :param ville_nai_: Ville de naissance du candidat
    :param ville_res_: Ville de résidence du candidat
    :param ville_ecrit_: Lieu où a été passé l'épreuve
    :param pays_nai_: Pays de naissance
    :param pays_res_: Pays de résidence
    :param serie_bac_: Série du bac
    :param mention_bac_: Mention obtenu au bac
    :param csp_pere_: Numéro ou libellé exact du CSP du père
    :param csp_mere_: Numéro ou libellé exact du CSP de la mère
    :return: Liste de note ou -1 si il n'y a pas de notes pour ces paramètres
    """

    liste_can = select_candidat(ville_nai=ville_nai_, ville_res=ville_res_, ville_ecrit=ville_ecrit_,
                                pays_nai=pays_nai_, pays_res=pays_res_,
                                serie_bac=serie_bac_,
                                mention_bac=mention_bac_,
                                csp_pere=csp_pere_,
                                csp_mere=csp_mere_)

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

    if len(liste_note) == 0:
        return -1
    else:
        return liste_note  # round(sum(liste_note) / len(liste_note), 2)


"""test: (donne tous 14.36)
print(moyenne_epreuve("mathématiques"))
print(moyenne_epreuve("961"))
print(moyenne_epreuve(961))"""


def stats_rang(classe=False, ville_nai_=None, ville_res_=None, ville_ecrit_=None,
               pays_nai_=None, pays_res_=None,
               serie_bac_=None,
               mention_bac_=None,
               csp_pere_=None,
               csp_mere_=None):
    """Fonction qui renvoie des stats sur le rang

    :param classe: True si c'est "rang_classe", False si c'est "rang"
    :param ville_nai_: Ville de naissance du candidat
    :param ville_res_: Ville de résidence du candidat
    :param ville_ecrit_: Lieu où a été passé l'épreuve
    :param pays_nai_: Pays de naissance
    :param pays_res_: Pays de résidence
    :param serie_bac_: Série du bac
    :param mention_bac_: Mention obtenu au bac
    :param csp_pere_: Numéro ou libellé exact du CSP du père
    :param csp_mere_: Numéro ou libellé exact du CSP de la mère
    :return: Liste de rang ou -1 si il n'y a pas de notes pour ces paramètres
    """

    liste_can = select_candidat(ville_nai=ville_nai_, ville_res=ville_res_, ville_ecrit=ville_ecrit_,
                                pays_nai=pays_nai_, pays_res=pays_res_,
                                serie_bac=serie_bac_,
                                mention_bac=mention_bac_,
                                csp_pere=csp_pere_,
                                csp_mere=csp_mere_)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    liste_rang = []
    res = []
    type_rang = "rang"
    if classe is True:
        type_rang = "rang_classe"

    if len(liste_can) != 0:
        str_excl = "(" + "?, " * len(liste_can)
        str_excl = str_excl[:-2] + ")"  # Ne marche pas sinon
        cur.execute(f"SELECT {type_rang} FROM candidat WHERE code IN {str_excl}", (*liste_can,))
        res = cur.fetchall()
    else:
        cur.execute(f"SELECT {type_rang} FROM candidat")
        res = cur.fetchall()

    for entrie in res:
        if entrie[0] is not None:
            liste_rang.append(entrie[0])

    con.close()

    if len(liste_rang) == 0:
        return -1
    else:
        return liste_rang  # round(sum(liste_rang) / len(liste_rang), 2)


def select_candidat(ville_nai=None, ville_res=None, ville_ecrit=None,
                    pays_nai=None, pays_res=None,
                    serie_bac=None,
                    mention_bac=None,
                    csp_pere=None,
                    csp_mere=None):
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

    if csp_pere is not None:
        code = False
        if type(csp_pere) is str:
            if csp_pere.isdecimal():
                code = True
                csp_pere = int(csp_pere)
        elif type(csp_pere) is int:
            code = True

        code_csp = csp_pere
        if not code:  # Si csp_pere est le libellé, on récupère son code
            cur.execute(f"SELECT code_csp FROM csp WHERE csp=?", (csp_pere,))
            res = cur.fetchall()
            code_csp = res[0][0]

        cur.execute(f"SELECT code FROM candidat WHERE code_csp_pere=?", (code_csp,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    if csp_mere is not None:
        code = False
        if type(csp_mere) is str:
            if csp_mere.isdecimal():
                code = True
                csp_mere = int(csp_mere)
        elif type(csp_mere) is int:
            code = True

        code_csp = csp_mere
        if not code:  # Si csp_pere est le libellé, on récupère son code
            cur.execute(f"SELECT code_csp FROM csp WHERE csp=?", (csp_mere,))
            res = cur.fetchall()
            code_csp = res[0][0]

        cur.execute(f"SELECT code FROM candidat WHERE code_csp_mere=?", (code_csp,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    con.close()
    return list_can


"""
for mention in ["TB", "B", "AB", "S"]:  # Exemple:
    print(moyenne(stats_epreuve(600, ville_ecrit_="Paris", pays_nai_="Maroc", mention_bac_=mention)))
"""


def statOfList(elements: list):
    infos = [
        statistics.mean(elements),
        numpy.quantile(elements, 0.25),
        numpy.quantile(elements, 0.75),
        statistics.median(elements),
        statistics.variance(elements)
    ]
    return infos


"""Test (résultat de ligne 2 et 3 identique)
print(statOfList(stats_rang()))
print(statOfList(stats_rang(csp_pere_=81, csp_mere_=85)))
print(statOfList(stats_rang(csp_pere_="Chômeurs n'ayant jamais travaillé", csp_mere_="Personnes diverses sans activité  professionnelle de moins de 60 ans (sauf retraités)")))
"""