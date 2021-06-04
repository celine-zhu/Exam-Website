# Fonctions permettant de parser des données précises
import sys
import re

# format de tel géré ['+33 (0)8 06 39 06 32', '05 94 40 87 21', '0256932111', '+33 5 49 50 46 69']
# Longueurs: 1er = 20, 2ème = 14, 3ème = 10, 4ème = 17


def telephone(str_tel: str):
    """
    :param str_tel: Un numéro de téléphone  dans un format quelconque
    :return: Un numéro de téléphone format +33 X XX XX XX XX
    """
    if str_tel in ["", None]:  # Si le champ était vide
        return ""

    len_tel = len(str_tel)  # On trouve le format du tel suivant la longueur de la chaine de caractère

    if len_tel == 17:
        return str_tel  # Déjà dans le format souhaité
    elif len_tel == 20:
        return str_tel.replace("(0)", "")  # Retire le "(0)"
    elif len_tel == 14:
        return "+33 " + str_tel[1:]  # Ajoute le "+33"
    elif len_tel == 10:
        new_tel = " ".join([str_tel[:2], str_tel[2:4], str_tel[4:6], str_tel[6:8], str_tel[8:10]])  # ajoute des " "
        return "+33 " + new_tel[1:]  # Ajoute le +33
    else:  # format non géré (n'est pas sensé arriver)
        print("Le numéro de téléphone n'est pas dans un format pris en compte", file=sys.stderr)
        return str_tel


def findVoie(filename: str):
    if "_MP" in filename:
        return "MP"
    if "_PC" in filename:
        return "PC"
    if "_PSI" in filename:
        return "PSI"
    if "_PT" in filename:
        return "PT"
    if "_TSI" in filename:
        return "TSI"
    return None


"""
Test:
tel_possible = ['+33 (0)8 06 39 06 32', '05 94 40 87 21', '0256932111', '+33 5 49 50 46 69']
for tel in tel_possible:
    print("Avant: " + tel + "\nAprès: " + telephone(tel))
"""


def checkTelephoneFr(tel: str):
    """Check if tel is a phone number in the format +33 X XX XX XX XX

    :return 0 if its a phone number ine the correct format
    1 if its detected as a phone number but not in the good format
    -1 otherwise"""

    if tel[0] == "+":
        no_pref = tel[1:]
        if len(no_pref) == 16:
            num = no_pref.replace(" ", "")
            if num.isdecimal() and len(num) == 1:
                return 0
    # If we reach this code, tel wasn't in the correct format
    num = tel.replace(" ", "").replace("+", "").replace("(0)", "")
    if (num.startswith("33") and len(num) == 11) or (num.startswith("0") and len(num) == 10):
        return 1
    else:
        return -1


def checkMail(email: str):
    """Check if 'mail' is a valid mail : string1@string2.suffixe

    :param email: str to test
    :return: 0 if its a valid mail
    -1 otherwise
    """

    # Note: La vérification poussée de validité d'un mail est un vrai problème en raison de ce qui accepté par les RFC
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    res = re.findall(pattern, email)
    if len(res) == 1 and res[0] == email:
        return 0
    else:
        return -1


def checkDate(date):
    """Check if 'date' is a valid date : YYYYMM

    :param date: str to test
    :return: 0 if its a valid date
    -1 otherwise
    """

    if type(date) is int:
        if len(date) == 6:
            return 0
    if type(date) is str:
        if date.isdecimal() and len(date) == 6:
            return 0
    return -1
