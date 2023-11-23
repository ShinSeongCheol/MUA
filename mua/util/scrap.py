import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()


def getMapleHomeResponse():
    """
    메이플 홈페이지 응답
    """
    MAPLE_HOME_URL = "https://maplestory.nexon.com/Home/Main"
    response = requests.get(
        MAPLE_HOME_URL,
        headers={
            "user-Agent": ua.random,
        },
    )
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
    response = requests.get(
        URL,
        headers={
            "user-Agent": ua.random,
        },
    )

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


def getWorldInfo(URL):
    """
    주어진 URL의 월드 정보
    Args:
        URL: 월드 정보를 얻을 URL
    Returns:
        월드 정보(이름, 종류)
    """

    # 요청
    response = requests.get(
        URL,
        headers={
            "user-Agent": ua.random,
        },
    )

    # 응답 확인
    if not response.ok:
        return

    bs = BeautifulSoup(response.text, "html.parser")

    world_table_row = bs.select(
        "#container > div > div > div.rank_search_wrapper > table > tr"
    )

    normal_world = world_table_row[1].select("div:nth-child(1) > span")[0].text
    reboot_world = world_table_row[1].select("div:nth-child(2) > span")[0].text

    normal_world_chanal = world_table_row[1].select("div:nth-child(1) > ul > li > a")
    normal_world_chanal = [chanal.text for chanal in normal_world_chanal]

    normal_world_value = world_table_row[1].select("div:nth-child(1) > ul > li > input")
    normal_world_value = [value["value"] for value in normal_world_value]

    reboot_world_chanal = world_table_row[1].select("div:nth-child(2) > ul > li > a")
    reboot_world_chanal = [chanal.text for chanal in reboot_world_chanal]

    reboot_world_value = world_table_row[1].select("div:nth-child(2) > ul > li > input")
    reboot_world_value = [value["value"] for value in reboot_world_value]

    world_info = {}
    world_info[normal_world] = {}
    for i in range(1, len(normal_world_chanal)):
        world_info[normal_world][normal_world_chanal[i]] = normal_world_value[i]

    world_info[reboot_world] = {}
    for i in range(1, len(reboot_world_chanal)):
        world_info[reboot_world][reboot_world_chanal[i]] = reboot_world_value[i]

    return world_info


def getCharacterWorld(URL):
    """
    캐릭터 월드 정보 확인
    """

    # 요청
    response = requests.get(
        URL,
        headers={
            "user-Agent": ua.random,
        },
    )

    # 응답 확인
    if not response.ok:
        return

    bs = BeautifulSoup(response.text, "html.parser")

    table_row = bs.select(
        "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr"
    )

    return table_row
