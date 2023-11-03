from mua import db


class User(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
