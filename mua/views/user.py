from flask import Blueprint, render_template, redirect, url_for
from mua.models import Character, Image, Rank, World
import mua.util.scrap
from mua import db
import datetime
import time

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/<nickname>")
def user(nickname):
    character = Character.query.filter_by(nickname=nickname).first()
    if not character:
        # 전체 월드 특정 캐릭터 스크랩
        # 0 : 일반 월드
        # 254 : 리부트 월드

        # 일반 월드에 캐릭터 있는지 확인
        # 없으면 리부트 월드 캐릭터 조회

        url = "https://maplestory.nexon.com/N23Ranking/World/Total?c={nickname}&w={value}".format(nickname=nickname, value=0)
        response = mua.util.scrap.getCharacterWorld(url)

        if not len(response) > 0:
            url = "https://maplestory.nexon.com/N23Ranking/World/Total?c={nickname}&w={value}".format(nickname=nickname, value=254)
        print(url)
        total_character_info = mua.util.scrap.getCharacterInfo(url)

        # 스크랩된 10명의 캐릭터 정보 조회
        for character_info in total_character_info:
            character_info: dict
            total_rank = character_info.get("rank")
            total_image = character_info.get("image")
            total_name = character_info.get("name")
            total_occupation = character_info.get("occupation")
            total_level = character_info.get("level")
            total_experience = character_info.get("expreience")
            total_popularity = character_info.get("popularity")
            total_guild = character_info.get("guild")

            # 검색된 캐릭터가 아니면 다음 캐릭터로
            if not total_name == nickname:
                continue

            # 캐릭터가 데이터베이스에 있는지 확인
            character = Character.query.filter_by(nickname=total_name).first()
            # 없으면 데이터베이스에 값 넣기
            if not character:
                KST = datetime.timezone(datetime.timedelta(hours=9))
                current_time = datetime.datetime.now(KST)

                # 월드 페이지 전체 조회 하면서 캐릭터 월드 확인
                all_world = World.query.all()
                for world in all_world:
                    time.sleep(3)
                    url = "https://maplestory.nexon.com/N23Ranking/World/Total?c={name}&w={value}".format(
                        name=total_name, value=world.value
                    )
                    # 스크랩
                    response: dict = mua.util.scrap.getCharacterWorld(url)
                    if len(response) > 0:
                        # 찾은 월드 정보로 캐릭터 조회
                        world_character_info: dict = mua.util.scrap.getCharacterInfo(
                            url
                        )
                        for character_info in world_character_info:
                            character_info: dict
                            world_name = character_info.get("name")

                            # 조회한 캐릭터 정보가 나올때까지 건너뛰기
                            if not nickname == world_name:
                                continue

                            # 월드 랭킹 조회
                            world_rank = character_info.get("rank")

                            # 랭크 모델 생성
                            rank_model = Rank(
                                character_nickname=total_name,
                                update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                                total_rank=total_rank,
                                world_rank=world_rank,
                            )
                            db.session.add(rank_model)

                            image_model = Image(
                                character_nickname=total_name,
                                update_date=current_time.strftime("%Y-%m-%d, %H:%M:%S"),
                                url=total_image,
                            )
                            db.session.add(image_model)

                            rank_id = (
                                Rank.query.filter_by(character_nickname=total_name)
                                .order_by(Rank.update_date.desc())
                                .first()
                                .id
                            )

                            image_id = (
                                Image.query.filter_by(character_nickname=total_name)
                                .order_by(Image.update_date.desc())
                                .first()
                                .id
                            )

                            character_model = Character(
                                nickname=total_name,
                                world_name=world.name,
                                user_name=None,
                                rank_id=rank_id,
                                image_id=image_id,
                                level=total_level,
                                occupation=total_occupation,
                                experience=total_experience,
                                popularity=total_popularity,
                                guild=total_guild,
                            )

                        break

                db.session.add(character_model)
                db.session.commit()

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
