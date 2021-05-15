# Fonctions permettant de parser des données précises
import sys

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
        return str_tel.replace("(0)","")  # Retire le "(0)"
    elif len_tel == 14:
        return "+33 " + str_tel[1:]  # Ajoute le "+33"
    elif len_tel == 10:
        new_tel = " ".join([str_tel[:2], str_tel[2:4], str_tel[4:6], str_tel[6:8], str_tel[8:10]])  # ajoute des " "
        return "+33 " + new_tel[1:]  # Ajoute le +33
    else:  # format non géré (n'est pas sensé arriver)
        print("Le numéro de téléphone n'est pas dans un format pris en compte", file=sys.stderr)
        return str_tel

"""
Test:
tel_possible = ['+33 (0)8 06 39 06 32', '05 94 40 87 21', '0256932111', '+33 5 49 50 46 69']
for tel in tel_possible:
    print("Avant: " + tel + "\nAprès: " + telephone(tel))
"""
