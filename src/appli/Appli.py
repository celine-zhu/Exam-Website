from flask import Flask, Blueprint, render_template, abort, request, redirect, url_for
from flask import g
import pdfkit
import Statistiques
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
# from reportlab.pdfgen.canvas import Canvas
import sqlite3
import numpy
import statistics
import Statistiques as St

app = Flask(__name__, static_folder='static', template_folder='templates')
DATABASE = "../../bdd/project.db"


def statOfList(elements: list):
    infos = [
        statistics.mean(elements),
        numpy.quantile(elements, 0.25),
        numpy.quantile(elements, 0.75),
        statistics.median(elements),
        statistics.variance(elements),
        min(elements),
        max(elements),
        len(elements)
    ]
    return infos


def getdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def Index():
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('index.html'))
    return render_template('index.html')


@app.route('/test')
def test():
    list_ = [1, 2, 3]
    return render_template('test.html', list=list_)


@app.route('/Candidat/<code>')
def Candidat(code):
    db = getdb()
    user = db.execute("SELECT * FROM candidat WHERE code = ?", (code,)).fetchall()

    if user is None or user == []:
        print(code, " n'existe pas")
        return render_template('candidat_error.html', code=code)

    note = db.execute("SELECT * FROM notes WHERE can_code =? ORDER BY type_id ASC", (code,)).fetchall()
    ranginfo = db.execute("SELECT * FROM ranginfo WHERE rang_classe =? AND code_voie=?",
                          (user[0][-3], user[0][31],)).fetchall()
    voeux = db.execute("SELECT * FROM voeux_ecole WHERE can_code =? ORDER BY voe_ord ASC", (code,)).fetchall()
    vo = []
    n = []
    for k in range(0, len(note)):
        m = db.execute("SELECT label FROM matiere WHERE matiere_id =?", (note[k][1],)).fetchone()
        t = db.execute("SELECT label FROM typeExam WHERE type_id =?", (note[k][2],)).fetchone()
        n.append([note[k], m, t])
    for j in voeux:
        vo.append([j, db.execute("SELECT nom FROM ecole WHERE code =?", (j[1],)).fetchall(),
                   db.execute("SELECT Ata_lib FROM reponse WHERE Ata_cod =?", (j[4],)).fetchall()])

    handicap = "Non"
    if user[0][40] == 1:
        handicap = "Oui"

    datebac = user[0][32]
    if datebac is not None:
        datebac = str(datebac)
        datebac = datebac[:4] + "/" + datebac[4:]

    lib_user = [db.execute("SELECT civilite FROM civilite WHERE civilite_index=?", (user[0][1],)).fetchall(),
                db.execute("SELECT commune FROM commune WHERE commune_index=?", (user[0][7],)).fetchall(),
                db.execute("SELECT liste_pays FROM pays WHERE pays_id=?", (user[0][8],)).fetchall(),
                db.execute("SELECT commune FROM commune WHERE commune_index=?", (user[0][13],)).fetchall(),
                db.execute("SELECT liste_pays FROM pays WHERE pays_id=?", (user[0][14],)).fetchall(),
                db.execute("SELECT puissance FROM puissance WHERE code_puissance=?", (user[0][19],)).fetchall(),
                db.execute("SELECT nom FROM etablissement WHERE etabl_id=?", (user[0][20],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][21],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][22],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][23],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][24],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][25],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][26],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][27],)).fetchall(),
                db.execute("SELECT epreuve FROM epreuve WHERE epreuve_code=?", (user[0][28],)).fetchall(),
                db.execute("SELECT commune FROM commune WHERE commune_index=?", (user[0][29],)).fetchall(),
                db.execute("SELECT concours FROM concours WHERE code_concours=?", (user[0][30],)).fetchall(),
                db.execute("SELECT voie FROM voie WHERE code_voie=?", (user[0][31],)).fetchall(),
                db.execute("SELECT serie FROM seriebac WHERE code_serie=?", (user[0][33],)).fetchall(),
                db.execute("SELECT mention FROM mention WHERE code_mention=?", (user[0][34],)).fetchall(),
                db.execute("SELECT csp FROM csp WHERE code_csp=?", (user[0][37],)).fetchall(),
                db.execute("SELECT csp FROM csp WHERE code_csp=?", (user[0][38],)).fetchall(),
                db.execute("SELECT etat_dossier FROM etat_dossier WHERE code_etat_dossier=?",
                           (user[0][39],)).fetchall(),
                handicap,
                db.execute("SELECT qualite FROM qualite WHERE code_qualite=?", (user[0][41],)).fetchall()]

    # Contient les infos indirectement contenu dans "user"

    print(ranginfo)

    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('candidat.html', user=user, n=n, ranginfo=ranginfo, vo=vo, lib_user=lib_user,
                                datebac=datebac))
    return render_template('candidat.html', user=user, n=n, ranginfo=ranginfo, vo=vo, lib_user=lib_user,
                           datebac=datebac)


