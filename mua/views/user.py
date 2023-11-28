from flask import Blueprint, render_template
from mua.models import Character, Image, Rank, World
from mua.util.scrap import getCharacterInfo
from mua import db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/<nickname>")
def user(nickname):
    result = (
        db.session.query(Character, Rank, Image)
        .filter_by(nickname=nickname)
        .order_by(Character.level.desc(), Character.experience.desc())
        .join(Rank, Character.rank_id == Rank.id)
        .join(Image, Character.image_id == Image.id)
        .all()
    )
    return render_template("main/user.html", character=result[0][0], rank=result[0][1], image=result[0][2])
