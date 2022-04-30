from flask import render_template
from .modeles.donnees import Personne, Adresse, Oeuvre
from .app import app, db
from flask import render_template, Flask, request
from .modeles.donnees import Personne, Adresse, Oeuvre
from .app import app, db
from sqlalchemy import or_


@app.route("/")
def accueil(exemple=None):
    ""
    personnes = Personne.query.order_by(Personne.personne_id.desc()).all()
    return render_template("pages/Accueil.html", nom="ThesauRusse", personnes=personnes)

@app.route("/personnes/<int:personne_id>")
def personne(personne_id):
    resultats_personne = Personne.query.get(personne_id)
    return render_template("pages/Personnes.html", personnes=resultats_personne)

@app.route("/oeuvres/<int:oeuvre_id>")
def oeuvre(oeuvre_id):
    resultats_oeuvre = Oeuvre.query.get(oeuvre_id)
    return render_template("pages/Oeuvres.html", oeuvres=resultats_oeuvre)

@app.route("/adresses/<int:adresse_id>")
def adresse(adresse_id):
    resultats_adresse = Adresse.query.get(adresse_id)
    return render_template("pages/Adresses.html", adresses=resultats_adresse)

@app.route("/recherche")
def recherche():
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats_personne = []
    resultats_oeuvre = []
    resultats_adresse = []
    # On fait de même pour le titre de la page
    titre = "PagedeRecherche"
    if motclef:
        resultats_personne = Personne.query.filter(
            or_(
            Personne.personne_nom.like("%{}%".format(motclef)),
            Personne.personne_prenom.like("%{}%".format(motclef)),
            Personne.personne_date_naissance.like("%{}%".format(motclef)),
            Personne.personne_date_mort.like("%{}%".format(motclef)),
            )
        ).all()
        resultats_oeuvre = Oeuvre.query.filter(
            or_(
                Oeuvre.oeuvre_date.like("%{}%".format(motclef)),
                Oeuvre.oeuvre_titre_russe.like("%{}%".format(motclef)),
                Oeuvre.oeuvre_titre_francais.like("%{}%".format(motclef)),
            )
        ).all()
        resultats_adresse = Adresse.query.filter(
            or_(
                Adresse.adresse_rue.like("%{}%".format(motclef)),
                Adresse.adresse_commune.like("%{}%".format(motclef)),
                Adresse.adresse_arrondissement.like("%{}%".format(motclef)),
                Adresse.adresse_date.like("%{}%".format(motclef)),
            )
        ).all()

        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/PagedeRecherche.html", resultats_personne=resultats_personne,
                           resultats_oeuvre=resultats_oeuvre,
                           resultats_adresse=resultats_adresse, titre=titre)
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