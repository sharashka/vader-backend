import unittest
from src import __version__


class TestHelpers(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        assert __version__ == "0.1.0"
