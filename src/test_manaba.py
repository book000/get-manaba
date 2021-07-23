import json
from unittest import TestCase

import src
from src import Manaba


class TestManaba(TestCase):
    def setUp(self) -> None:
        """
        setup test
        """
        with open("config.json", encoding="utf-8") as f:
            self.config = json.load(f)

        self.base_url = self.config["base_url"]
        self.manaba = Manaba(self.base_url)

        username = self.config["username"]
        password = self.config["password"]

        self.assertTrue(self.manaba.login(username, password))

        self.courses_count: dict[str, int] = {}

    def test_get_courses_from_thumbnail(self) -> None:
        # Change to thumbnail format
        response = self.manaba.session.get(self.base_url + "/ct/home_course?chglistformat=thumbnail")
        response.raise_for_status()

        courses = self.manaba.get_courses()
        self.courses_count["thumbnail"] = len(courses)
        self.assertGreater(len(courses), 0)

        self.check_courses_count()

    def test_get_courses_from_list(self) -> None:
        # Change to list format
        response = self.manaba.session.get(self.base_url + "/ct/home_course?chglistformat=list")
        response.raise_for_status()

        courses = self.manaba.get_courses()
        self.courses_count["list"] = len(courses)
        self.assertGreater(len(courses), 0)

        self.check_courses_count()

    def test_get_courses_from_timetable(self) -> None:
        # Change to timetable format
        response = self.manaba.session.get(self.base_url + "/ct/home_course?chglistformat=timetable")
        response.raise_for_status()

        courses = self.manaba.get_courses()
        self.courses_count["timetable"] = len(courses)
        self.assertGreater(len(courses), 0)

        self.check_courses_count()

    def check_courses_count(self) -> None:
        """
        それぞれのコース数が同じかどうかを調べる
        """
        if "thumbnail" in self.courses_count and \
                "list" in self.courses_count:
            self.assertEquals(self.courses_count["thumbnail"], self.courses_count["list"])

        if "list" in self.courses_count and \
                "timetable" in self.courses_count:
            self.assertEquals(self.courses_count["list"], self.courses_count["timetable"])

        if "thumbnail" in self.courses_count and \
                "timetable" in self.courses_count:
            self.assertEquals(self.courses_count["thumbnail"], self.courses_count["timetable"])

    def test_get_course(self) -> None:
        if "test" not in self.config:
            self.fail()

        self.assertRaises(src.ManabaNotFound, self.manaba.get_course, 0)

        course_id: int = self.config["test"]["course_id"]
        course_name = self.config["test"]["course_name"]

        course = self.manaba.get_course(course_id)
        self.assertEqual(course_name, course.name)


class TestManabaNotLoggedIn(TestCase):
    def setUp(self) -> None:
        """
        setup test
        """
        with open("config.json", encoding="utf-8") as f:
            self.config = json.load(f)

        base_url = self.config["base_url"]
        self.manaba = Manaba(base_url)

    def test_get_courses(self) -> None:
        self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_courses)

    def test_get_course(self) -> None:
        if "test" not in self.config:
            self.fail()

        course_id: int = self.config["test"]["course_id"]

        self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_course, course_id)
