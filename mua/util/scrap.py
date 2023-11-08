import requests
from bs4 import BeautifulSoup


def getMapleHomeResponse():
    """
    메이플 홈페이지 응답
    """
    MAPLE_HOME_URL = "https://maplestory.nexon.com/Home/Main"
    response = requests.get(MAPLE_HOME_URL)
    return response



