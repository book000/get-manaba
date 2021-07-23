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

        self.assertTrue(self.manaba.login(username, password), "ログインに失敗しました")

        self.courses_count: dict[str, int] = {}

    def test_get_courses_from_thumbnail(self) -> None:
        # Change to thumbnail format
        response = self.manaba.session.get(self.base_url + "/ct/home_course?chglistformat=thumbnail")
        response.raise_for_status()

        courses = self.manaba.get_courses()
        self.courses_count["thumbnail"] = len(courses)
        self.assertGreater(len(courses), 0, "サムネイルコース一覧が取得できませんでした(0件)")

        self.check_courses_count()

    def test_get_courses_from_list(self) -> None:
        # Change to list format
        response = self.manaba.session.get(self.base_url + "/ct/home_course?chglistformat=list")
        response.raise_for_status()

        courses = self.manaba.get_courses()
        self.courses_count["list"] = len(courses)
        self.assertGreater(len(courses), 0, "リストコース一覧が取得できませんでした(0件)")

        self.check_courses_count()

    def test_get_courses_from_timetable(self) -> None:
        # Change to timetable format
        response = self.manaba.session.get(self.base_url + "/ct/home_course?chglistformat=timetable")
        response.raise_for_status()

        courses = self.manaba.get_courses()
        self.courses_count["timetable"] = len(courses)
        self.assertGreater(len(courses), 0, "タイムテーブルコース一覧が取得できませんでした(0件)")

        self.check_courses_count()

    def check_courses_count(self) -> None:
        """
        それぞれのコース数が同じかどうかを調べる
        """
        if "thumbnail" in self.courses_count and \
                "list" in self.courses_count:
            self.assertEquals(self.courses_count["thumbnail"], self.courses_count["list"],
                              "サムネイル({0})とリスト({1})の件数が異なります。".format(
                                  str(self.courses_count["thumbnail"]),
                                  str(self.courses_count["list"])))

        if "list" in self.courses_count and \
                "timetable" in self.courses_count:
            self.assertEquals(self.courses_count["list"], self.courses_count["timetable"],
                              "リスト({0})とタイムテーブル({1})の件数が異なります。".format(
                                  str(self.courses_count["list"]),
                                  str(self.courses_count["timetable"])))

        if "thumbnail" in self.courses_count and \
                "timetable" in self.courses_count:
            self.assertEquals(self.courses_count["thumbnail"], self.courses_count["timetable"],
                              "サムネイル({0})とタイムテーブル({1})の件数が異なります。".format(
                                  str(self.courses_count["thumbnail"]),
                                  str(self.courses_count["timetable"])))

    def test_get_course(self) -> None:
        if "test" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "get_course" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_course, 0)

        course_id: int = self.config["test"]["get_course"]["course_id"]
        course_name = self.config["test"]["get_course"]["course_name"]

        course = self.manaba.get_course(course_id)
        self.assertEqual(course_name, course.name, "テストデータに登録されているコース名と異なります。")

    def test_get_querys(self) -> None:
        if "test" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_querys" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_querys, 0)

        course_id: int = self.config["test"]["test_get_querys"]["course_id"]
        query_id: int = self.config["test"]["test_get_querys"]["query_id"]
        query_title = self.config["test"]["test_get_querys"]["query_title"]

        querys = self.manaba.get_querys(course_id)
        query_ids = list(map(lambda x: x.query_id, querys))
        query_names = list(map(lambda x: x.title, querys))
        self.assertIn(query_id, query_ids, "テストデータの小テストIDに合致するタイトルが見つかりません。")
        self.assertIn(query_title, query_names, "テストデータの小テストタイトルに合致するタイトルが見つかりません。")

    def test_get_surveys(self) -> None:
        if "test" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_surveys" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_surveys, 0)

        course_id: int = self.config["test"]["test_get_surveys"]["course_id"]
        survey_id: int = self.config["test"]["test_get_surveys"]["survey_id"]
        survey_title = self.config["test"]["test_get_surveys"]["survey_title"]

        surveys = self.manaba.get_surveys(course_id)
        survey_ids = list(map(lambda x: x.survey_id, surveys))
        survey_names = list(map(lambda x: x.title, surveys))
        self.assertIn(survey_id, survey_ids, "テストデータのアンケートIDに合致するタイトルが見つかりません。")
        self.assertIn(survey_title, survey_names, "テストデータのアンケートタイトルに合致するタイトルが見つかりません。")

    def test_get_reports(self) -> None:
        if "test" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_reports" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_reports, 0)

        course_id: int = self.config["test"]["test_get_reports"]["course_id"]
        report_id: int = self.config["test"]["test_get_reports"]["report_id"]
        report_title = self.config["test"]["test_get_reports"]["report_title"]

        reports = self.manaba.get_reports(course_id)
        report_ids = list(map(lambda x: x.report_id, reports))
        report_names = list(map(lambda x: x.title, reports))
        self.assertIn(report_id, report_ids, "テストデータのレポートIDに合致するタイトルが見つかりません。")
        self.assertIn(report_title, report_names, "テストデータのレポートタイトルに合致するタイトルが見つかりません。")


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
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "get_course" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        course_id: int = self.config["test"]["get_course"]["course_id"]

        self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_course, course_id)

    def test_get_querys(self) -> None:
        if "test" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_querys" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        course_id: int = self.config["test"]["test_get_querys"]["course_id"]

        self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_querys, course_id)

    def test_get_surveys(self) -> None:
        if "test" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_surveys" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        course_id: int = self.config["test"]["test_get_surveys"]["course_id"]

        self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_surveys, course_id)

    def test_get_reports(self) -> None:
        if "test" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_reports" not in self.config["test"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        course_id: int = self.config["test"]["test_get_reports"]["course_id"]

        self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_reports, course_id)
