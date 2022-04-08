from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

current_path = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(current_path, "templates")
statics = os.path.join(current_path, "static")

app = Flask(
    "ThesauRusse",
    template_folder=templates,
    static_folder=statics
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Base_Ecrivains.sqlite'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .routes import *
