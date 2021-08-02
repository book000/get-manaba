import json
from unittest import TestCase

import src
from src import Manaba, get_task_status, get_your_status
from src.models.ManabaPortfolioType import get_portfolio_type_from_name
from src.models.ManabaResultViewType import get_result_view_type_from_name


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
        if "tests" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_course" not in self.config["tests"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_course, 0)

        for test in self.config["tests"]["test_get_course"]:
            course_id: int = test["course_id"]
            course_name = test["course_name"]
            print("course_name:" + course_name, "course_id:" + str(course_id))

            course = self.manaba.get_course(course_id)
            self.assertEqual(course.name, course_name, "テストデータに登録されているコース名と異なります。")

    def test_get_querys(self) -> None:
        if "tests" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_querys" not in self.config["tests"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_querys, 0)

        for test in self.config["tests"]["test_get_querys"]:
            course_id: int = test["course_id"]
            query_id: int = test["query_id"]
            query_title = test["query_title"]
            print("query_title:" + query_title, "query_id:" + str(query_id), "course_id:" + str(course_id))

            querys = self.manaba.get_querys(course_id)
            query_ids = list(map(lambda x: x.query_id, querys))
            query_names = list(map(lambda x: x.title, querys))
            self.assertIn(query_id, query_ids, "テストデータの小テストIDに合致するタイトルが見つかりません。")
            self.assertIn(query_title, query_names, "テストデータの小テストタイトルに合致するタイトルが見つかりません。")

    def test_get_query(self) -> None:
        if "tests" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_query" not in self.config["tests"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_query,
                          self.config["tests"]["test_get_query"][0]["course_id"], 0)

        for test in self.config["tests"]["test_get_query"]:
            course_id: int = test["course_id"]
            query_id: int = test["query_id"]
            query_title = test["query_title"]
            print("query_title:" + query_title, "course_id:" + str(course_id), "query_id:" + str(query_id))

            description = test["description"]
            reception_start_time = Manaba.process_datetime(test["reception_start_time"])
            self.assertNotEqual(None, reception_start_time, "テストデータとして渡された reception_start_time が正しくありません。")
            reception_end_time = Manaba.process_datetime(test["reception_end_time"])
            self.assertNotEqual(None, reception_end_time, "テストデータとして渡された reception_end_time が正しくありません。")
            portfolio_type = get_portfolio_type_from_name(test["portfolio_type"])
            result_view_type = get_result_view_type_from_name(test["result_view_type"])
            task_status = get_task_status(test["status"]["task_status"])
            self.assertNotEqual(None, task_status, "テストデータとして渡された task_status が正しくありません。")
            your_status = get_your_status(test["status"]["your_status"])
            self.assertNotEqual(None, your_status, "テストデータとして渡された task_status が正しくありません。")
            grade: int = test["grade"]
            below_percent = test["position"]["below_percent"]
            my_pos_percent = test["position"]["my_pos_percent"]
            above_percent = test["position"]["above_percent"]

            query = self.manaba.get_query(course_id, query_id)
            self.assertEqual(query_title, query.title, "課題タイトルが一致しません。")
            self.assertEqual(description, query.description, "課題説明が一致しません。")
            self.assertEqual(reception_start_time, query.reception_start_time, "受付開始時刻が一致しません。")
            self.assertEqual(reception_end_time, query.reception_end_time, "受付終了時刻が一致しません。")
            self.assertEqual(portfolio_type, query.portfolio_type, "ポートフォリオ種別が一致しません。")
            self.assertEqual(result_view_type, query.result_view_type, "採点結果と正解の公開が一致しません。")
            self.assertNotEqual(None, query.status, "課題の状態を取得できませんでした。")
            assert query.status is not None
            self.assertEqual(task_status, query.status.task_status, "課題の状態が一致しません。")
            self.assertEqual(your_status, query.status.your_status, "課題の提出状態が一致しません。")
            self.assertEqual(grade, query.grade, "成績が一致しません。")
            self.assertNotEqual(None, query.position, "成績ポジション情報を取得できませんでした。")
            assert query.position is not None
            self.assertEqual(below_percent, query.position.below_percent, "成績ポジションにおける自身より下の点数の割合が一致しません。")
            self.assertEqual(my_pos_percent, query.position.my_pos_percent, "成績ポジションにおける自身と同じ点数の割合が一致しません。")
            self.assertEqual(above_percent, query.position.above_percent, "成績ポジションにおける自身より上の点数の割合が一致しません。")

    def test_get_surveys(self) -> None:
        if "tests" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_surveys" not in self.config["tests"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_surveys, 0)

        for test in self.config["tests"]["test_get_surveys"]:
            course_id: int = test["course_id"]
            survey_id: int = test["survey_id"]
            survey_title = test["survey_title"]

            print("survey_title:" + survey_title, "course_id:" + str(course_id), "survey_id:" + str(survey_id))

            surveys = self.manaba.get_surveys(course_id)
            survey_ids = list(map(lambda x: x.survey_id, surveys))
            survey_names = list(map(lambda x: x.title, surveys))
            self.assertIn(survey_id, survey_ids, "テストデータのアンケートIDに合致するタイトルが見つかりません。")
            self.assertIn(survey_title, survey_names, "テストデータのアンケートタイトルに合致するタイトルが見つかりません。")

    def test_get_reports(self) -> None:
        if "tests" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_reports" not in self.config["tests"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(src.ManabaNotFound, self.manaba.get_reports, 0)

        for test in self.config["tests"]["test_get_reports"]:
            course_id: int = test["course_id"]
            report_id: int = test["report_id"]
            report_title = test["report_title"]
            print("report_title:" + report_title, "course_id:" + str(course_id), "report_id:" + str(report_id))

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
        if "tests" not in self.config:
            self.fail("コンフィグにテストデータがないため、失敗しました。")
        if "test_get_course" not in self.config["tests"]:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        for test in self.config["tests"]["test_get_course"]:
            course_id: int = test["course_id"]
            print("course_id:" + str(course_id))

            self.assertRaises(src.ManabaNotLoggedIn, self.manaba.get_course, course_id)
