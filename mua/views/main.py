from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
from sqlalchemy import cast, INTEGER
from mua.util.scheduler import updateWorldTotalRank

from mua.models import *

bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def main():
    # 가져올 월드들의 리스트
    top_characters = {}
    worlds = World.query.order_by(cast(World.value, INTEGER)).all()

    # 각 월드별로 상위 5개 캐릭터 가져오기
    for world in worlds:
        top_characters[world.name] = (
            db.session.query(Character, Image)
            .filter_by(world_name=world.name)
            .order_by(Character.level.desc(), Character.experience.desc())
            .join(Image, Character.image_id == Image.id)
            .group_by(Character.nickname)
            .order_by(Image.update_date.desc())
            .limit(5)
            .all()
        )

    return render_template("main/main.html", top_characters=top_characters)
