from mua import db


class User(db.Model):
    user_name = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)


class World(db.Model):
    name = db.Column(db.String(32), primary_key=True)
    type = db.Column(db.String(32), nullable=False)

class Character(db.Model):
    nickname = db.Column(db.String(64), primary_key=True)
    world_name = db.Column(db.String(32), db.ForeignKey("world_name"), ondelete="CASCADE", onupdate="CASCADE")
    user_id = db.Column(db.String(32), db.ForeignKey("user_id"), ondelete="CASCADE")
    occupation = db.Column(db.String(64), nullable=False)
    experience = db.Column(db.String(256))
    popularity = db.Column(db.Integer)
    guild = db.Column(db.String(64))