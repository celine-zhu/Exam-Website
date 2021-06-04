from ParserFichiers import UploadInscription, UploadEtabli
from LectureV2 import lectxl
import sqlite3
from AjoutDonnee import *

PATH_DB = "../bdd/project.db"
PATH_FILE_INSC = "../data/examples/Inscription_e.xlsx"
PATH_FILE_ETABL = "../data/public/listeEtablissements.xlsx"

file_insc = lectxl(PATH_FILE_INSC)
file_etabl = lectxl(PATH_FILE_ETABL)

UploadInscription(file_insc)
UploadEtabli(file_etabl)

con = sqlite3.connect(PATH_DB)
cur = con.cursor()
cur.execute("SELECT * FROM candidat WHERE code=?", (53621,))

res = cur.fetchall()[0]

code_ville_naissance = AddCommune("Calais")
code_pays_naissance = AddCountry("Maroc")
code_com = AddCommune("Jacquotboeuf")
code_puissance = AddPuissance("5/2")
code_etabl = AddEtabl("835320", "Institut Christophe Roy-Schmitt", "Leveque-sur-Mer")
code_ville_ecr = AddCommune("Lille")
code_concours = AddConcours("177", "Concours Mines-Télécom")
code_voie = AddVoie("PSI")
code_serie = AddSerie("1", "S Scientifique")
code_mention = AddMention("TB")
code_csp_pere = AddCSP(38, "Ingénieurs et cadres techniques d'entreprise")
code_csp_mere = AddCSP(31, "Professions libérales")
code_etat_dossier = AddEtatDossier("4", "Enregistrés")
code_handicap = AjoutHandicap("non")
code_qualite = AddQualite(' ')

epreuve_1 = AddEpreuve("Langue vivante écrite")
option_1 = AddEpreuve("Anglais")
epreuve_2 = AddEpreuve(None)
option_2 = AddEpreuve(None)
epreuve_3 = AddEpreuve(None)
option_3 = AddEpreuve(None)
epreuve_4 = AddEpreuve(None)
option_4 = AddEpreuve(None)

print(res)

cand_53621 = (53621, 1, 'DIAS', 'Louis-Marie', None, '05/11/1999', 0, code_ville_naissance, code_pays_naissance, 0, '806, chemin Maurice', None, 45569, code_com, None, 162, '+33 8 06 39 06 32', '+33 5 94 40 87 21', 'dorotheebuisson@charles.com', code_puissance, code_etabl, epreuve_1, option_1, None, None, None, None, None, None, code_ville_ecr, code_concours, code_voie, 201706, code_serie, code_mention, 'Modélisation d’un réfrigérateur thermoacoustique\n', '0833465573C', code_csp_pere, code_csp_mere, code_etat_dossier, code_handicap, code_qualite, 62, None, None, None, None)

print(cand_53621)

assert cand_53621 == res

con.close()
