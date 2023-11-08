import requests
from bs4 import BeautifulSoup


def getMapleHomeResponse():
    MAPLE_HOME_URL = "https://maplestory.nexon.com/Home/Main"
    response = requests.get(MAPLE_HOME_URL)
    return response.status_code
