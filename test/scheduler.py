import unittest
from mua.util import scrap
import sys
sys.path.insert(0, "E:\dev\python\project\MUA\mua")


class UnitTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_status(self):
        self.assertEqual(scrap.getMapleHomeResponse(), 200)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
