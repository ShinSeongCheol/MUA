from mua.models import World, Character, Image, Rank, World
from flask import Flask
import mua.util.scrap
from mua import db, scheduler
import datetime
import time

@scheduler.task("cron", id="updateWorld", day="*", hour=9)
def updateWorld():
    """
    월드 이름과 종류를 업데이트
    """
    app:Flask = scheduler.app
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


def updateWorldTotalRank():
    """
    월드 전체 랭킹 업데이트
    """
    with app.app_context():
        for i in range(1, 11):
            TOTAL_WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?page={page}".format(
                page=i
            )
            all_character_info = mua.util.scrap.getCharacterInfo(TOTAL_WORLD_URL)

            # 캐릭터 10개 정보
            for character_info in all_character_info:
                character_info: dict
                total_world_nickname = character_info.get("name")
                total_world_rank = character_info.get("rank")
                total_world_image = character_info.get("image")
                total_world_occupation = character_info.get("occupation")
                total_world_level = character_info.get("level")
                total_world_experience = character_info.get("experience")
                total_world_popularity = character_info.get("popularity")
                total_world_guild = character_info.get("guild")

                # 캐릭터 월드 정보 확인
                all_world = World.query.all()
                for world in all_world:
                    time.sleep(3)
                    url = "https://maplestory.nexon.com/N23Ranking/World/Total?c={name}&w={value}".format(
                        name=total_world_nickname, value=world.value
                    )
                    # 스크랩
                    # 캐릭터가 속해있는 월드의 10명 캐릭터 정보
                    all_world_character_info = mua.util.scrap.getCharacterWorld(url)
                    if len(all_world_character_info) > 0:
                        for world_character_info in all_world_character_info:
                            world_character_info: dict
                            world_nickname = world_character_info.get("name")
                            world_rank = world_character_info.get("rank")

                            # 캐릭터의 이름이 일치하지 않으면 종료
                            if not total_world_nickname == world_nickname:
                                break

                            KST = datetime.timezone(datetime.timedelta(hours=9))
                            current_time = datetime.datetime.now(KST)

                            rank_model = Rank(
                                character_nickname=total_world_nickname,
                                update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                                total_rank=total_world_rank,
                                world_rank=world_rank,
                            )
                            db.session.add(rank_model)

                            image_model = Image(
                                character_nickname=total_world_nickname,
                                update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                                url=total_world_image,
                            )
                            db.session.add(image_model)

                            rank_id = (
                                Rank.query.filter_by(
                                    character_nickname=total_world_nickname
                                )
                                .order_by(Rank.update_date.desc())
                                .first()
                                .id
                            )

                            image_id = (
                                Image.query.filter_by(
                                    character_nickname=total_world_nickname
                                )
                                .order_by(Image.update_date.desc())
                                .first()
                                .id
                            )

                            # 특정 캐릭터 있으면 rank_id, image_id, level, experince, popularity, guild업데이트
                            character = Character.query.filter_by(
                                nickname=total_world_nickname
                            ).first()
                            if character:
                                character.rank_id = rank_id
                                character.image_id = image_id
                                character.level = total_world_level
                                character.experience = total_world_experience
                                character.popularity = total_world_popularity
                                character.guild = total_world_guild

                                db.session.commit()

                            else:
                                character_model = Character(
                                    nickname=total_world_nickname,
                                    world_name=world.name,
                                    user_name=None,
                                    rank_id=rank_id,
                                    image_id=image_id,
                                    level=total_world_level,
                                    occupation=total_world_occupation,
                                    experience=total_world_experience,
                                    popularity=total_world_popularity,
                                    guild=total_world_guild,
                                )
                                db.session.add(character_model)
                                db.session.commit()

            time.sleep(10)

        db.session.close()

@scheduler.task("cron", id="updateWorldRank", hour=9)
def updateWorldRank():
    """
    특정 월드 TOP100 랭킹 업데이트
    """
    app:Flask = scheduler.app
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
                    world_rank = character_info.get("rank")
                    world_image = character_info.get("image")
                    world_nickname = character_info.get("name")
                    world_occupation = character_info.get("occupation")
                    world_level = character_info.get("level")
                    world_experience = character_info.get("experience")
                    world_popularity = character_info.get("popularity")
                    world_guild = character_info.get("guild")

                    # 일반월드 전체 월드에서 종합랭킹 가져오기
                    TOTAL_NORMAL_WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?c={nickname}&w=0".format(
                        nickname=world_nickname
                    )

                    # 리부트 월드 종합랭킹
                    TOTAL_REBOOT_WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?c={nickname}&w=254".format(
                        nickname=world_nickname
                    )

                    time.sleep(3)

                    if world.value == "1" or world.value == "2":
                        total_world_character_info = mua.util.scrap.getCharacterInfo(
                            TOTAL_REBOOT_WORLD_URL
                        )
                    else:
                        total_world_character_info = mua.util.scrap.getCharacterInfo(
                            TOTAL_NORMAL_WORLD_URL
                        )

                    # 특정 캐릭터 있는지 확인
                    if not len(total_world_character_info) > 0:
                        continue

                    for total_world_character in total_world_character_info:
                        total_world_character: dict
                        total_world_nickname = total_world_character.get("name")

                        # 이름이 같은지 확인
                        if not total_world_nickname == world_nickname:
                            continue
                        else:
                            print(total_world_nickname, world_nickname)

                        total_world_rank = total_world_character.get("rank")
                        # 데이터 추가

                        KST = datetime.timezone(datetime.timedelta(hours=9))
                        current_time = datetime.datetime.now(KST)

                        rank_model = Rank(
                            character_nickname=world_nickname,
                            update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                            total_rank=total_world_rank,
                            world_rank=world_rank,
                        )
                        db.session.add(rank_model)

                        image_model = Image(
                            character_nickname=world_nickname,
                            update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                            url=world_image,
                        )
                        db.session.add(image_model)

                        rank_id = (
                            Rank.query.filter_by(character_nickname=world_nickname)
                            .order_by(Rank.update_date.desc())
                            .first()
                            .id
                        )

                        image_id = (
                            Image.query.filter_by(character_nickname=world_nickname)
                            .order_by(Image.update_date.desc())
                            .first()
                            .id
                        )

                        # 캐릭터가 데이터베이스에 존재하는지 확인
                        character = Character.query.filter_by(
                            nickname=world_nickname
                        ).first()

                        # 있으면 업데이트
                        if character:
                            character.rank_id = rank_id
                            character.image_id = image_id
                            character.world_name = world.name
                            character.level = world_level
                            character.experience = world_experience
                            character.popularity = world_popularity
                            character.guild = world_guild

                            db.session.commit()
                        # 없으면 새로 등록
                        else:
                            character_model = Character(
                                nickname=world_nickname,
                                world_name=world.name,
                                user_name=None,
                                rank_id=rank_id,
                                image_id=image_id,
                                level=world_level,
                                occupation=world_occupation,
                                experience=world_experience,
                                popularity=world_popularity,
                                guild=world_guild,
                            )
                            db.session.add(character_model)
                            db.session.commit()

                time.sleep(6)
        db.session.close()
