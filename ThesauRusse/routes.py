from flask import render_template
from .modeles.donnees import Personne, Adresse, Oeuvre
from .app import app, db

@app.route("/")
def accueil(exemple=None):
    ""
    personnes = Personne.query.order_by(Personne.personne_id.desc()).limit(5).all()
    return render_template("pages/Accueil.html", nom="ThesauRusse", personnes=personnes)

@app.route("/personnes/<int:personne_id>")
def personne(personne_id):
    pass

"""
personne = Personne.query
print(personne)

for pers in personne:
    print(pers.personne_nom, pers.personne_prenom)

personnes = Personne.query.filter(Personne.personne_prenom == "Marina").all()
print(personnes)


for pers in personnes:
    print(pers.personne_nom, pers.personne_prenom)

adresses = Adresse.query.filter(Adresse.adresse_id == "5").count()
print(adresses) """