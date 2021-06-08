#! /usr/local/bin/python3
import click
from src.ParserFichiers import *
from src.PolyMorph_Lecture import ReadFile
import os


@click.command()
@click.argument('repository_path', default='../data/public/', type=click.Path(exists=True))
@click.argument('database_path', default='../bdd/project.db')
def ImportRepository(repository_path, database_path):
    directoryInfo = os.listdir(repository_path)
    filelist = []
    for i in directoryInfo:
        if os.path.isfile(repository_path + i):
            filelist.append(i)

    file2function_association = []

    file2function_association.append([UploadEcole, findFileByname(filelist, 'listeecoles')])
    file2function_association.append([UploadEtabli, findFileByname(filelist, 'listeetablissements')])
    file2function_association.append([UploadListReponse, findFileByname(filelist, 'listeetatsreponsesappel')])

    file2function_association.append([UploadInscription, findFileByname(filelist, 'inscription')])
    file2function_association.append([UploadAdm, findFileByname(filelist, 'admissible_'), 'admissible'])
    file2function_association.append([UploadClasse, findFileByname(filelist, 'classes_', 'scei')])
    file2function_association.append([UploadSCEI, findFileByname(filelist, 'scei')])
    file2function_association.append([UploadOralEcrit, findFileByname(filelist, 'ecrit_'), 'ecrit'])
    file2function_association.append([UploadOralEcrit, findFileByname(filelist, 'oral_'), 'oral'])
    file2function_association.append([UploadAdm, findFileByname(filelist, 'admis_'), 'admis'])

    file2function_association.append([UploadListeVoeux, findFileByname(filelist, 'listevoeux_')])
    file2function_association.append([UploadNote, findFileByname(filelist, 'cmt_oraux')])
    file2function_association.append([UploadNote, findFileByname(filelist, 'resultatecrit_')])
    file2function_association.append([UploadNote, findFileByname(filelist, 'resultatoral_')])

    total = len(filelist)
    index = 1
    for i in file2function_association:
        args = (len(i) == 3)
        for j in i[1]:
            print(str(index) + "/" + str(total))
            data = ReadFile(repository_path + j)
            if args:
                i[0](data, i[2])
            else:
                i[0](data)
            index = index + 1


def findFileByname(filelist, filetypename: str, exclude: str = '$£€'):
    filetype = []
    for i in filelist:
        if i.lower().find(filetypename) == 0 and exclude not in i.lower():
            filetype.append(i)
    return filetype


if __name__ == "__main__":
    ImportRepository()