@app.route('/Candidat', methods=['POST', 'GET'])
def candlogin():
    error = None
    if request.method == 'POST':
        candidat: str = request.form["candidat"]
        numero: str = request.form["numero"]

        db = getdb()
        user = None
        error = "Erreur : Numéro ou nom de candidat incorrect"

        if numero is None or numero == "":
            if candidat is not None:
                user = db.execute(
                    "SELECT code FROM candidat WHERE nom = ?", (candidat.upper(),)
                ).fetchall()
                if user is not None and user != []:
                    print("user:", user)
                    numero = user[0][0]

        if numero is not None:
            user = db.execute(
                "SELECT code FROM candidat WHERE code = ?", (numero,)
            ).fetchall()
            if user is not None and user != []:
                return redirect(url_for('Candidat', code=numero))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('candlogin.html', error=error))
    return render_template('candlogin.html', error=error)


@app.route('/Prof')
def prof():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        user = None
        db = getdb()
        error = None
        user = db.execute(
            "SELECT nom FROM candidat WHERE code = ?", (numero,)
        ).fetchone()
        if user is None:
            return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
        elif user != candidat:
            error = '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
            return error

        if error is None:
            return redirect(url_for('Prof', name=candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('proflogin.html', error=error))
    return render_template('proflogin.html', error=error)


@app.route('/Prof/<name>')
def etablissement(name):
    db = getdb()
    rne = name
    etabl = db.execute("SELECT etabl_id,nom FROM etablissement WHERE rne = ?", (rne,)).fetchall()
    user = db.execute("SELECT code, nom, prenom FROM candidat WHERE code_etabl = ?", (etabl[0][0],)).fetchall()
    note = []
    for j in range(0, len(user)):
        note.append(db.execute("SELECT * FROM notes WHERE can_code =? ORDER BY type_id ASC", (user[j][0],)).fetchall())
    n = []
    if not user:  # idem à '== []'
        with open("./static/some_new_file.html", "w") as f:
            f.write(render_template("noneeleve.html", etabl=etabl, name=name))
        return render_template("noneeleve.html", etabl=etabl, name=name)
    for k in range(0, len(note)):
        l = [user[k]]
        for d in range(0, len(note[k])):
            m = db.execute("SELECT label FROM matiere WHERE matiere_id =?", (note[k][d][1],)).fetchone()
            t = db.execute("SELECT label FROM typeExam WHERE type_id =?", (note[k][d][2],)).fetchone()
            d = [m, t, note[k][d][-1]]
            l.append(d)
        n.append(l)
    k = len(user)
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('professeur.html', user=user, n=n, name=name, etabl=etabl, k=k))
    return render_template('professeur.html', user=user, n=n, name=name, etabl=etabl, k=k)


