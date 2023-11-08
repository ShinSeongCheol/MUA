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
        self.assertEqual(response.status, 200)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
