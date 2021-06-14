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
    file2function_association = [[UploadEcole, findFileByname(filelist, 'listeecoles')],
                                [UploadEtabli, findFileByname(filelist, 'listeetablissements')],
                                [UploadListReponse, findFileByname(filelist, 'listeetatsreponsesappel')],

                                [UploadInscription, findFileByname(filelist, 'inscription')],

                                [UploadAdm, findFileByname(filelist, 'admissible_'), 'admissible'],

                                [UploadClasse, findFileByname(filelist, 'classes_', 'scei')],
                                [UploadSCEI, findFileByname(filelist, 'scei')],
                                [UploadOralEcrit, findFileByname(filelist, 'ecrit_', anypose=False), 'ecrit'],
                                [UploadOralEcrit, findFileByname(filelist, 'oral_', anypose=False), 'oral'],

                                [UploadAdm, findFileByname(filelist, 'admis_'), 'admis'],

                                [UploadListeVoeux, findFileByname(filelist, 'listevoeux_')],
                                [UploadNote, findFileByname(filelist, 'cmt_oraux')],
                                [UploadNote, findFileByname(filelist, 'resultatecrit_')],
                                [UploadNote, findFileByname(filelist, 'resultatoral_')]]

    total = len(filelist)
    index = 1
    for i in file2function_association:
        args = (len(i) == 3)
        for j in i[1]:
            print(str(index) + "/" + str(total) + "-- file : " + j)
            data = ReadFile(repository_path + j)
            if args:
                i[0](data, i[2])
            else:
                i[0](data)
            index = index + 1


def findFileByname(filelist, filetypename: str, exclude: str = '$£€', anypose: bool = True):
    filetype = []
    for i in filelist:
        pos = i.lower().find(filetypename)
        if ((pos != -1 and anypose) or pos == 0) and exclude not in i.lower():
            filetype.append(i)
    return filetype


if __name__ == "__main__":
    ImportRepository()
