from mua.util.scrap import getCharacterInfo
from mua.models import Character
from mua import scheduler


URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"

@scheduler.scheduled_job('cron', second='*/10', args=(URL,))
def updateCharacterInfo(URL):
    result = getCharacterInfo(URL)

# bs.add_job(updateCharacterInfo, "cron", second="*/10", id="totalRank1", args=(URL,))
