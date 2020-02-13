import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

application = Flask(__name__)

application.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), Config.UPLOAD_FOLDER)
application.config['DB_FOLDER'] = os.path.abspath(os.path.dirname(__file__))
application.config['DB_FILE'] = os.path.join(application.config['DB_FOLDER'], Config.DB_FILE)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(Config.DB_FILE)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)


class ImageDB(db.Model):
    __tablename__ = 'imagedb'

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(255), nullable=False)
    posx = db.Column(db.Integer)
    posy = db.Column(db.Integer)
