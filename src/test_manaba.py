import json
from unittest import TestCase

import src
from src import Manaba


class TestManaba(TestCase):
    def setUp(self) -> None:
        """
        setup test
        """
        with open("config.json") as f:
            self.config = json.load(f)

        self.base_url = self.config["base_url"]
        self.manaba = Manaba(self.base_url)

        username = self.config["username"]
        password = self.config["password"]

        self.assertTrue(self.manaba.login(username, password))

    def test_get_courses_from_thumbnail(self) -> None:
        # Change to thumbnail format
        response = self.manaba.session.get(self.base_url + "/ct/home_course?chglistformat=thumbnail")
        response.raise_for_status()

        courses = self.manaba.get_courses()
        self.assertGreater(len(courses), 0)


class TestManabaNotLoggedIn(TestCase):
    def setUp(self) -> None:
        """
        setup test
        """
        with open("config.json") as f:
            self.config = json.load(f)

        base_url = self.config["base_url"]
        self.manaba = Manaba(base_url)

    def test_get_courses(self) -> None:
        self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_courses)