@app.route('/Register')
def nouveau():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        user = None
        db = getdb()
        error = None
        user = db.execute(
            "SELECT nom FROM candidat WHERE code = ?", (numero,)
        ).fetchone()
        if user is None:
            return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
        elif user != candidat:
            error = '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
            return error

        if error is None:
            return redirect(url_for('Candidat', name=candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('newcand.html', error=error))
    return render_template('newcand.html', error=error)


@app.route('/Admin')
def Admin():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        user = None
        db = getdb()
        error = None
        if numero is None:
            return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
        elif user != candidat:
            error = '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
            return error

        if error is None:
            return redirect(url_for('Admin/select', name=candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('adminlogin.html', error=error))
    return render_template('adminlogin.html', error=error)


@app.route('/Admin/select')
def links():
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('adminselect.html'))
    return render_template('adminselect.html')


@app.route('/Admin/SQL', methods=['POST', 'GET'])
def sql():
    selec = None
    fro = None
    a = None
    b = None
    resultat = None
    st = ''
    if request.method == 'POST':

        if request.form['btn_identifier'] == 'chercher':
            selec = request.form.get("select")
            fro = request.form.get("table")
            if selec is None or fro is None:
                return '''<div> Erreur, commande incomplète<div>
             <div> <a href="http://127.0.0.1:5000/Admin/SQL"> retour<div>'''
            a = request.form["A"]
            b = request.form["B"]
            db = getdb()
            cursor = db.cursor()
            if a == '' or b == '':
                st = str("SELECT " + selec + " FROM " + fro)
                resultat = db.execute(st).fetchall()
                result = cursor.execute(str("PRAGMA table_info(" + fro + ");")).fetchall()
                column_names = list(zip(*result))[1]
            else:
                st = str("SELECT" + selec + "FROM" + fro + " WHERE " + a + " = " + b)
                resultat = db.execute(st).fetchall()
                result = cursor.execute(str("PRAGMA table_info(" + fro + ");")).fetchall()
                column_names = list(zip(*result))[1]
            output_from_parsed_template = render_template('adminsql.html', resultat=resultat, column_names=column_names,
                                                          result=result)
            with open("./static/some_new_file.html", "w") as f:
                f.write(output_from_parsed_template)
            return render_template('adminsql.html', resultat=resultat, column_names=column_names, result=result)
        elif request.form['btn_identifier'] == 'commande':
            st = request.form.get("search")
            db = getdb()
            cursor = db.cursor()
            if st is not None:
                resultat = db.execute(str(st)).fetchall()
            if resultat is None:
                return '''<div> Erreur, commande incomplète<div>
             <div> <a href="http://127.0.0.1:5000/Admin/SQL"> retour<div>'''
            with open("./static/some_new_file.html", "w") as f:
                f.write(render_template('adminsql.html', resultat=resultat))
            return render_template('adminsql.html', resultat=resultat)
    return render_template('adminsql1.html')


@app.route('/Admin/Files')
def file():
    return


@app.route('/Admin/search', methods=['GET', 'POST'])
def search():
    resultat = None
    st = ''
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'commande':
            st = request.form.get("victor")
            db = getdb()
            cursor = db.cursor()
            resultat = cursor.execute("SELECT nom, prenom, code from candidat where prenom like ? ",
                                      ('%' + st + '%',)).fetchall()
            if len(resultat) > 100:
                resultat = resultat[:100]
            li = []
            for k in resultat:
                t = str("http://127.0.0.1:5000/Candidat/" + str(k[2]))
                li.append([t, k])
            if resultat is None:
                resultat = [["http://127.0.0.1:5000/Admin/search", ["0 résultats trouvés", " "]]]
            with open("./static/some_new_file.html", "w") as f:
                f.write(render_template('adminsearch.html', resultat=resultat, li=li))
            return render_template('adminsearch.html', resultat=resultat, li=li)
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('adminsearch2.html', resultat=resultat))
    return render_template('adminsearch2.html', resultat=resultat)


@app.route('/Credits')
def credit():
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('credits.html'))
    return render_template('credits.html')


@app.route('/Download')
@app.route('/Download/<name>')
def my_link():
    pdfkit.from_url('http://127.0.0.1:5000/', 'out.pdf')
    return redirect(url_for('/'))


