from flask_sqlalchemy import SQLAlchemy

db = None


def init_db(app):
    db = SQLAlchemy(app)


class ImageDB(db.Model):
    __tablename__ = 'imagedb'

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(255), nullable=False)
    posx = db.Column(db.Integer)
    posy = db.Column(db.Integer)
