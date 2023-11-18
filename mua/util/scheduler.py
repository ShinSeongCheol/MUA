from mua.util.scrap import getCharacterInfo, getWorldInfo
from mua.models import World, Character, Image, Rank
from mua import db
import datetime
import time


def updateWorld(app):
    """
    월드 이름과 종류를 업데이트
    """
    url = "https://maplestory.nexon.com/N23Ranking/World/Total"
    with app.app_context():
        response = getWorldInfo(url)
        normal_world: dict = response.get("일반 월드")
        for world in normal_world:
            world_name = World.query.get(world)
            if not world_name:
                world_model = World(name=world, type="normal")
                db.session.add(world_model)

        reboot_world: dict = response.get("리부트 월드")
        for world in reboot_world:
            world_name = World.query.get(world)
            if not world_name:
                world_model = World(name=world, type="reboot")
                db.session.add(world_model)
        db.session.commit()
        db.session.close()


def updateWorldTotalRank(app):
    """
    일반월드 전체 랭킹 업데이트
    """
    with app.app_context():
        for i in range(1, 11):
            TOTAL_WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?page={page}".format(
                page=i
            )
            all_character_info = getCharacterInfo(TOTAL_WORLD_URL)

            for character_info in all_character_info:
                character_info: dict
                rank = character_info.get("rank")
                image = character_info.get("image")
                name = character_info.get("name")
                occupation = character_info.get("occupation")
                level = character_info.get("level")
                expreience = character_info.get("expreience")
                popularity = character_info.get("popularity")
                guild = character_info.get("guild")

                KST = datetime.timezone(datetime.timedelta(hours=9))
                current_time = datetime.datetime.now(KST)

                rank_model = Rank(
                    character_nickname=name,
                    update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                    total_rank=rank,
                    world_rank=None
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
                    .first().id
                )

                image_id = (
                    Image.query.filter_by(character_nickname=name)
                    .order_by(Image.update_date.desc())
                    .first().id
                )

                character_model = Character(
                    nickname=name,
                    world_name=None,
                    user_name=None,
                    rank_id=rank_id,
                    image_id=image_id,
                    level = level,
                    occupation=occupation,
                    experience=expreience,
                    popularity=popularity,
                    guild=guild,
                )
                db.session.add(character_model)

            time.sleep(5)

            db.session.commit()
            db.session.close()
