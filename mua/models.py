from mua import db


class User(db.Model):
    user_name = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)

class World(db.Model):
    name=db.Column(db.String(32), primary_key=True)
    type=db.Column(db.String(32), nullable=False)
