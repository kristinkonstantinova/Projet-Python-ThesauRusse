from ..app import db

class Personne(db.Model):
    __tablename__ = "Personne"
    personne_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    personne_adresse_id = db.Column(db.Integer, nullable=False)
    personne_oeuvre_id = db.Column(db.Integer, nullable=False)
    personne_nom = db.Column(db.Text, nullable=False)
    personne_prenom = db.Column(db.Text, nullable=False)
    personne_date_naissance = db.Column(db.Integer, nullable=False)
    personne_date_mort= db.Column(db.Integer, nullable=False)


class Adresse(db.Model):
    __tablename__ = "Adresse"
    adresse_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    adresse_personne_id = db.Column(db.Integer, nullable=False)
    adresse_oeuvre_id = db.Column(db.Integer, nullable=False)
    adresse_date = db.Column(db.Integer, nullable=False)
    adresse_commune = db.Column(db.Text, nullable=False)
    adresse_arrondissement = db.Column(db.Text)
    adresse_rue = db.Column(db.Text, nullable=False)
    adresse_longitude = db.Column(db.Float, nullable=False)
    adresse_latitude = db.Column(db.Float, nullable=False)


class Oeuvre(db.Model):
    __tablename__ = "Oeuvre"
    oeuvre_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    oeuvre_personne_id = db.Column(db.Integer, nullable=False)
    oeuvre_date = db.Column(db.Text, nullable=False)
    oeuvre_titre_russe = db.Column(db.Text, nullable=False)
    oeuvre_titre_francais = db.Column(db.Text, nullable=False)
    oeuvre_adresse_id = db.Column(db.Integer, nullable=False)
