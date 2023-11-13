import unittest
from mua.util import scrap


class Unittest(unittest.TestCase):
    def setUp(self):
        pass

    def test_mapleHomeResponseStatus(self):
        """
        메이플 홈페이지 상태 확인
        """
        response = scrap.getMapleHomeResponse()
        self.assertEqual(response.status_code, 200)

    def test_firstCharacterInfo(self):
        """
        첫번째 캐릭터 정보 확인
        """
        URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"

        character_info = scrap.getCharacterInfo(URL)
        data: dict = character_info[0]
        rank = data.get("rank")
        image = data.get("image")
        name = data.get("name")
        occupation = data.get("occupation")
        level = data.get("level")
        expreience = data.get("expreience")
        popularity = data.get("popularity")
        guild = data.get("guild")

        self.assertEqual(rank, "1")
        self.assertEqual(
            image,
            "https://avatar.maplestory.nexon.com/Character/180/INIMBCNLKFOPHKPADGLEFIAOJAJOKDGMIFCDOMHDJDCCGGMCBFKCCOGBMFIOGHJOPKCDALEHEOMJANJPAJPGNEMKNPGIJGBGNPAFHOJKAAMBFFIEMGLGCIECIGCKBEEHLLBPMBPCJFBABDLIFMFBLCELFEGCIILPOKNFHENJAMGPBFONCPENGFPHCNPMDLEJNLICJLPACPDLHHHAICFPBHECGIOPHDHNEHNGHILJNEGFDMNIIABELDLEMFKFIONL.png",
        )
        self.assertEqual(name, "오지환")
        self.assertEqual(occupation, "키네시스")
        self.assertEqual(level, "295")
        self.assertEqual(expreience, "616,213,799,872,414")
        self.assertEqual(popularity, "28,624")
        self.assertEqual(guild, "지존")

    def test_lastCharaterInfo(self):
        """
        마지막 캐릭터 정보 확인
        """

        URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"

        character_info = scrap.getCharacterInfo(URL)
        data: dict = character_info[9]

        rank = data.get("rank")
        image = data.get("image")
        name = data.get("name")
        occupation = data.get("occupation")
        level = data.get("level")
        expreience = data.get("expreience")
        popularity = data.get("popularity")
        guild = data.get("guild")

        self.assertEqual(rank, "10")
        self.assertEqual(
            image,
            "https://avatar.maplestory.nexon.com/Character/180/BFKHAHNPHNMFMMGAKEHGPJFFADKAAAMIAICBOFCCEEFDLPNJMDCEJFFDLJNBKPOLADGECHDIAGKDLBOEHCFCAFMNKFOMJPAKNFKCJFODANJLGPNAEELGFGBNFJBPMCBIJFPBDMINODOLMLHDICIKIPLBHPDEABAHKKCKBEDLLJPKDGNKICHAJMCACHGDHIJODDMLOMPEAMKJKOCLCHFDFMEAMOFBGEEMFKDGLKKLGHIGPEKCPIIBKJEPOEHJLOMO.png",
        )
        self.assertEqual(name, "시바개")
        self.assertEqual(occupation, "아란")
        self.assertEqual(level, "293")
        self.assertEqual(expreience, "42,600,973,228,514")
        self.assertEqual(popularity, "4,370")
        self.assertEqual(guild, "아름다움")

    def test_worldInfo(self):
        """
        월드 이름과 종류를 확인
        """
        WORLD_INFO_URL = "https://maplestory.nexon.com/N23Ranking/World/Total"
        world_info = scrap.getWorldInfo(WORLD_INFO_URL)

        self.assertEqual(world_info, {'일반 월드': ['전체월드', '오로라', '레드', '이노시스', '유니온', '스카니아', '루나', '제니스', '크로아', '베라', '엘리시움', '아케인', '노바'], '리부트 월드': ['전체월드', '리부트2', '리부트']})


    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
