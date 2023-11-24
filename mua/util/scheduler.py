from mua.models import World, Character, Image, Rank, World
import mua.util.scrap
from mua import db
import datetime
import time


def updateWorld(app):
    """
    월드 이름과 종류를 업데이트
    """
    url = "https://maplestory.nexon.com/N23Ranking/World/Total"
    with app.app_context():
        response = mua.util.scrap.getWorldInfo(url)
        normal_world: dict = response.get("일반 월드")
        for world, value in normal_world.items():
            if not World.query.filter_by(name=world):
                world_model = World(name=world, type="normal", value=value)
                db.session.add(world_model)

        reboot_world: dict = response.get("리부트 월드")
        for world, value in reboot_world.items():
            if not World.query.filter_by(name=world):
                world_model = World(name=world, type="reboot", value=value)
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
            all_character_info = mua.util.scrap.getCharacterInfo(TOTAL_WORLD_URL)

            for character_info in all_character_info:
                character_info: dict
                rank = character_info.get("rank")
                image = character_info.get("image")
                name = character_info.get("name")
                occupation = character_info.get("occupation")
                level = character_info.get("level")
                experience = character_info.get("expreience")
                popularity = character_info.get("popularity")
                guild = character_info.get("guild")

                KST = datetime.timezone(datetime.timedelta(hours=9))
                current_time = datetime.datetime.now(KST)

                rank_model = Rank(
                    character_nickname=name,
                    update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                    total_rank=rank,
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

                # 특정 캐릭터 있으면 rank_id, image_id, level, experince, popularity, guild업데이트
                character = Character.query.filter_by(nickname=name).first()
                if character:
                    character.rank_id = rank_id
                    character.image_id = image_id
                    character.level = level
                    character.experience = experience
                    character.popularity = popularity
                    character.guild = guild

                    db.session.commit()
                else:
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

        db.session.close()


def updateWorldRank(app):
    """
    특정 월드 TOP100 랭킹 업데이트
    """
    with app.app_context():
        # 월드 정보 가져오기
        all_world = World.query.all()
        # 월드 하나당 TOP100 업데이트
        for world in all_world:
            for i in range(1, 11):
                url = "https://maplestory.nexon.com/N23Ranking/World/Total?page={page}&w={value}".format(
                    page=i, value=world.value
                )
                # 주어진 url로 10명 캐릭터 스크랩
                all_character_info = mua.util.scrap.getCharacterInfo(url)

                # 정보 추출
                for character_info in all_character_info:
                    character_info: dict
                    rank = character_info.get("rank")
                    image = character_info.get("image")
                    name = character_info.get("name")
                    occupation = character_info.get("occupation")
                    level = character_info.get("level")
                    experience = character_info.get("expreience")
                    popularity = character_info.get("popularity")
                    guild = character_info.get("guild")

                    KST = datetime.timezone(datetime.timedelta(hours=9))
                    current_time = datetime.datetime.now(KST)

                    rank_model = Rank(
                        character_nickname=name,
                        update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                        total_rank=None,
                        world_rank=rank,
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

                    # 캐릭터가 데이터베이스에 존재하는지 확인
                    character = Character.query.filter_by(nickname=name).first()

                    # 있으면 업데이트
                    if character:
                        character.rank_id = rank_id
                        character.image_id = image_id
                        character.world_name = world.name
                        character.level = level
                        character.experience = experience
                        character.popularity = popularity
                        character.guild = guild

                        db.session.commit()
                    # 없으면 새로 등록
                    else:
                        character_model = Character(
                            nickname=name,
                            world_name=world.name,
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
        db.session.close()