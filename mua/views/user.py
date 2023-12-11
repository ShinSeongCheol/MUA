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
        # 리부트 월드 캐릭터 있는지 확인
        # 없다면 캐릭터 없음 페이지로 이동
        url = (
            "https://maplestory.nexon.com/N23Ranking/World/Total?c={nickname}&w={value}"
        )

        normal_world_url = url.format(nickname=nickname, value=0)
        reboot_world_url = url.format(nickname=nickname, value=254)

        # 캐릭터 월드 조회
        normal_world_response = mua.util.scrap.getCharacterWorld(normal_world_url)
        time.sleep(1)
        reboot_world_response = mua.util.scrap.getCharacterWorld(reboot_world_url)

        # 일반 월드에 캐릭터 존재
        if len(normal_world_response) > 0:
            insertCharacter(nickname, "normal", url, normal_world_url)

        # 리부트 월드에 캐릭터 존재
        elif len(reboot_world_response) > 0:
            insertCharacter(nickname, "reboot", url, reboot_world_url)

        # 일반, 리부트 월드 캐릭터 존재하지 않음
        else:
            return redirect(url_for("main.main"))
        

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



def insertCharacter(nickname: str, world_type: str, base_url: str, search_url:str):
    """
    캐릭터 정보 삽입\n
    Args:
        nickname : 캐릭터 이름\n
        world_type : 월드 타입\n
        base_url : 기본 url\n
        search_url : 검색할 url 정보
    """
    time.sleep(1)
    total_character_info = mua.util.scrap.getCharacterInfo(search_url)

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

        KST = datetime.timezone(datetime.timedelta(hours=9))
        current_time = datetime.datetime.now(KST)

        # 일반월드 가져오기
        world_list = World.query.filter_by(type=world_type)

        # 모든 일반월드 조회하면서 캐릭터가 속해 있는 월드 확인
        for world in world_list:
            time.sleep(1)
            url = base_url.format(nickname=total_name, value=world.value)

            # 스크랩
            response: dict = mua.util.scrap.getCharacterWorld(url)
            time.sleep(1)

            if len(response) > 0:
                # 찾은 월드 정보로 캐릭터 조회
                world_character_info: dict = mua.util.scrap.getCharacterInfo(url)
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
