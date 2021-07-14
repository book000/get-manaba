import json
from unittest import TestCase

from src import Manaba


class TestManaba(TestCase):
    def setUp(self):
        with open("config.json") as f:
            self.config = json.load(f)

        base_url = self.config["base_url"]

        self.manaba = Manaba(base_url)


class TestManabaLogin(TestManaba):
    def test_login(self):
        username = self.config["username"]
        password = self.config["password"]

        self.manaba.login(username, password)
