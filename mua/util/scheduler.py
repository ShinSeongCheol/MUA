from mua.util.scrap import getCharacterInfo, getWorldInfo
from mua.models import World
from mua import db


def updateWorld(app, url):
    """
    월드 이름과 종류를 업데이트 하기 위한 함수
    """
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


TOTAL_WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"


def updateWorldRank(URL):
    response = getCharacterInfo(URL)
