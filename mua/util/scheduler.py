from mua.util.scrap import getCharacterInfo, getWorldInfo
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.start()


WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total"


@scheduler.scheduled_job("cron", second="*/20", args=(WORLD_URL,))
def updateWorld(WORLD_URL):
    """
    월드 이름과 종류를 업데이트 하기 위한 함수
    """
    response = getWorldInfo(WORLD_URL)


TOTAL_WORLD_URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"


@scheduler.scheduled_job("cron", second="*/10", args=(TOTAL_WORLD_URL,))
def updateWorldRank(URL):
    response = getCharacterInfo(URL)
