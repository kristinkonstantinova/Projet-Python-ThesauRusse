import csv
import flask_migrate
import os
from ..app import app, db

personne_adresses_table = db.Table(
    'personne_adresse', db.Model.metadata,
    db.Column('personne_id', db.ForeignKey('Personne.personne_id'), primary_key=True),
    db.Column('adresse_id', db.ForeignKey('Adresse.adresse_id'), primary_key=True)
)

personne_oeuvre_table = db.Table(
    'personne_oeuvre', db.Model.metadata,
    db.Column('personne_id', db.ForeignKey('Personne.personne_id'), primary_key=True),
    db.Column('oeuvre_id', db.ForeignKey('Oeuvre.oeuvre_id'), primary_key=True)
)

oeuvre_adresses_table = db.Table(
    'oeuvre_adresse', db.Model.metadata,
    db.Column('oeuvre_id', db.ForeignKey('Oeuvre.oeuvre_id'), primary_key=True),
    db.Column('adresse_id', db.ForeignKey('Adresse.adresse_id'), primary_key=True)
)

class Personne(db.Model):
    __tablename__ = "Personne"
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_nom = db.Column(db.Text, nullable=False)
    personne_prenom = db.Column(db.Text, nullable=False)
    personne_date_naissance = db.Column(db.Integer, nullable=False)
    personne_date_mort= db.Column(db.Integer, nullable=False)
    adresses = db.relationship("Adresse", secondary=personne_adresses_table, backref=db.backref('personnes'))
    oeuvres = db.relationship("Oeuvre", secondary=personne_oeuvre_table, backref=db.backref('personnes'))

class Adresse(db.Model):
    __tablename__ = "Adresse"
    adresse_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    adresse_date = db.Column(db.Integer, nullable=True)
    adresse_commune = db.Column(db.Text, nullable=False)
    adresse_arrondissement = db.Column(db.Text)
    adresse_rue = db.Column(db.Text, nullable=False)
    adresse_longitude = db.Column(db.Float, nullable=True)
    adresse_latitude = db.Column(db.Float, nullable=True)
    oeuvres = db.relationship("Oeuvre", secondary=oeuvre_adresses_table, backref=db.backref('adresses'))

class Oeuvre(db.Model):
    __tablename__ = "Oeuvre"
    oeuvre_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    oeuvre_date = db.Column(db.Text, nullable=True)
    oeuvre_titre_russe = db.Column(db.Text, nullable=False)
    oeuvre_titre_francais = db.Column(db.Text, nullable=False)



def lire_lignes(fichier):
    with open(fichier, 'r') as f:
        # supprimer la premiere ligne qui contient les intitules de colonnes
        return [line for line in csv.reader(f, delimiter=',')][1:]


def db_valeur(v):
    if isinstance(v, int) or isinstance(v, float):
        return f"{v}"
    elif v is None:
        return "NULL"
    else:
        return f"'{v}'"


def convertir_int(valeur):
    try:
        return int(valeur)
    except ValueError:
        return None


def convertir_float(valeur):
    try:
        return float(valeur)
    except ValueError:
        return None


def convertir_adresse(adresse):
    """
    id
    personne_id
    oeuvre_id
    date
    commune
    arrondissement
    rue
    longitude
    latitude
    """
    return Adresse(
        adresse_id=convertir_int(adresse[0]),
        adresse_date=convertir_int(adresse[3]),
        adresse_commune=adresse[4],
        adresse_arrondissement=convertir_int(adresse[5]),
        adresse_rue=adresse[6],
        adresse_longitude=convertir_float(adresse[7]),
        adresse_latitude=convertir_float(adresse[8])
    )


def convertir_personne(personne):
    """
    id
    adresse_id
    oeuvre_id
    nom
    prenom
    date_naissance
    date_mort
    """
    return Personne(
        personne_id=convertir_int(personne[0]),
        personne_nom=personne[3],
        personne_prenom=personne[4],
        personne_date_naissance=convertir_int(personne[5]),
        personne_date_mort=convertir_int(personne[6])
    )


def convertir_oeuvre(oeuvre):
    """
    id
    personne_id
    date
    titre_russe
    titre_francais
    adresse_id
    """
    return Oeuvre(
        oeuvre_id=convertir_int(oeuvre[0]),
        oeuvre_date=convertir_int(oeuvre[2]),
        oeuvre_titre_russe=oeuvre[3],
        oeuvre_titre_francais=oeuvre[4]
    )


def ajout_lien_personne_oeuvre(db, personne_id, oeuvre_id):
    personne = Personne.query.get(personne_id)
    oeuvre = Oeuvre.query.get(oeuvre_id)
    personne.oeuvres.append(oeuvre)
    db.session.add(personne)


def ajout_lien_personne_adresse(db, personne_id, adresse_id):
    personne = Personne.query.get(personne_id)
    adresse = Adresse.query.get(adresse_id)
    personne.adresses.append(adresse)
    db.session.add(personne)


def ajout_lien_oeuvre_adresse(db, oeuvre_id, adresse_id):
    oeuvre = Oeuvre.query.get(oeuvre_id)
    adresse = Adresse.query.get(adresse_id)
    oeuvre.adresses.append(adresse)
    db.session.add(oeuvre)


def initialiser_base(app, db):
    with app.app_context():
        if os.path.exists("migrations"):
            print('La base de données existe déjà')
            return
        else:
            print('Initialisation de la base de données')

        flask_migrate.init()
        flask_migrate.migrate()
        flask_migrate.upgrade()

        adresses_csv = lire_lignes("Adresse.csv")
        adresses = [convertir_adresse(a) for a in adresses_csv]
        personnes_csv = lire_lignes("Personne.csv")
        personnes = [convertir_personne(a) for a in personnes_csv]
        oeuvres_csv = lire_lignes("Oeuvre.csv")
        oeuvres = [convertir_oeuvre(a) for a in oeuvres_csv]

        for objet in adresses + personnes + oeuvres:
            db.session.add(objet)

        for personne in personnes_csv:
            if personne[1]:
                ajout_lien_personne_adresse(db, personne[0], personne[1])
            if personne[2]:
                ajout_lien_personne_oeuvre(db, personne[0], personne[2])

        for oeuvre in oeuvres_csv:
            if oeuvre[5]:
                ajout_lien_oeuvre_adresse(db, oeuvre[0], oeuvre[5])

        db.session.commit()


initialiser_base(app, db)
