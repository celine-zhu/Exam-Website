import sqlite3
import sys
from ParserDonnee import *

# DB_PATH = "../bdd/project.db"

# Ce fichier contient des fonctions servant vérifier la cohérence des données de la DB
# Exemple: vérifier dans les champ sensé contenir des mails que ce sont des mails, idem pour numéro de téléphone, etc...


def verifChampMail(DB_PATH):
    """ Vérifier que les champs sensé contenir des mails contienne uniquement des mails

    :return: Le nombre de mail non valide, 0 si tous valide
    """

    count_not_valid = 0

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute(f"SELECT email FROM candidat")
    res = cur.fetchall()
    for entrie in res:
        email = entrie[0]
        if checkMail(email) != 0:
            count_not_valid += 1
            print(f"Attention, le mail '{email}' semble de pas être valide", file=sys.stderr)
    if count_not_valid == 0:
        print("Tous les emails vérifiés sont valides")
    else:
        print(f"Attention, {count_not_valid} mail(s) semble(nt) de pas être valide", file=sys.stderr)

    con.commit()

    con.close()

    return count_not_valid


verifChampMail("../bdd/project.db")
