from flask import Blueprint, render_template, redirect, url_for
from mua.models import Character, Image, Rank, World
import mua.util.scrap
from mua import db
import datetime
import time

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/<nickname>")
def user(nickname):
    # https://maplestory.nexon.com/N23Ranking/World/Total?c=%EB%A6%B0%ED%8A%B8%EA%B2%94&w=0
    # https://maplestory.nexon.com/N23Ranking/World/Total?c=%EB%A6%B0%ED%8A%B8%EA%B2%94&w=3

    character = Character.query.filter_by(nickname=nickname).first()
    if not character:
        # 전체 월드 특정 캐릭터 스크랩
        url = "https://maplestory.nexon.com/N23Ranking/World/Total?c={nickname}&w=0".format(
            nickname=nickname
        )
        character_info_list = mua.util.scrap.getCharacterInfo(url)

        # 스크랩된 10명의 캐릭터 정보 업데이트
        for character_info in character_info_list:
            character_info: dict
            total_rank = character_info.get("rank")
            image = character_info.get("image")
            name = character_info.get("name")
            occupation = character_info.get("occupation")
            level = character_info.get("level")
            experience = character_info.get("expreience")
            popularity = character_info.get("popularity")
            guild = character_info.get("guild")

            # 10명의 캐릭터가 데이터베이스에 있는지 확인
            character = Character.query.filter_by(nickname=name).first()
            if not character:
                KST = datetime.timezone(datetime.timedelta(hours=9))
                current_time = datetime.datetime.now(KST)

                rank_model = Rank(
                    character_nickname=name,
                    update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                    total_rank=total_rank,
                    world_rank=None,
                )
                db.session.add(rank_model)

                image_model = Image(
                    character_nickname=name,
                    update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                    url=image,
                )
                db.session.add(image_model)

                rank_id = (
                    Rank.query.filter_by(character_nickname=name)
                    .order_by(Rank.update_date.desc())
                    .first()
                    .id
                )

                image_id = (
                    Image.query.filter_by(character_nickname=name)
                    .order_by(Image.update_date.desc())
                    .first()
                    .id
                )

                # 데이터베이스 일반월드 12개 가져와서
                # 정보 스크랩해서 값넣기
                all_world = World.query.all()
                character_world = ""
                for world in all_world:
                    time.sleep(3)
                    url = "https://maplestory.nexon.com/N23Ranking/World/Total?c={name}&w={value}".format(
                        name=name, value=world.value
                    )
                    # 스크랩
                    response = mua.util.scrap.getCharacterWorld(url)
                    if len(response) > 0:
                        character_world = world.name
                        break

                character_model = Character(
                    nickname=name,
                    world_name=character_world,
                    user_name=None,
                    rank_id=rank_id,
                    image_id=image_id,
                    level=level,
                    occupation=occupation,
                    experience=experience,
                    popularity=popularity,
                    guild=guild,
                )
                db.session.add(character_model)
                db.session.commit()

            time.sleep(10)

    # 결과 조회
    result = (
        db.session.query(Character, Rank, Image)
        .filter_by(nickname=nickname)
        .order_by(Character.level.desc(), Character.experience.desc())
        .join(Rank, Character.rank_id == Rank.id)
        .join(Image, Character.image_id == Image.id)
        .all()
    )
    return render_template(
        "main/user.html", character=result[0][0], rank=result[0][1], image=result[0][2]
    )
