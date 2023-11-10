from apscheduler.schedulers.background import BackgroundScheduler
from mua.util.scrap import getCharacterInfo

bs = BackgroundScheduler()
bs.start()

def updateCharacterInfo():
    URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"
    bs.add_job(getCharacterInfo, "cron", second="*/10", id="totalRank", args=(URL,))
