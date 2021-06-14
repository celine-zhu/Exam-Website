from flask import Flask, Blueprint, render_template, abort, request, redirect, url_for
from flask import g
import pdfkit
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
# from reportlab.pdfgen.canvas import Canvas
import sqlite3
app = Flask(__name__, static_folder='static', template_folder='templates')
DATABASE = "../../bdd/project.db"


def getdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def Index():
    return render_template('index.html')
@app.route('/test')
def test():
    list=[1,2,3]
    return render_template('test.html',list=list)


@app.route('/Candidat/<name>')

def Candidat(name):
    db = getdb()
    user = db.execute("SELECT * FROM candidat WHERE code = ?", (name,)).fetchall()
    note=db.execute("SELECT * FROM notes WHERE can_code =? ORDER BY type_id ASC", (name,)).fetchall()
    ranginfo=db.execute("SELECT * FROM ranginfo WHERE rang_classe =? AND code_voie=?", (user[0][-3],user[0][31],)).fetchall()
    voeux=db.execute("SELECT * FROM voeux_ecole WHERE can_code =? ORDER BY voe_ord ASC", (name,)).fetchall()
    vo=[]
    n=[]
    for k in range(0, len(note)):
        m=db.execute("SELECT label FROM matiere WHERE matiere_id =?", (note[k][1],)).fetchone()
        t=db.execute("SELECT label FROM typeExam WHERE type_id =?", (note[k][2],)).fetchone()
        n.append([note[k],m,t])
    for j in voeux:
              vo.append([j,db.execute("SELECT nom FROM ecole WHERE code =?",(j[1],)).fetchall(),db.execute("SELECT Ata_lib FROM reponse WHERE Ata_cod =?", (j[4],)).fetchall()])
    if ranginfo==[]:
        ranginfo=[['','',''],'','','','','']
    if n==[]:
        n=[['','','',''],[''],['']]
    if vo==[]:
        vo=[[['','',''],[[['']]],[[['']]]]]
    return render_template( 'candidat.html', user=user,n=n, ranginfo=ranginfo,vo=vo )


