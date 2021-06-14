import sqlite3

# Fichier contenant des fonctions de statistiques

DB_PATH = "../bdd/project.db"


def moyenne_epreuve(epreuve, ville_nai=None, ville_res=None, ville_ecrit=None):
    """Fonction qui renvoie la moyenne pour une épreuve donné

    :param epreuve: Nom de l'épreuve ou code de l'épreuve
    :param ville_nai: Ville de naissance du candidat
    :param ville_res: Ville de résidence du candidat
    :param ville_ecrit: Lieu où a été passé l'épreuve
    :return: Moyenne de l'épreuve ou -1 si il n'y a pas de notes pour ces paramètres
    """

    liste_can = []
    selec_can = False
    if not (ville_nai is None and ville_res is None and ville_ecrit is None):
        selec_can = True
        liste_can = select_candidat(ville_nai, ville_res, ville_ecrit)

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

    if selec_can is False or len(liste_can) == 0:
        cur.execute(f"SELECT {'value'} FROM notes WHERE matiere_id=?", code_epreuve)
        res = cur.fetchall()

    else:
        str_excl = "(" + "?, " * len(liste_can)
        str_excl = str_excl[:-2] + ")"  # Ne marche pas sinon
        cur.execute(f"SELECT {'value'} FROM notes WHERE matiere_id=? AND can_code IN {str_excl}", (code_epreuve[0], *liste_can))
        res = cur.fetchall()

    for entrie in res:
        if entrie[0] != 99.99:
            liste_note.append(entrie[0])

    con.close()
    print(liste_note)
    return round(sum(liste_note)/len(liste_note), 2)


"""test: (donne tous 14.36)
print(moyenne_epreuve("mathématiques"))
print(moyenne_epreuve("961"))
print(moyenne_epreuve(961))"""


def select_candidat(ville_nai=None, ville_res=None, ville_ecrit=None):
    list_can = []

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    if ville_nai is not None:
        cur.execute(f"SELECT code FROM candidat WHERE code_ville_naissance=(SELECT commune_index FROM commune WHERE commune=?)", (ville_nai,))
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
        cur.execute(f"SELECT code FROM candidat WHERE code_ville_ecr=(SELECT commune_index FROM commune WHERE commune=?)",
                    (ville_ecrit,))
        res = cur.fetchall()

        for entrie in res:
            if entrie[0] not in list_can:
                list_can.append(entrie[0])

    con.close()
    return list_can


print(moyenne_epreuve(600, ville_res="Meunier"))
