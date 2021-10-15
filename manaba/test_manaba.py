import json
import os
from unittest import TestCase

import manaba
from manaba import Manaba
from manaba.models.ManabaFile import ManabaFile
from manaba.models.ManabaPortfolioType import get_portfolio_type_from_name
from manaba.models.ManabaResultViewType import get_result_view_type_from_name
from manaba.models.ManabaStudentReSubmitType import get_student_resubmit_type_from_name
from manaba.models.ManabaTaskStatusFlag import get_task_status_from_name
from manaba.models.ManabaTaskYourStatusFlag import get_your_status_from_name


class TestManaba(TestCase):
    def setUp(self) -> None:
        """
        setup test
        """
        self.maxDiff = None

        with open("config.json", encoding="utf-8") as f:
            self.config = json.load(f)

        if os.path.exists("tests.json"):
            with open("tests.json", encoding="utf-8") as f:
                self.tests = json.load(f)
        elif "tests" in self.config:
            self.tests = self.config["tests"]

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
        if "test_get_course" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_course, 0)

        for test in self.tests["test_get_course"]:
            course_id: int = test["course_id"]
            course_name = test["course_name"]
            print("course_name:" + course_name, "course_id:" + str(course_id))

            course = self.manaba.get_course(course_id)
            self.assertEqual(course.name, course_name, "テストデータに登録されているコース名と異なります。")

    def test_get_querys(self) -> None:
        if "test_get_querys" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_querys, 0)

        for test in self.tests["test_get_querys"]:
            course_id: int = test["course_id"]
            query_id: int = test["query_id"]
            query_title = test["query_title"]
            print("query_title:" + query_title, "query_id:" + str(query_id), "course_id:" + str(course_id))

            querys = self.manaba.get_querys(course_id)
            query_ids = list(map(lambda x: x.query_id, querys))
            query_titles = list(map(lambda x: x.title, querys))
            self.assertIn(query_id, query_ids, "テストデータの小テストIDに合致する小テストが見つかりません。")
            self.assertIn(query_title, query_titles, "テストデータの小テストタイトルに合致する小テストが見つかりません。")

    def test_get_query(self) -> None:
        if "test_get_query" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_query,
                          self.tests["test_get_query"][0]["course_id"], 0)

        for test in self.tests["test_get_query"]:
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
            task_status = get_task_status_from_name(test["status"]["task_status"])
            self.assertNotEqual(None, task_status, "テストデータとして渡された task_status が正しくありません。")
            your_status = get_your_status_from_name(test["status"]["your_status"])
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
        if "test_get_surveys" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_surveys, 0)

        for test in self.tests["test_get_surveys"]:
            course_id: int = test["course_id"]
            survey_id: int = test["survey_id"]
            survey_title = test["survey_title"]

            print("survey_title:" + survey_title, "course_id:" + str(course_id), "survey_id:" + str(survey_id))

            surveys = self.manaba.get_surveys(course_id)
            survey_ids = list(map(lambda x: x.survey_id, surveys))
            survey_titles = list(map(lambda x: x.title, surveys))
            self.assertIn(survey_id, survey_ids, "テストデータのアンケートIDに合致するアンケートが見つかりません。")
            self.assertIn(survey_title, survey_titles, "テストデータのアンケートタイトルに合致するアンケートが見つかりません。")

    def test_get_survey(self) -> None:
        if "test_get_survey" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_query,
                          self.tests["test_get_survey"][0]["course_id"], 0)

        for test in self.tests["test_get_survey"]:
            course_id: int = test["course_id"]
            survey_id: int = test["survey_id"]
            survey_title = test["survey_title"]
            print("survey_title:" + survey_title, "course_id:" + str(course_id), "survey_id:" + str(survey_id))

            reception_start_time = Manaba.process_datetime(test["reception_start_time"])
            self.assertNotEqual(None, reception_start_time, "テストデータとして渡された reception_start_time が正しくありません。")
            reception_end_time = Manaba.process_datetime(test["reception_end_time"])
            self.assertNotEqual(None, reception_end_time, "テストデータとして渡された reception_end_time が正しくありません。")
            portfolio_type = get_portfolio_type_from_name(test["portfolio_type"])
            student_resubmit_type = get_student_resubmit_type_from_name(test["student_resubmit_type"])
            self.assertNotEqual(None, student_resubmit_type, "テストデータとして渡された student_resubmit_type が正しくありません。")
            task_status = get_task_status_from_name(test["status"]["task_status"])
            self.assertNotEqual(None, task_status, "テストデータとして渡された task_status が正しくありません。")
            your_status = get_your_status_from_name(test["status"]["your_status"])
            self.assertNotEqual(None, your_status, "テストデータとして渡された task_status が正しくありません。")

            survey = self.manaba.get_survey(course_id, survey_id)
            self.assertEqual(survey_title, survey.title, "課題タイトルが一致しません。")
            self.assertEqual(reception_start_time, survey.reception_start_time, "受付開始時刻が一致しません。")
            self.assertEqual(reception_end_time, survey.reception_end_time, "受付終了時刻が一致しません。")
            self.assertEqual(portfolio_type, survey.portfolio_type, "ポートフォリオ種別が一致しません。")
            self.assertEqual(student_resubmit_type, survey.student_resubmit_type, "学生による再提出の許可が一致しません。")
            self.assertNotEqual(None, survey.status, "課題の状態を取得できませんでした。")
            assert survey.status is not None
            self.assertEqual(task_status, survey.status.task_status, "課題の状態が一致しません。")
            self.assertEqual(your_status, survey.status.your_status, "課題の提出状態が一致しません。")

    def test_get_reports(self) -> None:
        if "test_get_reports" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_reports, 0)

        for test in self.tests["test_get_reports"]:
            course_id: int = test["course_id"]
            report_id: int = test["report_id"]
            report_title = test["report_title"]
            print("report_title:" + report_title, "course_id:" + str(course_id), "report_id:" + str(report_id))

            reports = self.manaba.get_reports(course_id)
            report_ids = list(map(lambda x: x.report_id, reports))
            report_titles = list(map(lambda x: x.title, reports))
            self.assertIn(report_id, report_ids, "テストデータのレポートIDに合致するレポートが見つかりません。")
            self.assertIn(report_title, report_titles, "テストデータのレポートタイトルに合致するレポートが見つかりません。")

    def test_get_report(self) -> None:
        if "test_get_report" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_report,
                          self.tests["test_get_report"][0]["course_id"], 0)

        for test in self.tests["test_get_report"]:
            course_id: int = test["course_id"]
            report_id: int = test["report_id"]
            report_title = test["report_title"]
            print("survey_title:" + report_title, "course_id:" + str(course_id), "report_id:" + str(report_id))

            description = test["description"]
            reception_start_time = Manaba.process_datetime(test["reception_start_time"])
            self.assertNotEqual(None, reception_start_time, "テストデータとして渡された reception_start_time が正しくありません。")
            reception_end_time = Manaba.process_datetime(test["reception_end_time"])
            self.assertNotEqual(None, reception_end_time, "テストデータとして渡された reception_end_time が正しくありません。")
            portfolio_type = get_portfolio_type_from_name(test["portfolio_type"])
            student_resubmit_type = get_student_resubmit_type_from_name(test["student_resubmit_type"])
            self.assertNotEqual(None, student_resubmit_type, "テストデータとして渡された student_resubmit_type が正しくありません。")
            task_status = get_task_status_from_name(test["status"]["task_status"])
            self.assertNotEqual(None, task_status, "テストデータとして渡された task_status が正しくありません。")
            your_status = get_your_status_from_name(test["status"]["your_status"])
            self.assertNotEqual(None, your_status, "テストデータとして渡された task_status が正しくありません。")

            report = self.manaba.get_report(course_id, report_id)
            self.assertEqual(report_title, report.title, "課題タイトルが一致しません。")
            self.assertEqual(description, report.description, "課題説明が一致しません。")
            self.assertEqual(reception_start_time, report.reception_start_time, "受付開始時刻が一致しません。")
            self.assertEqual(reception_end_time, report.reception_end_time, "受付終了時刻が一致しません。")
            self.assertEqual(portfolio_type, report.portfolio_type, "ポートフォリオ種別が一致しません。")
            self.assertEqual(student_resubmit_type, report.student_resubmit_type, "学生による再提出の許可が一致しません。")
            self.assertNotEqual(None, report.status, "課題の状態を取得できませんでした。")
            assert report.status is not None
            self.assertEqual(task_status, report.status.task_status, "課題の状態が一致しません。")
            self.assertEqual(your_status, report.status.your_status, "課題の提出状態が一致しません。")

    def test_get_threads(self) -> None:
        if "test_get_threads" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_threads, 0)

        for test in self.tests["test_get_threads"]:
            course_id: int = test["course_id"]
            thread_id: int = test["thread_id"]
            thread_title = test["thread_title"]
            print("thread_title:" + thread_title, "course_id:" + str(course_id), "thread_id:" + str(thread_id))

            threads = self.manaba.get_threads(course_id)
            thread_ids = list(map(lambda x: x.thread_id, threads))
            thread_titles = list(map(lambda x: x.title, threads))
            self.assertIn(thread_id, thread_ids, "テストデータのスレッドIDに合致するスレッドが見つかりません。")
            self.assertIn(thread_title, thread_titles, "テストデータのスレッドタイトルに合致するスレッドが見つかりません。")

    def test_get_thread(self) -> None:
        if "test_get_thread" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_thread,
                          self.tests["test_get_thread"][0]["course_id"], 0)

        for test in self.tests["test_get_thread"]:
            course_id: int = test["course_id"]
            thread_id: int = test["thread_id"]
            thread_title = test["thread_title"]
            print("thread_title:" + thread_title, "course_id:" + str(course_id), "thread_id:" + str(thread_id))

            thread = self.manaba.get_thread(course_id, thread_id)

            self.assertEqual(thread_title, thread.title, "テストデータとして渡された thread_title が正しくありません。")

            self.assertNotEqual(None, thread.comments, "スレッドコメントデータが None です。")
            assert thread.comments is not None

            for comment in thread.comments:
                comment_test_matches = list(filter(lambda x: comment.comment_id == x["comment_id"], test["comments"]))
                if len(comment_test_matches) == 0:
                    continue

                comment_title = comment_test_matches[0]["title"]
                comment_author = comment_test_matches[0]["author"]
                comment_posted_at = Manaba.process_datetime(comment_test_matches[0]["posted_at"])
                comment_reply_to_id = comment_test_matches[0]["reply_to_id"]
                comment_deleted = comment_test_matches[0]["deleted"]
                comment_html = comment_test_matches[0]["html"]
                comment_files = comment_test_matches[0]["files"]

                self.assertEqual(comment_title, comment.title, "テストデータとして渡された title が正しくありません。")
                self.assertEqual(comment_author, comment.author, "テストデータとして渡された author が正しくありません。")
                self.assertEqual(comment_posted_at, comment.posted_at, "テストデータとして渡された posted_at が正しくありません。")
                self.assertEqual(comment_reply_to_id, comment.reply_to_id, "テストデータとして渡された reply_to_id が正しくありません。")
                self.assertEqual(comment_deleted, comment.deleted, "テストデータとして渡された deleted が正しくありません。")
                self.assertEqual(comment_html, comment.html, "テストデータとして渡された html が正しくありません。")

                for file in comment_files:
                    matches = list(filter(lambda x: x.name == file["name"], comment.files))
                    if len(matches) == 0:
                        self.fail("テストデータとして渡された name:" + file["name"] + " ファイルが見つかりません。")

                    match = matches[0]
                    self.assertEqual(Manaba.process_datetime(file["uploaded_at"]), match.uploaded_at,
                                     "テストデータとして渡された uploaded_at が正しくありません。")
                    self.assertEqual(file["download_url"], match.download_url, "テストデータとして渡された download_url が正しくありません。")

    def test_get_news_list(self) -> None:
        if "test_get_news_list" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_news,
                          self.tests["test_get_news_list"][0]["course_id"], 0)

        for test in self.tests["test_get_news_list"]:
            course_id: int = test["course_id"]
            news_id: int = test["news_id"]
            news_title = test["news_title"]
            print("news_title:" + news_title, "course_id:" + str(course_id), "news_id:" + str(news_id))

            news = self.manaba.get_news_list(course_id)
            news_ids = list(map(lambda x: x.news_id, news))
            news_titles = list(map(lambda x: x.title, news))
            self.assertIn(news_id, news_ids, "テストデータのニュースIDに合致するニュースが見つかりません。")
            self.assertIn(news_title, news_titles, "テストデータのニュースタイトルに合致するニュースが見つかりません。")

    def test_get_news(self) -> None:
        if "test_get_news" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_thread,
                          self.tests["test_get_news"][0]["course_id"], 0)

        for test in self.tests["test_get_news"]:
            course_id: int = test["course_id"]
            news_id: int = test["news_id"]
            news_title = test["news_title"]
            print("news_title:" + news_title, "course_id:" + str(course_id), "news_id:" + str(news_id))

            author = test["author"]
            posted_at = Manaba.process_datetime(test["posted_at"])
            last_edited_author = test["last_edited_author"]
            last_edited_at = Manaba.process_datetime(test["last_edited_at"])
            html = test["html"]
            files = test["files"]

            news = self.manaba.get_news(course_id, news_id)

            self.assertEqual(news_title, news.title, "テストデータとして渡された news_title が正しくありません。")
            self.assertEqual(author, news.author, "テストデータとして渡された author が正しくありません。")
            self.assertEqual(posted_at, news.posted_at, "テストデータとして渡された posted_at が正しくありません。")
            self.assertEqual(last_edited_author, news.last_edited_author, "テストデータとして渡された last_edited_author が正しくありません。")
            self.assertEqual(last_edited_at, news.last_edited_at, "テストデータとして渡された last_edited_at が正しくありません。")
            self.assertEqual(html, news.html, "テストデータとして渡された html が正しくありません。")

            for file in files:
                matches = list(filter(lambda x: x.name == file["name"], news.files))
                if len(matches) == 0:
                    self.fail("テストデータとして渡された name:" + file["name"] + " ファイルが見つかりません。")

                matched: ManabaFile = matches[0]
                self.assertEqual(Manaba.process_datetime(file["uploaded_at"]), matched.uploaded_at,
                                 "テストデータとして渡された uploaded_at が正しくありません。")
                self.assertEqual(file["download_url"], matched.download_url, "テストデータとして渡された download_url が正しくありません。")

    def test_get_contents(self) -> None:
        if "test_get_contents" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_contents, 0)

        for test in self.tests["test_get_contents"]:
            course_id: int = test["course_id"]
            content_id = test["content_id"]
            content_title = test["content_title"]
            content_description = test["content_description"]
            print("content_title:" + content_title, "course_id:" + str(course_id), "content_id:" + str(content_id))

            contents = self.manaba.get_contents(course_id)
            content_ids = list(map(lambda x: x.content_id, contents))
            content_titles = list(map(lambda x: x.title, contents))
            content_descriptions = list(map(lambda x: x.description, contents))
            self.assertIn(content_id, content_ids, "テストデータのコンテンツIDに合致するコンテンツが見つかりません。")
            self.assertIn(content_title, content_titles, "テストデータのコンテンツタイトルに合致するコンテンツが見つかりません。")
            if content_description is not None:
                self.assertIn(content_description, content_descriptions, "テストデータのコンテンツ説明に合致するコンテンツが見つかりません。")

    def test_get_content_pages(self) -> None:
        if "test_get_content_pages" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_content_pages, "")

        for test in self.tests["test_get_content_pages"]:
            content_id = test["content_id"]
            pages = test["pages"]

            content_pages = self.manaba.get_content_pages(content_id)
            page_ids = list(map(lambda x: x.page_id, content_pages))
            titles = list(map(lambda x: x.title, content_pages))

            for page in pages:
                page_id = page["page_id"]
                title = page["title"]

                self.assertIn(page_id, page_ids, "テストデータのページIDに合致するコンテンツが見つかりません。")
                self.assertIn(title, titles, "テストデータのページタイトルに合致するコンテンツが見つかりません。")

    def test_get_content_page(self) -> None:
        if "test_get_content_page" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        self.assertRaises(manaba.ManabaNotFound, self.manaba.get_content_page,
                          self.tests["test_get_content_page"][0]["content_id"], 1)

        for test in self.tests["test_get_content_page"]:
            content_id = test["content_id"]
            page_id: int = test["page_id"]

            course_id: int = test["course_id"]
            title = test["title"]

            print("title:" + title, "course_id:" + str(course_id), "content_id:" + content_id,
                  "page_id:" + str(page_id))

            author = test["author"]
            version: str = test["version"]
            viewable: bool = test["viewable"]
            last_edited_at = Manaba.process_datetime(test["last_edited_at"])
            publish_start_at = Manaba.process_datetime(test["publish_start_at"])
            publish_end_at = Manaba.process_datetime(test["publish_end_at"])
            html = test["html"]
            files = test["files"]

            content_page = self.manaba.get_content_page(content_id, page_id)
            self.assertEqual(course_id, content_page.course_id, "テストデータとして渡された course_id が正しくありません。")
            self.assertEqual(title, content_page.title, "テストデータとして渡された title が正しくありません。")
            self.assertEqual(author, content_page.author, "テストデータとして渡された author が正しくありません。")
            self.assertEqual(version, content_page.version, "テストデータとして渡された version が正しくありません。")
            self.assertEqual(viewable, content_page.viewable, "テストデータとして渡された viewable が正しくありません。")
            self.assertEqual(last_edited_at, content_page.last_edited_at, "テストデータとして渡された last_edited_at が正しくありません。")
            self.assertEqual(publish_start_at, content_page.publish_start_at,
                             "テストデータとして渡された publish_start_at が正しくありません。")
            self.assertEqual(publish_end_at, content_page.publish_end_at, "テストデータとして渡された publish_end_at が正しくありません。")
            self.assertEqual(html, content_page.html, "テストデータとして渡された html が正しくありません。")

            for file in files:
                matches = list(filter(lambda x: x.name == file["name"], content_page.files))
                if len(matches) == 0:
                    self.fail("テストデータとして渡された name:" + file["name"] + " ファイルが見つかりません。")

                match = matches[0]
                self.assertEqual(Manaba.process_datetime(file["uploaded_at"]), match.uploaded_at,
                                 "テストデータとして渡された uploaded_at が正しくありません。")
                self.assertEqual(file["download_url"], match.download_url, "テストデータとして渡された download_url が正しくありません。")


class TestManabaNotLoggedIn(TestCase):
    def setUp(self) -> None:
        """
        setup test
        """
        with open("config.json", encoding="utf-8") as f:
            self.config = json.load(f)

        if os.path.exists("tests.json"):
            with open("tests.json", encoding="utf-8") as f:
                self.tests = json.load(f)
        elif "tests" in self.config:
            self.tests = self.config["tests"]

        base_url = self.config["base_url"]
        self.manaba = Manaba(base_url)

    def test_get_courses(self) -> None:
        self.assertRaises(manaba.ManabaNotLoggedIn, self.manaba.get_courses)

    def test_get_course(self) -> None:
        if "test_get_course" not in self.tests:
            self.fail("コンフィグにこのテスト用のテストデータがないため、失敗しました。")

        for test in self.tests["test_get_course"]:
            course_id: int = test["course_id"]
            print("course_id:" + str(course_id))

            self.assertRaises(manaba.ManabaNotLoggedIn, self.manaba.get_course, course_id)
