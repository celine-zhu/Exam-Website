import sqlite3

DB_PATH = "../bdd/project.db"

#  -------- Fonctions ajoutant des données dans les tables auxilliaire + Fonction d'insertion général


def AjoutHandicap(hand: str) -> int:
    res = 0
    if hand == "oui":
        res = 1
    return res


def AddCSP(code: int, lib: str, connection):
    """Add the CSP to the DB if it doesn't exist, using his code as index. return its code"""

    data = {"code_csp": code, "csp": lib}
    code_csp = InsertData(data, "code_csp", "csp", "code_csp", connection)

    return code_csp


def AddTypeExam(name: str, connection):

    data = {"label": name.lower()}
    type_id = InsertData(data, "type_id", "typeExam", "label", connection)

    return type_id


def AddMatiere(name: str, connection, code=None):

    data = {"label": name.lower(), "code": code}
    matiere_id = InsertData(data, "matiere_id", "matiere", "label", connection)

    return matiere_id


def AddCommune(name: str, connection):
    """add the commune to the bdd if it doesn't exist and return it's code """

    data = {"commune": name}
    commune_index = InsertData(data, "commune_index", "commune", "commune", connection)

    return commune_index


def AddCountry(name: str,connection ,code: int=None):
    """ add the country to the bdd if it doesn't exist and return it's code """
    if code is not None:
        data = {"pays_code": code, "liste_pays": name}
    else:
        data = {"liste_pays": name}
    pays_code = InsertData(data, "pays_id", "pays", "liste_pays", connection)

    return pays_code


def AddResultat(name: str, connection):
    """ add the result of the admission to the bdd if it doesn't exist and return it's code"""

    data = {"resultat": name}
    resultat_index = InsertData(data, "resultat_index", "resultat", "resultat", connection)
    return resultat_index


def AddEtabl(code: str, name: str, ville: str, connection):

    data = {"rne": code, "nom": name, "ville": ville}
    etabl_id = InsertData(data, "etabl_id", "etablissement", "rne", connection)
    return etabl_id


def AddCivilite(name: str, connection):
    """ add the civilite to the bdd if it doesn't exist and return it's code """

    data = {"civilite": name}
    civilite_index = InsertData(data, "civilite_index", "civilite", "civilite", connection)
    return civilite_index


def AddEtatDossier(code: str, name: str, connection):

    data = {"code_etat_dossier": code, "etat_dossier": name}
    code_etat_dossier = InsertData(data, "code_etat_dossier", "etat_dossier", "code_etat_dossier", connection)
    return code_etat_dossier


def AddConcours(code: str, name: str, connection):

    data = {"code_concours": code, "concours": name}
    code_concours = InsertData(data, "code_concours", "concours", "code_concours", connection)
    return code_concours


def AddSerie(code: str, name: str, connection):

    data = {"code_serie": code, "serie": name}
    code_serie = InsertData(data, "code_serie", "seriebac", "code_serie", connection)
    return code_serie


def AddQualite(name: str, connection):

    data = {"qualite": name}
    code_qualite = InsertData(data, "code_qualite", "qualite", "qualite", connection)
    return code_qualite


def AddMention(name: str,connection):

    data = {"mention": name}
    code_mention = InsertData(data, "code_mention", "mention", "mention", connection)
    return code_mention


def AddPuissance(name: str, connection):

    data = {"puissance": name}
    code_puissance = InsertData(data, "code_puissance", "puissance", "puissance", connection)
    return code_puissance


def AddEpreuve(name: str, connection):
    if name is not None:
        data = {"epreuve": name}
        epreuve_code = InsertData(data, "epreuve_code", "epreuve", "epreuve", connection)
        return epreuve_code
    return None


def AddVoie(name: str, connection):
    """ add the voie to the bdd if it doesn't exist and return it's code"""
    if not name:
        return None
    data = {"voie": name}
    code_voie = InsertData(data, "code_voie", "voie", "voie", connection)
    return code_voie


def InsertData(data: dict, name_id: str, name_table: str, name_select: str, connection):
    """
    Insert data in the DB. This function generalize the code for insertion and avoid repetition of similar code

    :param data: Dict with an entrie for each entrie in the DB. Key=Name of the attribute / Value=Value of the attribute
    :param name_id: Attribute used as Primary Key
    :param name_table: Name of the table used
    :param name_select: Attribute used to check if the entrie already exist
    :return: Value used to reference the entrie in an other table
    """
    cur = connection.cursor()

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
    connection.commit()

    return res[0][0]


def InsertOrUpdateData(data: dict, name_id: str, name_table: str, name_select: str, connection):
    """
    Insert data in the DB. This function generalize the code for insertion and avoid repetition of similar code
    It update the DB if an entry with the same "name_id" already exist

    :param data: Dict with an entrie for each entrie in the DB. Key=Name of the attribute / Value=Value of the attribute
    :param name_id: Attribute used as Primary Key
    :param name_table: Name of the table used
    :param name_select: Attribute used to check if the entrie already exist
    :return: Value used to reference the entrie in an other table
    """
    cur = connection.cursor()

    cur.execute(f"SELECT {name_id} FROM {name_table} WHERE {name_select}=?", (data[name_select],))
    res = cur.fetchall()
    #       if we already have an entrie, it is updated with the new values
    if res:
        line_set = ""
        for e in data.keys():
            line_set += e + " = ?,"
        line_set = line_set[:-1]
        tmp = list(data.values())
        tmp.append(data[name_id])
        cur.execute(f"UPDATE {name_table} SET {line_set} WHERE {name_select}=?", tuple(tmp))
    else:
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
    connection.commit()

    return res[0][0]
