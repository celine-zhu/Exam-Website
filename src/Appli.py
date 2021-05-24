from flask import Flask, Blueprint, render_template, abort, request, redirect, url_for
from flask import g
# from reportlab.pdfgen.canvas import Canvas
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')
DATABASE = "../bdd/project.db"


def getdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def Index():
    return render_template('index.html')



@app.route('/Candidat/<name>')
<<<<<<< HEAD
def Candidat(name):

    db = getdb()
    error = None
    user = db.execute(
            "SELECT * FROM candidat WHERE code = ?", (name,)
        ).fetchall()
    
    return 'template pour les infos à créer'


@app.route('/Candidat',methods=['POST','GET'])
def candlogin():
=======
def Candidat():
    return 'template pour les infos à créer'


@app.route('/Candidat', methods=['POST', 'GET'])
def cand():
>>>>>>> 49688cd407a2de761e45f8e103f8c6b459a7bfba
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
<<<<<<< HEAD
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
    return render_template('candlogin.html', error=error)   
   
   
=======
            return " numéro de candidat incorrect"
        elif user != candidat:
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            return redirect(url_for('Candidat', name=candidat))

        return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
    return render_template('cand.html', error=error)


>>>>>>> 49688cd407a2de761e45f8e103f8c6b459a7bfba
@app.route('/Candidat/<name>/edit')
def changinfo():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'


<<<<<<< HEAD
=======
@app.route('/Ecole')
@app.route('/Ecole/<name>')
def ecole():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'
>>>>>>> 49688cd407a2de761e45f8e103f8c6b459a7bfba


@app.route('/Prof')
@app.route('/Prof/<name>')
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
                return redirect(url_for('Candidat',name = candidat))

        """return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''"""
    return render_template('adminlogin.html', error=error)      


if __name__ == '__main__':
    app.run(debug=True)
