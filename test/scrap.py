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

    def test_getWholeWorldRank(self):
        """
        전체월드 랭킹 스크랩
        """
        URL = "https://maplestory.nexon.com/N23Ranking/World/Total?w=0"
        scrap.getRank(URL)
        self.assertEqual()

    def test_getAuroraWorldRank(self):
        """
        오로라 랭킹 스크랩
        """

    def test_getRedWorldRank(self):
        """
        레드 랭킹 스크랩
        """

    def test_getEnosisWorldRank(self):
        """
        이노시스 랭킹 스크랩
        """

    def test_getUnionWorldRank(self):
        """
        유니온 랭킹 스크랩
        """

    def test_getScaniaWorldRank(self):
        """
        스카니아 랭킹 스크랩
        """

    def test_getLunaWorldRank(self):
        """
        루나 랭킹 스크랩
        """

    def test_getZenithWorldRank(self):
        """
        제니스 랭킹 스크랩
        """

    def test_getCroixWorldRank(self):
        """
        크로아 랭킹 스크랩
        """

    def test_getVeraWorldRank(self):
        """
        베라 랭킹 스크랩
        """

    def test_getElysiumWorldRank(self):
        """
        엘리시움 랭킹 스크랩
        """

    def test_getArcaneWorldRank(self):
        """
        아케인 랭킹 스크랩
        """

    def test_getNovaWorldRank(self):
        """
        노바 랭킹 스크랩
        """

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
