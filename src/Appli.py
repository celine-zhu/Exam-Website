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
@app.route('/Candidat',methods=['POST', 'GET'])
def cand():
    if request.method == 'POST':
        candidat = request.form.get('Nom du candidat')
        num = request.form.get('Numéro de Dossier')
        b=str("select nom from candidat where code=" + str(num)  )
        c = getdb().cursor()
        c.execute(b)
        content = []
        for i in c.fetchall():
            content.append(i)
        if candidat==content[0]:
            return redirect(url_for('Candidat',name = candidat))
        else:
            return '''<div> Error, please check that your name and candidate serial are correct<div>
             <div> <a href="http://127.0.0.1:5000"> retour<div>'''

    return '''
              <form method="POST">
                  <div><label>Nom du candidat: <input type="text" name="Nom"></label></div>
                  <div><label>Numéro de Dossier: <input type="text" name="Num"></label></div>
                  <input type="submit" value="Submit">
              </form>
              <div> <a href="http://127.0.0.1:5000"> retour<div>'''
   
@app.route('/Candidat/<name>/edit')
def changinfo():
    return '<div> <a href="http://127.0.0.1:5000"> retour<div>'
@app.route('/Ecole')
@app.route('/Ecole/<name>')
def get_ecol(name=None):
    return render_template('template/ecole.html', name=name)
@app.route('/Prof')
@app.route('/Prof/<name>')
def getelev():
    return 'mamamia'
@app.route('/Register')
def nouveau():
    return 
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)
   