@app.route('/Candidat',methods=['POST','GET'])
def candlogin():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        user=None
        db = getdb()
        error = None
        user = db.execute(
            "SELECT nom FROM candidat WHERE code = ?", (numero,)
        ).fetchone()
        if user is None:
                return render_template('error.html')
        elif user!=candidat:
                 error = '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
                 return error
             
        if error is None:
                return redirect(url_for('Candidat',name = candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    return render_template('candlogin.html', error=error)   
   
   
@app.route('/Candidat/<name>/edit')
def changinfo():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'




@app.route('/Prof')
def prof():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        user=None
        db = getdb()
        error = None
        user = db.execute(
            "SELECT nom FROM candidat WHERE code = ?", (numero,)
        ).fetchone()
        if user is None:
                return'''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
        elif user!=candidat:
                 error = '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
                 return error
             
        if error is None:
                return redirect(url_for('Prof',name = candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    return render_template('proflogin.html', error=error)     

@app.route('/Prof/<name>')
def etabl(name):
    db = getdb()
    rne= name
    etabl=db.execute("SELECT etabl_id,nom FROM etablissement WHERE rne = ?", (rne,)).fetchall()
    user = db.execute("SELECT code, nom, prenom FROM candidat WHERE code_etabl = ?", (etabl[0][0],)).fetchall()
    note=[]
    for j in range(0, len(user)):
        note.append(db.execute("SELECT * FROM notes WHERE can_code =? ORDER BY type_id ASC", (user[j][0],)).fetchall())
    n=[]
    if user==[]:
        return render_template("noneeleve.html",etabl=etabl,name=name)
    for k in range(0,len(note)) :
        l=[user[k]]
        for d in range(0,len(note[k])):
            m=db.execute("SELECT label FROM matiere WHERE matiere_id =?", (note[k][d][1],)).fetchone()
            t=db.execute("SELECT label FROM typeExam WHERE type_id =?", (note[k][d][2],)).fetchone()
            d=[m,t,note[k][d][-1]]
            l.append(d)
        n.append(l)
    k=len(user)
    return render_template( 'professeur.html', user=user, n=n, name=name, etabl=etabl,k=k)

@app.route('/Register')
def nouveau():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        user=None
        db = getdb()
        error = None
        user = db.execute(
            "SELECT nom FROM candidat WHERE code = ?", (numero,)
        ).fetchone()
        if user is None:
                return'''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
        elif user!=candidat:
                 error = '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
                 return error
             
        if error is None:
                return redirect(url_for('Candidat',name = candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    return render_template('newcand.html', error=error)    

@app.route('/Admin')
def Admin():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        user=None
        db = getdb()
        error = None
        if numero is None:
                return'''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
        elif user!=candidat:
                 error = '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
                 return error
             
        if error is None:
                return redirect(url_for('Admin/select',name = candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    return render_template('adminlogin.html', error=error)      
@app.route('/Admin/select')
def links():
    return render_template('adminselect.html')
@app.route('/Admin/SQL', methods=['POST','GET'])
def sql():
    selec = None
    fro=None
    a=None
    b=None
    resultat=None
    st=''
    if request.method == 'POST':
        
        if request.form['btn_identifier'] == 'chercher':
            selec = request.form.get("select")
            fro = request.form.get("table")
            if selec is None or fro is None:
                    return'''<div> Erreur, commande incomplète<div>
             <div> <a href="http://127.0.0.1:5000/Admin/SQL"> retour<div>'''
            a=request.form["A"]
            b=request.form["B"]
            db = getdb()
            cursor=db.cursor()
            if a=='' or b=='':
                st=str("SELECT "+selec+" FROM "+fro)
                resultat= db.execute(st).fetchall()
                result = cursor.execute(str("PRAGMA table_info("+fro+");")).fetchall()
                column_names = list(zip(*result))[1]
            else:
                st=str("SELECT"+selec+"FROM"+fro+" WHERE "+a+" = "+b)
                resultat = db.execute(st).fetchall()
                result = cursor.execute(str("PRAGMA table_info("+fro+");")).fetchall()
                column_names = list(zip(*result))[1]
            return render_template('adminsql.html', resultat=resultat,column_names=column_names, result=result)
        elif request.form['btn_identifier'] == 'commande':
            st=request.form.get("search")
            db=getdb()
            cursor=db.cursor()
            if st!=None:
                resultat=db.execute(str(st)).fetchall()
            if resultat is None:   
                return'''<div> Erreur, commande incomplète<div>
             <div> <a href="http://127.0.0.1:5000/Admin/SQL"> retour<div>'''
            return render_template('adminsql.html', resultat=resultat)
            
    return render_template('adminsql1.html')
@app.route('/Admin/Files')
def file():
    return
@app.route('/Admin/search',methods=['GET','POST'])
def search():
    resultat=[]
    if request.method == 'POST':
            st=request.form.get("search")
            db=getdb()
            ugh=str("SELECT nom, prenom,code FROM candidat WHERE prenom LIKE %"+st)
            resultat=db.execute(str(ugh)).fetchall()
            if len(resultat)>20:
                resultat=resultat[:20]
            li=[]
            for k in resultat:
                    t=str("http://127.0.0.1:5000/Candidat/"+k[2])
                    li.append([t,k])
            if resultat==[]:   
                     resultat.append("0 résultats trouvés")
            return render_template('adminsearch.html', resultat=resultat,li=li)  
    return render_template('adminsearch2.html', resultat=resultat)  
    
    
@app.route('/Credits')
def credit():
    return
@app.route('/Download')
@app.route('/Download/<name>')
def my_link():
    pdfkit.from_url('http://127.0.0.1:5000/', 'out.pdf')
    return 'Click.'
@app.route('/Curieux')
def images():
    return
if __name__ == '__main__':
    app.run(debug=True)
