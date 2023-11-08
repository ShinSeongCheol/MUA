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

    def test_getWholeWorldCharacterInfo(self):
        """
        전체월드 랭킹 스크랩
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
        self.assertEqual(expreience, "611,251,115,519,887")
        self.assertEqual(popularity, "28,624")
        self.assertEqual(guild, "지존")

    def test_getAuroraWorldCharacterInfo(self):
        """
        오로라 랭킹 스크랩
        """

    def test_getRedWorldCharacterInfo(self):
        """
        레드 랭킹 스크랩
        """

    def test_getEnosisWorldCharacterInfo(self):
        """
        이노시스 랭킹 스크랩
        """

    def test_getUnionWorldCharacterInfo(self):
        """
        유니온 랭킹 스크랩
        """

    def test_getScaniaWorldCharacterInfo(self):
        """
        스카니아 랭킹 스크랩
        """

    def test_getLunaWorldCharacterInfo(self):
        """
        루나 랭킹 스크랩
        """

    def test_getZenithWorldCharacterInfo(self):
        """
        제니스 랭킹 스크랩
        """

    def test_getCroixWorldCharacterInfo(self):
        """
        크로아 랭킹 스크랩
        """

    def test_getVeraWorldCharacterInfo(self):
        """
        베라 랭킹 스크랩
        """

    def test_getElysiumWorldCharacterInfo(self):
        """
        엘리시움 랭킹 스크랩
        """

    def test_getArcaneWorldCharacterInfo(self):
        """
        아케인 랭킹 스크랩
        """

    def test_getNovaWorldCharacterInfo(self):
        """
        노바 랭킹 스크랩
        """

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
