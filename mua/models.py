from mua import db


class User(db.Model):
    user_name = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)


class World(db.Model):
    name = db.Column(db.String(32), primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    value = db.Column(db.String(4), unique=True)


class Character(db.Model):
    nickname = db.Column(db.String(64), primary_key=True)
    world_name = db.Column(
        db.String(32),
        db.ForeignKey("world.name"),
    )
    user_name = db.Column(
        db.String(32), db.ForeignKey("user.user_name")
    )
    rank_id = db.Column(db.Integer, db.ForeignKey("rank.id"))
    image_id = db.Column(db.Integer, db.ForeignKey("image.id"))
    level = db.Column(db.String(4))
    occupation = db.Column(db.String(64), nullable=False)
    experience = db.Column(db.String(256))
    popularity = db.Column(db.Integer)
    guild = db.Column(db.String(64))


class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_nickname = db.Column(
        db.String(64), db.ForeignKey("character.nickname")
    )
    update_date = db.Column(db.String(32))
    total_rank = db.Column(db.String(64))
    world_rank = db.Column(db.String(64))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_nickname = db.Column(db.String(64), db.ForeignKey("character.nickname"))
    update_date = db.Column(db.String(32))
    url = db.Column(db.String(256))
