#! /usr/local/bin/python3
import click
import sqlite3
import os
import sys


@click.command()
@click.argument('file_path', default='../bdd/ScriptCreationTables.txt', type=click.Path(exists=True))
@click.argument('database_path', default='../bdd/project.db')
def BDDcreation(file_path, database_path):
    # open the file and retrieve it's content
    f = open(file_path)

    line = f.readline()
    content = ""

    while line:
        # if we found the commentary mark in the line, we select everything at it's left
        # else we select te entire line
        pos = line.find("//")
        if pos != -1:
            line = line[0:pos]
        print(line)
        content = content + line

        line = f.readline()
    f.close()

    # we separate the different query
    requests = content.split(";")

    #   we check if the database is already existing
    # if it exist we let the user choose if he wants it to be deleted to continue
    if os.path.exists(database_path):
        val = input("database already exist, do you want to delete it to continue (Y/N) : ")
        if val != "Y" and val != "y":
            sys.exit("Refused to delete database -> aborting script")

        os.remove(database_path)

    con = sqlite3.connect(database_path)
    cur = con.cursor()

    for query in requests:
        # we check if the query is not empty
        if query.strip():
            cur.execute(query)

    con.commit()

    con.close()


if __name__ == "__main__":
    BDDcreation()
