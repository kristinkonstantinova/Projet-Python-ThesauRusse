from ..app import db

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
    personne_adresse_id = db.Column(db.Integer, db.ForeignKey('Adresse.adresse_id'), nullable=False)
    personne_oeuvre_id = db.Column(db.Integer, db.ForeignKey('Oeuvre.oeuvre_id'), nullable=False)
    personne_nom = db.Column(db.Text, nullable=False)
    personne_prenom = db.Column(db.Text, nullable=False)
    personne_date_naissance = db.Column(db.Integer, nullable=False)
    personne_date_mort= db.Column(db.Integer, nullable=False)
    adresse = db.relationship("Adresse", secondary=personne_adresses_table)
    oeuvre = db.relationship("Oeuvre", secondary=personne_oeuvre_table)

class Adresse(db.Model):
    __tablename__ = "Adresse"
    adresse_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    adresse_personne_id = db.Column(db.Integer, db.ForeignKey('Personne.personne_id'), nullable=False)
    adresse_oeuvre_id = db.Column(db.Integer, db.ForeignKey('Oeuvre.oeuvre_id'), nullable=False)
    adresse_date = db.Column(db.Integer, nullable=False)
    adresse_commune = db.Column(db.Text, nullable=False)
    adresse_arrondissement = db.Column(db.Text)
    adresse_rue = db.Column(db.Text, nullable=False)
    adresse_longitude = db.Column(db.Float, nullable=False)
    adresse_latitude = db.Column(db.Float, nullable=False)
    personnes = db.relationship("Personne", secondary=personne_adresses_table)
    oeuvre = db.relationship("Oeuvre", secondary=oeuvre_adresses_table)

class Oeuvre(db.Model):
    __tablename__ = "Oeuvre"
    oeuvre_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    oeuvre_personne_id = db.Column(db.Integer, db.ForeignKey('Personne.personne_id'), nullable=False)
    oeuvre_date = db.Column(db.Text, nullable=False)
    oeuvre_titre_russe = db.Column(db.Text, nullable=False)
    oeuvre_titre_francais = db.Column(db.Text, nullable=False)
    oeuvre_adresse_id = db.Column(db.Integer, db.ForeignKey('Adresse.adresse_id'), nullable=False)
    personne = db.relationship("Personne", secondary=personne_oeuvre_table)
    adresse = db.relationship("Adresse", secondary=oeuvre_adresses_table)

