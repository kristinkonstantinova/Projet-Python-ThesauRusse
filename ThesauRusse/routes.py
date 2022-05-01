from flask import render_template, redirect, url_for
from .modeles.donnees import Ecrivain, Adresse, Oeuvre
from .app import app, db
from flask import render_template, Flask, request
from .modeles.donnees import Ecrivain, Adresse, Oeuvre
from .app import app, db
from sqlalchemy import or_


@app.route("/")
def accueil(exemple=None):
    ""
    adresses = Adresse.query.order_by(Adresse.adresse_id.desc()).all()
    ecrivains = Ecrivain.query.order_by(Ecrivain.ecrivain_id.desc()).all()
    oeuvres = Oeuvre.query.order_by(Oeuvre.oeuvre_id.desc()).all()
    return render_template(
        "pages/Accueil.html",
        adresses=adresses,
        ecrivains=ecrivains,
        oeuvres=oeuvres
    )

@app.route("/ecrivains")
def ecrivains():
    resultats_ecrivain = Ecrivain.query.all()
    return render_template("pages/Ecrivains.html", ecrivains=resultats_ecrivain)

@app.route("/ecrivain/<int:ecrivain_id>")
def ecrivain(ecrivain_id):
    resultats_ecrivain = Ecrivain.query.get(ecrivain_id)
    return render_template("pages/Ecrivain.html", ecrivain=resultats_ecrivain)

@app.route("/oeuvres")
def oeuvres():
    resultats_oeuvre = Oeuvre.query.all()
    return render_template("pages/Oeuvres.html", oeuvres=resultats_oeuvre)

@app.route("/oeuvre/<int:oeuvre_id>")
def oeuvre(oeuvre_id):
    resultats_oeuvre = Oeuvre.query.get(oeuvre_id)
    return render_template("pages/Oeuvre.html", oeuvre=resultats_oeuvre)

@app.route("/adresses")
def adresses():
    resultats_adresse = Adresse.query.all()
    return render_template("pages/Adresses.html", adresses=resultats_adresse)

@app.route("/adresse/<int:adresse_id>")
def adresse(adresse_id):
    resultats_adresse = Adresse.query.get(adresse_id)
    return render_template("pages/Adresse.html", adresse=resultats_adresse)

@app.route("/ajout/ecrivain")
def ajout_ecrivain():
    return render_template("pages/ajout/ecrivain.html")

@app.route("/envoi/ecrivain", methods=['POST'])
def envoi_ecrivain():
    e = Ecrivain(
        ecrivain_prenom=request.form['Prenom'],
        ecrivain_nom=request.form['Nom'],
        ecrivain_date_naissance=int(request.form['Naissance']),
        ecrivain_date_mort=int(request.form['Mort'])
    )
    db.session.add(e)
    db.session.commit()

    return redirect(url_for('ecrivain', ecrivain_id=e.ecrivain_id))

@app.route("/supprimer/ecrivain/<int:ecrivain_id>", methods=['POST'])
def supprimer_ecrivain(ecrivain_id):
    db.session.delete(Ecrivain.query.get(ecrivain_id))
    db.session.commit()

    return redirect(url_for('ecrivains'))

@app.route("/ajout/oeuvre")
def ajout_oeuvre():
    return render_template("pages/ajout/oeuvre.html")

@app.route("/ajout/adresse")
def ajout_adresse():
    return render_template("pages/ajout/adresse.html")

@app.route("/recherche")
def recherche():
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    motclef = request.args.get("keyword", None)
    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats_ecrivain = []
    resultats_oeuvre = []
    resultats_adresse = []
    # On fait de même pour le titre de la page
    titre = "PagedeRecherche"
    if motclef:
        resultats_ecrivain = Ecrivain.query.filter(
            or_(
            Ecrivain.ecrivain_nom.like("%{}%".format(motclef)),
            Ecrivain.ecrivain_prenom.like("%{}%".format(motclef)),
            Ecrivain.ecrivain_date_naissance.like("%{}%".format(motclef)),
            Ecrivain.ecrivain_date_mort.like("%{}%".format(motclef)),
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
    return render_template("pages/PagedeRecherche.html", resultats_ecrivain=resultats_ecrivain,
                           resultats_oeuvre=resultats_oeuvre,
                           resultats_adresse=resultats_adresse, titre=titre)
"""
ecrivain = Ecrivain.query
print(ecrivain)

for pers in ecrivain:
    print(pers.ecrivain_nom, pers.ecrivain_prenom)

ecrivains = Ecrivain.query.filter(Ecrivain.ecrivain_prenom == "Marina").all()
print(ecrivains)


for pers in ecrivains:
    print(pers.ecrivain_nom, pers.ecrivain_prenom)

adresses = Adresse.query.filter(Adresse.adresse_id == "5").count()
print(adresses) """