@app.route('/Curieux')
def stats_crit():
    cur = getdb()
    matlist = cur.execute("SELECT * FROM matiere").fetchall()
    excluded = ['rang', 'total', 'bonification', 'centre', 'jury', 'rang ccp']
    epreuves = []
    for i in matlist:
        if i[1] not in excluded:
            epreuves.append(i)

    ville = []
    res = cur.execute("SELECT commune FROM commune").fetchall()
    for entrie in res:
        ville.append(entrie[0])

    pays = []
    res = cur.execute("SELECT liste_pays FROM pays").fetchall()
    for entrie in res:
        pays.append(entrie[0])

    serie = []
    res = cur.execute("SELECT serie FROM seriebac").fetchall()
    for entrie in res:
        serie.append(entrie[0])

    mention = []
    res = cur.execute("SELECT mention FROM mention").fetchall()
    for entrie in res:
        mention.append(entrie[0])

    csp = []
    res = cur.execute("SELECT csp FROM csp").fetchall()
    for entrie in res:
        csp.append(entrie[0])

    return render_template("curieux.html", epreuves=epreuves, ville=ville, pays=pays, serie=serie, mention=mention,
                           csp=csp)


@app.route('/curieux_stats', methods=["GET"])
def curieux_stats():
    choix = request.args.get('choix_c')

    list_critere = ["ville_nai", "ville_res", "ville_ecrit",
                    "pays_nai", "pays_res", "serie_bac",
                    "mention_bac", "csp_pere", "csp_mere"]
    args = {}

    for crit in list_critere:
        args[crit] = None

    for crit in list_critere:
        res = request.args.get(crit)
        if res:
            if res != "Ne pas prendre en compte":
                args[crit] = res
    error = None
    list_note = -1
    titre_stats = ""
    stats = []

    if choix == "epreuve_":
        epreuve = request.args.get('epreuve')
        if not epreuve:
            return "Erreur du nom de la matière"

        try:
            list_note = St.stats_epreuve(epreuve, *args.values())
        except sqlite3.OperationalError:
            error = "Impossible d'accéder à la base de donnée"
        titre_stats = "de la matière " + epreuve

    else:
        titre_stats = "du rang"
        type_rang = choix == "rang_c"
        if type_rang:
            titre_stats += " classé"
        try:
            list_note = St.stats_rang(type_rang, *args.values())
        except sqlite3.OperationalError:
            error = "Impossible d'accéder à la base de donnée"

    if list_note != -1:
        stats = St.statOfList(list_note)
        stats[0] = round(stats[0], 2)
        if type(stats[4]) is float:
            stats[4] = round(stats[4], 2)
    else:
        if choix == "epreuve_":
            error = "Aucune note disponible"
        else:
            error = "Aucun rang disponible"

    return render_template('curieux_res.html', list=stats, type_stats=titre_stats, error=error)


@app.route('/statform')
def statform():
    cur = getdb()
    matlist = cur.execute("SELECT * FROM matiere").fetchall()
    excluded = ['rang', 'total', 'bonification', 'centre', 'jury', 'rang ccp']
    cleaned = []
    for i in matlist:
        if i[1] not in excluded:
            cleaned.append(i)
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('StatsForm.html', list=cleaned))
    return render_template('StatsForm.html', list=cleaned)


@app.route('/statmat', methods=["GET"])
def statmat():
    var = request.args.get('matiere')
    if not var:
        return "erreur du code de la matière"
    cur = getdb()
    values = cur.execute("SELECT value FROM notes WHERE matiere_id=?", (var,)).fetchall()
    mat = cur.execute("SELECT label FROM matiere WHERE matiere_id=?", (var,)).fetchall()
    cleaned = []
    for i in values:
        cleaned.append(i[0])
    stats = statOfList(cleaned)
    with open("./static/some_new_file.html", "w") as f:
        f.write(render_template('Statmat.html', list=stats, matiere=mat[0][0]))
    stats[0] = round(stats[0], 2)
    stats[4] = round(stats[4], 2)
    return render_template('Statmat.html', list=stats, matiere=mat[0][0])


if __name__ == '__main__':
    app.run(debug=True)
