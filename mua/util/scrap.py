import requests
from bs4 import BeautifulSoup


def getMapleHomeResponse():
    """
    메이플 홈페이지 응답
    """
    MAPLE_HOME_URL = "https://maplestory.nexon.com/Home/Main"
    response = requests.get(MAPLE_HOME_URL)
    return response


def getCharacterInfo(URL: str):
    """
    주어진 URL의 10명의 캐릭터 정보
    Args:
        URL: 캐릭터 정보를 얻을 URL
    Returns:
        캐릭터 정보(랭크, 이미지, 이름, 직업, 레벨, 경험치, 인기도, 길드)
    """
    # URL의 페이지 정보
    response = requests.get(URL)

    # 정상 응답이 아니면 종료
    if not response.ok:
        return

    # 뷰티풀 수프 객체 생성
    bs = BeautifulSoup(response.text, "html.parser")
    table_row = bs.select(
        "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr"
    )

    # 캐릭터 정보 리스트
    character_info_list = []

    # 10위까지 반복
    for i in range(10):
        # 랭크
        rank = table_row[i].select("td > p")[0]
        if rank.find("img"):
            rank = rank.select("img")[0]["alt"][0:1]
        else:
            rank = rank.text.split()[0]

        # 캐릭터 이미지
        image = table_row[i].select("td > span > img")[0]["src"]

        # 캐릭터 이름
        name = table_row[i].select("td > dl > dt > a")[0].text

        # 캐릭터 직업
        occupation = table_row[i].select("td > dl > dd")[0].text.split("/")[1].strip()

        # 캐릭터 레벨
        level = table_row[i].select("td:nth-child(3)")[0].text.split("Lv.")[1]

        # 캐릭터 경험치
        expreience = table_row[i].select("td:nth-child(4)")[0].text

        # 캐릭터 인기도
        popularity = table_row[i].select("td:nth-child(5)")[0].text

        # 캐릭터 길드
        guild = table_row[i].select("td:nth-child(6)")[0].text

        # 캐릭터 정보 딕셔너리 생성
        character_info = {
            "rank": rank,
            "image": image,
            "name": name,
            "occupation": occupation,
            "level": level,
            "expreience": expreience,
            "popularity": popularity,
            "guild": guild,
        }

        # 캐릭터 정보 리스트에 딕셔너리 추가
        character_info_list.append(character_info)

    return character_info_list
