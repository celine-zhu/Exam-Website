from flask import Flask, Blueprint, render_template, abort, request,redirect, url_for
from flask import g
#from reportlab.pdfgen.canvas import Canvas
import sqlite3

app = Flask(__name__,  static_folder='static', template_folder='templates')
DATABASE= "../bdd/project.db"

def getdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def Index():
    return '''<div><h1>Je suis:</h1><div>
            <div> <a href="http://127.0.0.1:5000/Candidat">Un candidat </a><div>
            <div> <a href="http://127.0.0.1:5000/Prof"> Un professeur<div>
            <div> <a href="http://127.0.0.1:5000/Candidat"> Un nouveau candidat<div>
            '''

@app.route('/Candidat/<name>')
def Candidat():
    
    return 'template pour les infos à créer'
@app.route('/Candidat',methods=['POST','GET'])
def cand():
    error = None
    if request.method == 'POST':
        candidat = request.form["candidat"]
        numero = request.form["numero"]
        db = getdb()
        error = None
        user = db.execute(
            "SELECT nom FROM candidat WHERE code = ?", (numero,)
        ).fetchone()
        if user is None:
            return" numéro de candidat incorrect"
        elif user!=candidat:
                error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            return redirect(url_for('Candidat',name = candidat))

        return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''
    return render_template('cand.html', error=error)   
   
@app.route('/Candidat/<name>/edit')
def changinfo():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'

@app.route('/Ecole')
@app.route('/Ecole/<name>')
def ecole():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'

@app.route('/Prof')
@app.route('/Prof/<name>')
def prof():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'

@app.route('/Register')
def nouveau():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'


if __name__ == '__main__':
   app.run(debug = True)
   