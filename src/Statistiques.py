import sqlite3

# Fichier contenant des fonctions de statistiques

DB_PATH = "../bdd/project.db"


def moyenne_epreuve(epreuve, etabl=None):
    """Fonction qui renvoie la moyenne pour une épreuve donné

    :param epreuve: Nom de l'épreuve ou code de l'épreuve
    :param etabl: Lieu où a été passé l'épreuve
    :return: Moyenne de l'épreuve
    """

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

    if etabl is None:
        cur.execute(f"SELECT {'value'} FROM notes WHERE matiere_id=?", code_epreuve)
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
