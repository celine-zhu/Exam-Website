import sqlite3

DB_PATH = "../bdd/project.db"

#  -------- Fonctions ajoutant des données dans les tables auxilliaire + Fonction d'insertion général


def AjoutHandicap(hand: str) -> int:
    res = 0
    if hand == "oui":
        res = 1
    return res


def AddCSP(code: int, lib: str):
    """Add the CSP to the DB if it doesn't exist, using his code as index. return its code"""

    data = {"code_csp": code, "csp": lib}
    code_csp = InsertData(data, "code_csp", "csp", "code_csp")

    return code_csp


def AddTypeExam(name: str):

    data = {"label": name.lower()}
    type_id = InsertData(data, "type_id", "typeExam", "label")

    return type_id


def AddMatiere(name: str, code=None):

    data = {"label": name.lower(), "code": code}
    matiere_id = InsertData(data, "matiere_id", "matiere", "label")

    return matiere_id


def AddCommune(name: str):
    """add the commune to the bdd if it doesn't exist and return it's code """

    data = {"commune": name}
    commune_index = InsertData(data, "commune_index", "commune", "commune")

    return commune_index


def AddCountry(name: str):
    """ add the country to the bdd if it doesn't exist and return it's code """

    data = {"liste_pays": name}
    pays_code = InsertData(data, "pays_code", "pays", "liste_pays")

    return pays_code


def AddResultat(name: str):
    """ add the result of the admission to the bdd if it doesn't exist and return it's code"""

    data = {"resultat": name}
    resultat_index = InsertData(data, "resultat_index", "resultat", "resultat")
    return resultat_index


def AddEtabl(code: str, name: str, ville: str):

    data = {"rne": code, "nom": name, "ville": ville}
    rne = InsertData(data, "rne", "etablissement", "nom")
    return rne


def AddCivilite(name: str):
    """ add the civilite to the bdd if it doesn't exist and return it's code """

    data = {"civilite": name}
    civilite_index = InsertData(data, "civilite_index", "civilite", "civilite")
    return civilite_index


def AddEtatDossier(code: str, name: str):

    data = {"code_etat_dossier": code, "etat_dossier": name}
    code_etat_dossier = InsertData(data, "code_etat_dossier", "etat_dossier", "code_etat_dossier")
    return code_etat_dossier


def AddQualite(name: str):

    data = {"qualite": name}
    code_qualite = InsertData(data, "code_qualite", "qualite", "qualite")
    return code_qualite


def AddVoie(name: str):
    """ add the voie to the bdd if it doesn't exist and return it's code"""

    data = {"voie": name}
    code_voie = InsertData(data, "code_voie", "voie", "voie")
    return code_voie


def InsertData(data: dict, name_id: str, name_table: str, name_select: str):
    """
    Insert data in the DB. THis function generalize the code for insertion and avoid repetition of similar code
    :param data: Dict with an entrie for each entrie in the DB. Key=Name of the attribute / Value=Value of the attribute
    :param name_id: Attribute used as Primary Key
    :param name_table: Name of the table used
    :param name_select: Attribute used to check if the entrie already exist
    :return: Value used to reference the entrie in an other table
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute(f"SELECT {name_id} FROM {name_table} WHERE {name_select}=?", (data[name_select],))
    res = cur.fetchall()
    if not res:
        str_excl = "(" + "?, " * len(data.keys())
        str_excl = str_excl[:-2] + ")"  # Ne marche pas sinon
        query = ""
        if len(data.keys()) > 1:
            query = f"INSERT INTO {name_table} {tuple(data.keys())} VALUES {str_excl}"
        else:
            query = f"INSERT INTO {name_table} ({list(data.keys())[0]}) VALUES {str_excl}"
        cur.execute(query, tuple(data.values()))
        cur.execute(f"SELECT {name_id} FROM {name_table} WHERE {name_select}=?", (data[name_select],))
        res = cur.fetchall()
    con.commit()

    con.close()
    return res[0][0]
