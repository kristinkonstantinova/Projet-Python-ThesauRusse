import csv
import flask_migrate
import os
from ..app import app, db

ecrivain_adresses_table = db.Table(
    'ecrivain_adresse', db.Model.metadata,
    db.Column('ecrivain_id', db.ForeignKey('Ecrivain.ecrivain_id'), primary_key=True),
    db.Column('adresse_id', db.ForeignKey('Adresse.adresse_id'), primary_key=True)
)

ecrivain_oeuvre_table = db.Table(
    'ecrivain_oeuvre', db.Model.metadata,
    db.Column('ecrivain_id', db.ForeignKey('Ecrivain.ecrivain_id'), primary_key=True),
    db.Column('oeuvre_id', db.ForeignKey('Oeuvre.oeuvre_id'), primary_key=True)
)

oeuvre_adresses_table = db.Table(
    'oeuvre_adresse', db.Model.metadata,
    db.Column('oeuvre_id', db.ForeignKey('Oeuvre.oeuvre_id'), primary_key=True),
    db.Column('adresse_id', db.ForeignKey('Adresse.adresse_id'), primary_key=True)
)

class Ecrivain(db.Model):
    __tablename__ = "Ecrivain"
    ecrivain_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    ecrivain_nom = db.Column(db.Text, nullable=False)
    ecrivain_prenom = db.Column(db.Text, nullable=False)
    ecrivain_date_naissance = db.Column(db.Integer, nullable=False)
    ecrivain_date_mort= db.Column(db.Integer, nullable=False)
    adresses = db.relationship("Adresse", secondary=ecrivain_adresses_table, backref=db.backref('ecrivains'))
    oeuvres = db.relationship("Oeuvre", secondary=ecrivain_oeuvre_table, backref=db.backref('ecrivains'))

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
    ecrivain_id
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


def convertir_ecrivain(ecrivain):
    """
    id
    adresse_id
    oeuvre_id
    nom
    prenom
    date_naissance
    date_mort
    """
    return Ecrivain(
        ecrivain_id=convertir_int(ecrivain[0]),
        ecrivain_nom=ecrivain[3],
        ecrivain_prenom=ecrivain[4],
        ecrivain_date_naissance=convertir_int(ecrivain[5]),
        ecrivain_date_mort=convertir_int(ecrivain[6])
    )


def convertir_oeuvre(oeuvre):
    """
    id
    ecrivain_id
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


def ajout_lien_ecrivain_oeuvre(db, ecrivain_id, oeuvre_id):
    ecrivain = Ecrivain.query.get(ecrivain_id)
    oeuvre = Oeuvre.query.get(oeuvre_id)
    ecrivain.oeuvres.append(oeuvre)
    db.session.add(ecrivain)


def ajout_lien_ecrivain_adresse(db, ecrivain_id, adresse_id):
    ecrivain = Ecrivain.query.get(ecrivain_id)
    adresse = Adresse.query.get(adresse_id)
    ecrivain.adresses.append(adresse)
    db.session.add(ecrivain)


def ajout_lien_adresse_oeuvre(db, adresse_id, oeuvre_id):
    adresse = Adresse.query.get(adresse_id)
    oeuvre = Oeuvre.query.get(oeuvre_id)
    adresse.oeuvres.append(oeuvre)
    db.session.add(adresse)


def ajout_lien_adresse_ecrivain(db, adresse_id, ecrivain_id):
    adresse = Adresse.query.get(adresse_id)
    ecrivain = Ecrivain.query.get(ecrivain_id)
    adresse.ecrivains.append(ecrivain)
    db.session.add(adresse)


def ajout_lien_oeuvre_adresse(db, oeuvre_id, adresse_id):
    oeuvre = Oeuvre.query.get(oeuvre_id)
    adresse = Adresse.query.get(adresse_id)
    oeuvre.adresses.append(adresse)
    db.session.add(oeuvre)


def ajout_lien_oeuvre_ecrivain(db, oeuvre_id, ecrivain_id):
    oeuvre = Oeuvre.query.get(oeuvre_id)
    ecrivain = Ecrivain.query.get(ecrivain_id)
    oeuvre.ecrivains.append(ecrivain)
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
        ecrivains_csv = lire_lignes("Ecrivain.csv")
        ecrivains = [convertir_ecrivain(a) for a in ecrivains_csv]
        oeuvres_csv = lire_lignes("Oeuvre.csv")
        oeuvres = [convertir_oeuvre(a) for a in oeuvres_csv]

        for objet in adresses + ecrivains + oeuvres:
            db.session.add(objet)

        for ecrivain in ecrivains_csv:
            if ecrivain[1]:
                ajout_lien_ecrivain_adresse(db, ecrivain[0], ecrivain[1])
            if ecrivain[2]:
                ajout_lien_ecrivain_oeuvre(db, ecrivain[0], ecrivain[2])

        for oeuvre in oeuvres_csv:
            if oeuvre[5]:
                ajout_lien_oeuvre_adresse(db, oeuvre[0], oeuvre[5])
            if oeuvre[1]:
                ajout_lien_oeuvre_ecrivain(db, oeuvre[0], oeuvre[1])

        for adresse in adresses_csv:
            if adresse[1]:
                ajout_lien_adresse_ecrivain(db, adresse[0], adresse[1])
            if adresse[2]:
                ajout_lien_adresse_oeuvre(db, adresse[0], adresse[2])

        db.session.commit()


initialiser_base(app, db)
