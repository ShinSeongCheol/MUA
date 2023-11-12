from mua.util.scrap import getCharacterInfo
from mua.models import Character
from mua import create_app, db
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.start()

app = create_app()


TOTAL_WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"


@scheduler.scheduled_job("cron", second="*/10", args=(TOTAL_WORLD_URL,))
def updateWorldRank(URL):
    with app.app_context():
        result = getCharacterInfo(URL)

        character = Character()
