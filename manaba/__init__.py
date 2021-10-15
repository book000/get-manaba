# coding: utf-8
"""
Library for get various information about manaba.

manabaのさまざまな情報を取得するためのライブラリです。
"""
import datetime
import re
from typing import Optional, Union
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import bs4.element
import requests
from bs4 import BeautifulSoup
from requests import Response

from manaba.models.ManabaContent import ManabaContent
from manaba.models.ManabaContentPage import ManabaContentPage
from manaba.models.ManabaCourse import ManabaCourse
from manaba.models.ManabaCourseLamps import ManabaCourseLamps
from manaba.models.ManabaCourseNews import ManabaCourseNews
from manaba.models.ManabaFile import ManabaFile
from manaba.models.ManabaGradePosition import ManabaGradePosition
from manaba.models.ManabaPortfolioType import get_portfolio_type
from manaba.models.ManabaQuery import ManabaQuery
from manaba.models.ManabaQueryDetails import ManabaQueryDetails
from manaba.models.ManabaReport import ManabaReport
from manaba.models.ManabaReportDetails import ManabaReportDetails
from manaba.models.ManabaResultViewType import get_result_view_type
from manaba.models.ManabaStudentReSubmitType import get_student_resubmit_type
from manaba.models.ManabaSurvey import ManabaSurvey
from manaba.models.ManabaSurveyDetails import ManabaSurveyDetails
from manaba.models.ManabaTaskStatus import ManabaTaskStatus
from manaba.models.ManabaTaskStatusFlag import ManabaTaskStatusFlag, get_task_status
from manaba.models.ManabaTaskYourStatusFlag import ManabaTaskYourStatusFlag, get_your_status
from manaba.models.ManabaThread import ManabaThread
from manaba.models.ManabaThreadComment import ManabaThreadComment

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


class Manaba:
    """
    manaba 基本ライブラリ
    """

    def __init__(self,
                 base_url: str) -> None:
        self.session: requests.Session = requests.Session()
        self.__base_url: str = base_url
        self.__logged_in: bool = False
        self.__response: Optional[Response] = None

    def login(self,
              username: str,
              password: str) -> bool:
        """
        manaba にログインする

        Args:
            username: manaba ユーザー名
            password: manaba パスワード

        Returns:
            bool: ログインできたか
        """
        self.__response = self.session.get(urljoin(self.__base_url, "/ct/login"))
        if self.__response.status_code != 200:
            return False
        soup = BeautifulSoup(self.__response.text, "html5lib")

        login_form_box = soup.find("div", {"id": "login-form-box"})
        session_value1 = login_form_box.find("input", {"name": "SessionValue1"}).get("value")
        session_value = login_form_box.find("input", {"name": "SessionValue"}).get("value")
        login_value = login_form_box.find("input", {"name": "login"}).get("value")

        self.__response = self.session.post(urljoin(self.__base_url, "/ct/login"), params={
            "userid": username,
            "password": password,
            "login": login_value,
            "manaba-form": "1",
            "sessionValue1": session_value1,
            "sessionValue": session_value
        })

        self.__logged_in = self.__response.status_code == 200

        return self.__logged_in

    def get_course(self,
                   course_id: int) -> ManabaCourse:
        """
        指定したコース ID のコース情報(ManabaCourse)を取得します。

        Args:
            course_id: 取得するコースのコース ID

        Returns:
            ManabaCourse: 取得するコースのコース ID
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        title = soup.find("a", {"id": "coursename"}).text
        teacher = soup.find("span", {"class": "courseteacher"}).text
        lecture_at = soup.find("span", {"class": "coursedata-info"}).find("span").text
        year = int(soup.find("span", {"class": "coursedata-info"}).text.replace(lecture_at, ""))

        return ManabaCourse(title, course_id, year, lecture_at, teacher, None)

    def get_courses(self) -> list[ManabaCourse]:
        """
        参加しているコース情報を取得する

        Returns:
            list[ManabaCourse]: 参加しているコース情報

        Notes:
            詳細情報は :func:`manaba.Manaba.get_course` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(urljoin(self.__base_url, "/ct/home_course"))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        if soup.find("ul", {"class": "infolist-tab"}) is None:
            raise ManabaInternalError()

        correct_list_format_href: str = soup \
            .find("ul", {"class": "infolist-tab"}) \
            .find("li", {"class": "current"}) \
            .find("a") \
            .get("href")
        correct_list_format = parse_qs(urlparse(correct_list_format_href).query)["chglistformat"][0]

        my_courses = soup.find("div", {"class": "mycourses-body"})

        if correct_list_format == "thumbnail":
            return self._get_courses_from_thumbnail(my_courses)
        if correct_list_format == "list":
            return self._get_courses_from_list(my_courses)
        if correct_list_format == "timetable":
            return self._get_courses_from_timetable(my_courses, soup.find("table", {"class": "courselist"}))

        return []

    def _get_courses_from_thumbnail(self,
                                    my_courses: bs4.element.Tag) -> list[ManabaCourse]:
        """
        参加しているコース情報を取得する (サムネイル表示の場合)

        Args:
            my_courses: コース一覧のHTMLタグエレメント

        Returns:
            list[ManabaCourse]: 参加しているコース情報
        """
        course_cards = my_courses.find_all("div", {"class": "coursecard"})

        courses = []
        course_card: bs4.element.Tag
        for course_card in course_cards:
            title_link = course_card.find("div", {"class": "course-card-title"}).find("a")
            course_name = title_link.text.strip()
            course_link = title_link.get("href")
            course_id: int = int(re.sub(r"course_([0-9]+)", r"\1", course_link))

            course_items: bs4.element.Tag = course_card.find("dl", {"class": "courseitems"})
            dts = course_items.find_all("dt", {"class": "courseitemtext"}, recursive=False)
            dds = course_items.find_all("dd", {"class": "courseitemdetail"}, recursive=False)

            year: Optional[int] = None
            lecture_at: Optional[str] = None
            teacher: Optional[str] = None

            dt: bs4.element.Tag
            dd: bs4.element.Tag
            for dt, dd in zip(dts, dds):
                dt_text = dt.text.strip()
                dd_text = dd.text.strip()

                if dt_text == "時限":
                    lecture_at = dd.find("span").text
                    year = int(dd_text.replace(dd.find("span").text, ""))
                elif dt_text == "担当":
                    teacher = dd_text

            status_lamps = self._get_lamps_from_card(course_card.find("div", {"class": "course-card-status"}))

            courses.append(ManabaCourse(course_name, course_id, year, lecture_at, teacher, status_lamps))

        return courses

    def _get_courses_from_list(self,
                               my_courses: bs4.element.Tag) -> list[ManabaCourse]:
        """
        参加しているコース情報を取得する (リスト表示の場合)

        Args:
            my_courses: コース一覧のHTMLタグエレメント

        Returns:
            list[ManabaCourse]: 参加しているコース情報
        """
        course_rows = my_courses.find_all("tr", {"class": "courselist-c"})

        courses = []
        for course_row in course_rows:
            course_name = course_row.find("span", {"class": "courselist-title"}).text.strip()
            course_link = course_row.find("span", {"class": "courselist-title"}).find("a").get("href")
            course_id: int = int(re.sub(r"course_([0-9]+)", r"\1", course_link))

            status_lamps = self._get_lamps_from_card(course_row.find("div", {"class": "course-card-status"}))
            course_tds = course_row.find_all("td")
            course_year = int(course_tds[1].text.strip()) if len(course_tds) > 1 else None
            course_time = course_tds[2].text.strip() if len(course_tds) > 2 else None
            course_teacher = course_tds[3].text.strip() if len(course_tds) > 3 else None

            courses.append(ManabaCourse(course_name, course_id, course_year, course_time, course_teacher, status_lamps))

        return courses

    def _get_courses_from_timetable(self,
                                    my_courses: bs4.element.Tag,
                                    course_list: bs4.element.Tag) \
            -> list[ManabaCourse]:
        """
        参加しているコース情報を取得する (曜日表示の場合)

        Args:
            my_courses: コース一覧のHTMLタグエレメント

        Returns:
            list[ManabaCourse]: 参加しているコース情報
        """
        course_cards = my_courses.find_all("div", {"class": "courselistweekly-c"})

        courses = []
        for course_card in course_cards:
            course_name = course_card.find("a").text.strip()
            course_link = course_card.find("a").get("href")
            course_id: int = int(re.sub(r"course_([0-9]+)", r"\1", course_link))

            status_lamps = self._get_lamps_from_card(course_card.find("div", {"class": "coursestatus"}))

            courses.append(ManabaCourse(course_name, course_id, None, None, None, status_lamps))

        other_courses = self._get_courses_from_list(course_list)
        courses.extend(other_courses)

        return courses

    @staticmethod
    def _get_lamps_from_card(course_status: bs4.element.Tag) -> ManabaCourseLamps:
        """
        カードからステータスランプを取得する

        Args:
            course_status: カードのHTMLタグエレメント

        Returns:
            ManabaCourseLamps: コースステータスランプ
        """
        course_statuses = course_status \
            .find_all("img")
        return ManabaCourseLamps(
            course_statuses[0].get("src").endswith("on.png"),
            course_statuses[1].get("src").endswith("on.png"),
            course_statuses[2].get("src").endswith("on.png"),
            course_statuses[3].get("src").endswith("on.png"),
            course_statuses[4].get("src").endswith("on.png")
        )

    def get_querys(self,
                   course_id: int) -> list[ManabaQuery]:
        """
        指定したコースの小テスト一覧を取得します。

        Args:
            course_id: 取得するコースのコース ID

        Returns:
            list[ManabaQuery]: コースの小テスト一覧

        Notes:
            詳細情報は :func:`manaba.Manaba.get_query` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_query")
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")
        std_list = soup.find("table", {"class": "stdlist"})
        if std_list is None:
            return []

        query_tags = std_list.find_all("tr", class_=["row", "row0", "row1"])
        querys = []
        for query_tag in query_tags:
            query_td_tags = query_tag.findAll("td")
            query_title = query_tag.find("h3").text.strip()
            query_status_lamp = query_tag.find("h3").find("img").get("src").endswith("on.png")
            query_link = query_tag.find("h3").find("a").get("href")
            query_id: int = int(re.sub(r"course_[0-9]+_query_([0-9]+)", r"\1", query_link))

            query_status = self._parse_status(query_td_tags[1].text.strip())

            query_start_time = self.process_datetime(query_td_tags[2].text.strip())
            query_end_time = self.process_datetime(query_td_tags[3].text.strip())

            querys.append(ManabaQuery(
                course_id,
                query_id,
                query_title,
                query_status,
                query_status_lamp,
                query_start_time,
                query_end_time
            ))

        return querys

    def get_query(self,
                  course_id: int,
                  query_id: int) -> ManabaQueryDetails:
        """
        指定したコース・小テスト ID の小テスト詳細情報を取得します。

        Args:
            course_id: 取得する小テストのコース ID
            query_id: 取得する小テストの小テスト ID

        Returns:
            ManabaQueryDetails: 小テスト詳細情報
        """

        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_query_" + str(query_id))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        if soup.find("table", {"class": "stdlist-query"}) is None:
            raise ManabaNotFound()

        query_title = soup.find("tr", {"class": "title"}).text.strip()

        details = {}
        detail_trs = soup.find("table", {"class": "stdlist-query"}).find_all("tr")
        for tr in detail_trs:
            if tr.get("class") == "title":
                continue

            th = tr.find("th")
            td = tr.find("td")
            if th is None or td is None:
                continue

            details[th.text.strip()] = td.text.strip()

        portfolio_type = get_portfolio_type(self._opt_value(details, "ポートフォリオ"))
        result_view_type = get_result_view_type(self._opt_value(details, "採点結果と正解の公開"))

        status_value = self._opt_value(details, "状態")
        status = None
        if status_value is not None:
            if soup.find("table", {"class": "stdlist-query"}).find("span", {"class": "expired"}) is not None:
                status = ManabaTaskStatus(ManabaTaskStatusFlag.CLOSED, ManabaTaskYourStatusFlag.UNSUBMITTED)
            else:
                status = self._parse_status(status_value)

        gradelist = soup.find("table", {"class": "gradelist"})
        grade: Union[int, None] = None
        position = None
        if gradelist is not None:
            grade_str = gradelist.find("td", {"class": "grade"}).text
            try:
                grade = int(grade_str)
            except ValueError:
                grade = None

            position = self._parse_grade_bar(gradelist)

        return ManabaQueryDetails(
            course_id,
            query_id,
            query_title,
            self._opt_value(details, "課題に関する説明"),
            self.process_datetime(self._opt_value(details, "受付開始日時")),
            self.process_datetime(self._opt_value(details, "受付終了日時")),
            portfolio_type,
            result_view_type,
            status,
            grade,
            position
        )

    def get_surveys(self,
                    course_id: int) -> list[ManabaSurvey]:
        """
        指定したコースのアンケート一覧を取得します。

        Args:
            course_id: 取得するコースのコース ID

        Returns:
            list[ManabaSurvey]: コースのアンケート一覧

        Notes:
            詳細情報は :func:`manaba.Manaba.get_survey` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_survey")
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")
        std_list = soup.find("table", {"class": "stdlist"})
        if std_list is None:
            return []

        survey_tags = std_list.find_all("tr", class_=["row", "row0", "row1"])
        surveys = []
        for survey_tag in survey_tags:
            survey_td_tags = survey_tag.findAll("td")
            survey_title = survey_tag.find("h3").text.strip()
            survey_status_lamp = survey_tag.find("h3").find("img").get("src").endswith("on.png")
            survey_link = survey_tag.find("h3").find("a").get("href")
            survey_id: int = int(re.sub(r"course_[0-9]+_survey_([0-9]+)", r"\1", survey_link))

            survey_status = self._parse_status(survey_td_tags[1].text.strip())

            survey_start_time = self.process_datetime(survey_td_tags[2].text.strip())
            survey_end_time = self.process_datetime(survey_td_tags[3].text.strip())

            surveys.append(ManabaSurvey(
                course_id,
                survey_id,
                survey_title,
                survey_status,
                survey_status_lamp,
                survey_start_time,
                survey_end_time
            ))

        return surveys

    def get_survey(self,
                   course_id: int,
                   survey_id: int) -> ManabaSurveyDetails:
        """
        指定したコース・アンケート ID のアンケート詳細情報を取得します。

        Args:
            course_id: 取得するアンケートのコース ID
            survey_id:取得するアンケートのアンケート ID

        Returns:
            ManabaSurveyDetails: アンケート詳細情報
        """

        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_survey_" + str(survey_id))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        if soup.find("table", {"class": "stdlist-query"}) is None:
            raise ManabaNotFound()

        survey_title = soup.find("tr", {"class": "title"}).text.strip()

        details = {}
        detail_trs = soup.find("table", {"class": "stdlist-query"}).find_all("tr")
        for tr in detail_trs:
            if tr.get("class") == "title":
                continue

            th = tr.find("th")
            td = tr.find("td")
            if th is None or td is None:
                continue

            details[th.text.strip()] = td.text.strip()

        portfolio_type = get_portfolio_type(self._opt_value(details, "ポートフォリオ"))
        student_resubmit_type = get_student_resubmit_type(self._opt_value(details, "学生による再提出の許可"))

        status_value = self._opt_value(details, "状態")
        status = None
        if status_value is not None:
            if soup.find("table", {"class": "stdlist-query"}).find("span", {"class": "expired"}) is not None:
                status = ManabaTaskStatus(ManabaTaskStatusFlag.CLOSED, ManabaTaskYourStatusFlag.UNSUBMITTED)
            else:
                status = self._parse_status(status_value)

        return ManabaSurveyDetails(
            course_id,
            survey_id,
            survey_title,
            self.process_datetime(self._opt_value(details, "受付開始日時")),
            self.process_datetime(self._opt_value(details, "受付終了日時")),
            portfolio_type,
            student_resubmit_type,
            status
        )

    def get_reports(self,
                    course_id: int) -> list[ManabaReport]:
        """
        指定したコースのレポート一覧を取得します。

        Args:
            course_id: 取得するコースのコース ID

        Returns:
            list[ManabaReport]: コースのレポート一覧

        Notes:
            詳細情報は :func:`manaba.Manaba.get_report` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_report")
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")
        std_list = soup.find("table", {"class": "stdlist"})
        if std_list is None:
            return []

        report_tags = std_list.find_all("tr", class_=["row", "row0", "row1"])
        reports = []
        for report_tag in report_tags:
            report_td_tags = report_tag.findAll("td")
            report_title = report_tag.find("h3").text.strip()
            report_status_lamp = report_tag.find("h3").find("img").get("src").endswith("on.png")
            report_link = report_tag.find("h3").find("a").get("href")
            report_id: int = int(re.sub(r"course_[0-9]+_report_([0-9]+)", r"\1", report_link))

            report_status = self._parse_status(report_td_tags[1].text.strip())

            report_start_time = self.process_datetime(report_td_tags[2].text.strip())
            report_end_time = self.process_datetime(report_td_tags[3].text.strip())

            reports.append(ManabaReport(
                course_id,
                report_id,
                report_title,
                report_status,
                report_status_lamp,
                report_start_time,
                report_end_time
            ))

        return reports

    def get_report(self,
                   course_id: int,
                   report_id: int) -> ManabaReportDetails:
        """
        指定したコース・レポート ID のレポート詳細情報を取得します。

        Args:
            course_id: 取得するレポートのコース ID
            report_id: 取得するレポートのレポート ID

        Returns:
            ManabaReportDetails: レポート詳細情報
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_report_" + str(report_id))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        if soup.find("table", {"class": "stdlist-report"}) is None:
            raise ManabaNotFound()

        report_title = soup.find("tr", {"class": "title"}).text.strip()

        details = {}
        detail_trs = soup.find("table", {"class": "stdlist-report"}).find_all("tr")
        for tr in detail_trs:
            if tr.get("class") == "title":
                continue

            th = tr.find("th")
            td = tr.find("td")
            if th is None or td is None:
                continue
            for tag in td.find_all("br"):
                tag.replace_with("\n")

            details[th.text.strip()] = td.text.strip()

        portfolio_and_view_settings = self._opt_value(details, "ポートフォリオ / 閲覧設定")
        portfolio_type = None
        result_view_type = None
        if portfolio_and_view_settings is not None and " / " in portfolio_and_view_settings:
            portfolio_type = get_portfolio_type(portfolio_and_view_settings.split(" / ")[0])
            result_view_type = get_result_view_type(portfolio_and_view_settings.split(" / ")[1])

        student_resubmit_type = get_student_resubmit_type(self._opt_value(details, "学生による再提出の許可"))

        status_value = self._opt_value(details, "状態")
        status = None
        if status_value is not None:
            if (soup.find("table", {"class": "stdlist-report"}).find("span", {"class": "expired"}) is not None) or \
                    (soup.find("div", {"class": "report-form"}) is not None and
                     soup.find("div", {"class": "report-form"}).find("span", {"class": "expired"}) is not None):
                status = ManabaTaskStatus(ManabaTaskStatusFlag.CLOSED, ManabaTaskYourStatusFlag.UNSUBMITTED)
            else:
                status = self._parse_status(status_value)

        return ManabaReportDetails(
            course_id,
            report_id,
            report_title,
            self._opt_value(details, "課題に関する説明"),
            self.process_datetime(self._opt_value(details, "受付開始日時")),
            self.process_datetime(self._opt_value(details, "受付終了日時")),
            portfolio_type,
            result_view_type,
            student_resubmit_type,
            status
        )

    def get_threads(self,
                    course_id: int) -> list[ManabaThread]:
        """
        指定したコースのスレッド一覧を取得します。

        Args:
            course_id: 取得するコースのコース ID

        Returns:
            list[ManabaThread]: コースのスレッド一覧

        Notes:
            詳細情報は :func:`manaba.Manaba.get_thread` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_topics")
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        std_list = soup.find("table", {"class": "stdlist"})
        if std_list is None:
            return []

        thread_tags = std_list.find_all("tr", class_=["row", "row0", "row1"])
        threads = []
        for thread_tag in thread_tags:
            thread_title = thread_tag.find("span", {"class": "thread-title"}).text.strip()
            thread_link = thread_tag.find("a", {"class": "threadhead"}).get("href")
            thread_id: int = int(re.sub(r"course_[0-9]+_topics_([0-9]+)_.+", r"\1", thread_link))

            threads.append(ManabaThread(
                course_id,
                thread_id,
                thread_title,
                None
            ))

        return threads

    def get_thread(self,
                   course_id: int,
                   thread_id: int,
                   start_id: Optional[int] = None,
                   page_len: int = 10000) -> ManabaThread:
        """
        指定したコース・スレッド ID のスレッド詳細情報を取得します。

        Args:
            course_id: 取得するコースのコース ID
            thread_id: 取得するスレッドのスレッド ID
            start_id: 直近から何番目から取得するか (指定しない場合はすべて)
            page_len: 1 ページで最大何件コメント取得するか (指定しない場合は 10000 件)

        Returns:
            ManabaThread: スレッド詳細情報

        Notes:
            start_id の仕様は manaba 自体の仕様ですが、特殊です。スレッドのコメント数が 50 個ある場合、start_id に 5 を指定すると 45 件目以前を取得します。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        params = {
            "pagelen": page_len
        }
        if start_id is not None:
            params["start_id"] = start_id

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_topics_" + str(
                thread_id) + "_tflat?" + urlencode(params))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        comments: list[ManabaThreadComment] = []
        comment_tags = soup.find_all("div", {"class": "articlecontainer"})
        for comment_tag in comment_tags:
            comment_id: int = int(comment_tag.find("h3", {"class": "articlenumber"}).text.strip())
            comment_title: str = comment_tag.find("div", {"class": "articlesubject"}).text.strip()
            comment_body: bs4.element.Tag = comment_tag.find("div", {"class": "articlebody-msgbody"})
            article_info: bs4.element.Tag = comment_tag.find("div", {"class": "articleinfo"})

            # 以下、投稿者名と投稿日時が正常に取れない可能性あり
            comment_author: Optional[str] = None
            comment_date: Optional[str] = None
            if article_info.find("span", {"class": "posted-time"}) is not None:
                if article_info.find("a", {"href": "#"}) is not None:
                    # リンクになっている投稿者情報があればそれ
                    comment_author = article_info.find("a").text.strip()
                else:
                    # リンクがなければ投稿後のひとつ前のタグ
                    comment_author = str(
                        article_info.find("span", {"class": "posted-time"}).previous_sibling.string).strip()

                comment_date = article_info.find("span", {"class": "posted-time"}).text.strip()

            reply_to_id = None
            if comment_tag.find("div", {"class": "parentmsg-no"}) is not None:
                reply_to_id = int(comment_tag.find("div", {"class": "parentmsg-no"}).text.strip())

            deleted = comment_tag.find("div", {"class": "articlecontainer-deleted"}) is not None

            manaba_thread_comment = ManabaThreadComment(
                course_id,
                thread_id,
                comment_id,
                comment_title,
                comment_author,
                self.process_datetime(comment_date),
                reply_to_id,
                deleted,
                str(comment_body).replace(" ", "&nbsp;").strip()
            )

            attachments = comment_tag.find_all("div", {"class": "inlineattachment"})
            for attachment in attachments:
                a_tag = attachment.find("div", {"class": "inlineaf-description"}).find("a")
                manaba_thread_comment.add_file(ManabaFile(
                    manaba_thread_comment,
                    re.sub(r"(.+?) - ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", r"\1",
                           a_tag.text).strip(),
                    self.process_datetime(
                        re.sub(r"(.+?) - ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", r"\2",
                               a_tag.text).strip()),
                    urljoin(self.__base_url + "/ct/", a_tag.get("href"))
                ))

            comments.append(manaba_thread_comment)

        return ManabaThread(
            course_id,
            thread_id,
            comments[0].title,
            comments
        )

    def get_news_list(self,
                      course_id: int,
                      start_id: Optional[int] = None,
                      page_len: int = 10000) -> list[ManabaCourseNews]:
        """
        指定したコースのコースニュース一覧を取得します。

        Args:
            course_id: 取得するコースのコース ID
            start_id: 直近から何番目から取得するか (指定しない場合はすべて)
            page_len: 1 ページで最大何件コメント取得するか (指定しない場合は 10000 件)

        Returns:
            list[ManabaCourseNews]: コースのニュース一覧

        Notes:
            一部の項目のプロパティは None になります。詳細情報は :func:`manaba.Manaba.get_news` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        params = {
            "pagelen": page_len
        }
        if start_id is not None:
            params["start_id"] = start_id

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_news?" + urlencode(params))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        std_list = soup.find("table", {"class": "stdlist"})
        if std_list is None:
            return []

        news_tags = std_list.find_all("tr", class_=["row", "row0", "row1"])
        news = []
        for news_tag in news_tags:
            tds = news_tag.find_all("td")
            news_title_tag = tds[0]
            news_title = news_title_tag.text.strip()
            news_link = news_title_tag.find("a").get("href")
            news_id: int = int(re.sub(r"course_[0-9]+_news_([0-9]+)", r"\1", news_link))
            news_author = tds[1].text.strip()
            news_posted_at = self.process_datetime(tds[2].text.strip())

            news.append(ManabaCourseNews(
                course_id,
                news_id,
                news_title,
                news_author,
                news_posted_at,
                None,
                None,
                None
            ))

        return news

    def get_news(self,
                 course_id: int,
                 news_id: int) -> ManabaCourseNews:
        """
        指定したコース・ニュース ID のニュース詳細情報を取得します。

        Args:
            course_id: 取得するコースのコース ID
            news_id: 取得するニュースのニュース ID
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_news_" + str(news_id))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        if soup.find("h2", {"class": "msg-subject"}) is None:
            raise ManabaNotFound()

        news_title = soup.find("h2", {"class": "msg-subject"}).text.strip()

        if soup.find("div", {"class": "msg-info"}).find("a", {"href": "#"}) is not None:
            news_author = soup \
                .find("div", {"class": "msg-info"}) \
                .find("a", {"href": "#"}) \
                .text.strip()
        else:
            news_author = soup \
                .find("div", {"class": "msg-info"}) \
                .text.replace("投稿者", "").strip()

        news_posted_at = self.process_datetime(soup.find("span", {"class": "msg-date"}).text.strip())
        msg_text = soup.find("div", {"class": "msg-text"})

        news_html = str(msg_text).replace(" ", "&nbsp;").strip()

        # last_edit
        last_modified = soup.find("div", {"class": "msg-lastmod"})
        last_edited_author = None
        last_edited_at = None
        if last_modified is not None:
            if last_modified.find("a") is not None:
                last_edited_author = last_modified.find("a").text.strip()
                last_edited_at = self.process_datetime(
                    str(last_modified.find("a").next_sibling.string).strip()
                )
            else:
                # 最終更新 <a onclick="return manaba.userballoon('97279', event);" href="user_97279_profile">中山　智美</a> 2021-08-04  10:25
                last_edited_str = last_modified.text.strip()
                last_edited_author = re.sub(r"最終更新 (.+) ([0-9]{4}-[0-9]{2}-[0-9]{2} +[0-9]{2}:[0-9]{2})", r"\1",
                                            last_edited_str)
                last_edited_at = self.process_datetime(
                    re.sub(r"最終更新 (.+) ([0-9]{4}-[0-9]{2}-[0-9]{2} +[0-9]{2}:[0-9]{2})", r"\2", last_edited_str))

        manaba_course_news = ManabaCourseNews(
            course_id,
            news_id,
            news_title,
            news_author,
            news_posted_at,
            last_edited_author,
            last_edited_at,
            news_html
        )

        attachments = soup.find_all("div", {"class": "inlineattachment"})
        for attachment in attachments:
            a_tag = attachment.find("div", {"class": "inlineaf-description"}).find("a")
            manaba_course_news.add_file(ManabaFile(
                manaba_course_news,
                re.sub(r"(.+?) - ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", r"\1",
                       a_tag.text).strip(),
                self.process_datetime(
                    re.sub(r"(.+?) - ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", r"\2",
                           a_tag.text).strip()),
                urljoin(self.__base_url + "/ct/", a_tag.get("href"))
            ))

        return manaba_course_news

    def get_contents(self,
                     course_id: int) -> list[ManabaContent]:
        """
        指定したコースのコンテンツ一覧を取得します。

        Args:
            course_id: 取得するコースのコース ID

        Returns:
            list[ManabaContent]: コースのコンテンツ一覧

        Notes:
            一部の項目のプロパティは None になります。詳細情報は :func:`manaba.Manaba.get_content_pages` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_page")
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        contents_list = soup.find("table", {"class": "contentslist"})
        if contents_list is None:
            return []

        trs = contents_list.find_all("tr")
        contents = []
        for tr in trs:
            about = tr.find("td", {"class": "about-contents"})
            title = about.find("a").text.strip()
            link = about.find("a").get("href")
            content_id = re.sub(r"page_(.+)", r"\1", link)
            description = about.find("span").text.strip()

            contents.append(ManabaContent(
                course_id,
                content_id,
                title,
                description,
                None,
                None
            ))

        return contents

    def get_content_pages(self,
                          content_id: str) -> list[ManabaContentPage]:
        """
        指定したコンテンツ ID のコンテンツページ一覧を取得します。

        Args:
            content_id: 取得するコンテンツのコンテンツ ID

        Notes:
            一部の項目のプロパティは None になります。詳細情報は :func:`manaba.Manaba.get_content_page` で取得できます。
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/page_" + str(content_id)))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        if soup.find("div", {"class": "articletext"}) is None:
            raise ManabaNotFound()

        course_link = soup.find("a", {"id": "coursename"}).get("href")
        course_id: int = int(re.sub(r"course_([0-9]+)", r"\1", course_link))

        contents_list = soup.find("ul", {"class": "contentslist"}).find_all("li")
        pages = []
        for content in contents_list:
            page_title = content.text.strip()
            page_link = content.find("a").get("href")
            page_id: int = int(re.sub(r"page_[a-z0-9]+_([a-z0-9]+)", r"\1", page_link))
            pages.append(ManabaContentPage(
                course_id,
                content_id,
                page_id,
                page_title,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ))

        return pages

    def get_content_page(self,
                         content_id: str,
                         page_id: int) -> ManabaContentPage:
        """
        指定したコンテンツ ID のコンテンツページ詳細を取得します。

        Args:
            content_id: 取得するコンテンツページのコンテンツ ID
            page_id: 取得するコンテンツページのコンテンツページ ID
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        print(urljoin(self.__base_url, "/ct/page_" + str(content_id) + "_" + str(page_id)))
        self.__response = self.session.get(
            urljoin(self.__base_url, "/ct/page_" + str(content_id) + "_" + str(page_id)))
        if self.__response.status_code == 404 or self.__response.status_code == 403:
            raise ManabaNotFound()
        self.__response.raise_for_status()
        soup = BeautifulSoup(self.__response.text, "html5lib")

        if soup.find("div", {"class": "articletext"}) is None:
            raise ManabaNotFound()

        course_link = soup.find("a", {"id": "coursename"}).get("href")
        course_id: int = int(re.sub(r"course_([0-9]+)", r"\1", course_link))

        page_title = soup.find("h1", {"class": "pagetitle"}).text.strip()

        pagelimitview = soup.find("div", {"class": "pagelimitview"}).text.strip()
        publish_start_at = None
        publish_end_at = None
        if re.search(
                r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) ～ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})",
                pagelimitview) is not None:
            # 開始・終了日時両方ある
            publish_start_at = self.process_datetime(re.sub(
                r".*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) ～ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})",
                r"\1",
                pagelimitview))
            publish_end_at = self.process_datetime(re.sub(
                r".*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) ～ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})",
                r"\2",
                pagelimitview))
        elif re.search(r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) ～", pagelimitview) is not None:
            # 開始日時だけある
            publish_start_at = self.process_datetime(re.sub(
                r".*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) ～",
                r"\1",
                pagelimitview))
        elif re.search(r"～ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", pagelimitview) is not None:
            # 終了日時だけある
            publish_end_at = self.process_datetime(re.sub(
                r".*～ ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})",
                r"\1",
                pagelimitview))

        article_author = soup.find("div", {"class": "articleauthor"}).text.strip()
        last_edited_at = self.process_datetime(
            re.sub(r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}) - (.+)- ([0-9.]+)版", r"\1", article_author))
        page_author = re.sub(r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}) - (.+)- ([0-9.]+)版", r"\2",
                             article_author)
        version = re.sub(r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}) - (.+)- ([0-9.]+)版", r"\3", article_author)
        viewable = soup.find("div", {"class": "pageviewdisabled"}) is None
        html = None
        if viewable:
            article_text = soup.find("div", {"class": "articletext"})

            html = str(article_text).replace(" ", "&nbsp;").strip()

        manaba_content_page = ManabaContentPage(
            course_id,
            content_id,
            page_id,
            page_title,
            page_author,
            version,
            viewable,
            last_edited_at,
            publish_start_at,
            publish_end_at,
            html
        )

        if viewable:
            attachments = soup.find_all("div", {"class": "inlineattachment"})
            for attachment in attachments:
                a_tag = attachment.find("div", {"class": "inlineaf-description"}).find("a")
                manaba_content_page.add_file(ManabaFile(
                    manaba_content_page,
                    re.sub(r"(.+?) - ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", r"\1",
                           a_tag.text).strip(),
                    self.process_datetime(
                        re.sub(r"(.+?) - ([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})", r"\2",
                               a_tag.text).strip()),
                    urljoin(self.__base_url + "/ct/", a_tag.get("href"))
                ))

        return manaba_content_page

    def get_latest_response(self) -> Optional[Response]:
        """
        最後のレスポンスを返します。デバッグのために利用することを想定しています。

        Returns:
            Optional[Response]: レスポンス (ない場合は None)
        """
        return self.__response

    @staticmethod
    def process_datetime(datetime_str: Optional[str]) -> Optional[datetime.datetime]:
        """
        manabaの日時テキスト(YYYY-MM-DD HH:MM:SS)から datetime.datetime に変換する

        Args:
            datetime_str: manabaの日時テキスト

        Returns:
            Optional[datetime.datetime]: 変換後の datetime.datetime
        """
        if datetime_str is None or datetime_str == "":
            return None
        datetime_str = datetime_str.replace("  ", " ")
        datetime_format = "%Y-%m-%d %H:%M:%S %z" if len(datetime_str) == 19 else "%Y-%m-%d %H:%M %z"
        return datetime.datetime.strptime(datetime_str + " +0900", datetime_format).astimezone(JST)

    @staticmethod
    def _opt_value(items: dict[str, str],
                   key: str) -> Optional[str]:
        if key not in items or items[key] is None:
            return None
        return items[key].strip()

    @staticmethod
    def _parse_status(status_text: str) -> ManabaTaskStatus:
        statuses = status_text.split("\n")
        statuses = list(map(lambda x: x.strip(), statuses))
        statuses = list(filter(lambda x: len(x) != 0, statuses))
        if len(statuses) == 1:
            # 受付開始待ちなど1行しか状態がない
            task_status = get_task_status(statuses[0].strip())
            if task_status is None:
                raise ManabaInternalError(
                    "get_task_status return None (" + statuses[0].strip() + ")")
            return ManabaTaskStatus(task_status, None)

        if len(statuses) == 2:
            task_status = get_task_status(statuses[0].strip())
            if task_status is None:
                raise ManabaInternalError(
                    "get_task_status return None (" + statuses[0].strip() + ")")

            if "まだ提出は可能です" not in statuses[1]:  # 未提出 & ※遅延として取り扱われますが、まだ提出は可能です。
                your_status = get_your_status(statuses[1].strip())
                if your_status is None:
                    raise ManabaInternalError(
                        "your_status return None (" + statuses[1].strip() + ")")
            else:
                your_status = ManabaTaskYourStatusFlag.UNSUBMITTED

            return ManabaTaskStatus(task_status, your_status)

        if len(statuses) == 3:
            task_status = get_task_status(statuses[0].strip())
            if task_status is None:
                raise ManabaInternalError(
                    "get_task_status return None (" + statuses[0].strip() + ")")

            your_status = get_your_status(statuses[1].strip())
            if your_status is None:
                raise ManabaInternalError(
                    "your_status return None (" + statuses[1].strip() + ")")

            return ManabaTaskStatus(task_status, your_status)

        if len(statuses) == 4:
            task_status = get_task_status(statuses[0].strip())
            if task_status is None:
                raise ManabaInternalError(
                    "get_task_status return None (" + statuses[0].strip() + ")")

            your_status = get_your_status(statuses[2].strip())
            if your_status is None:
                raise ManabaInternalError(
                    "your_status return None (" + statuses[2].strip() + ")")

            return ManabaTaskStatus(task_status, your_status)

        raise ManabaInternalError("td_tags length not matched (" + str(len(statuses)) + ")")

    @staticmethod
    def _parse_grade_bar(gradelist: bs4.element.Tag) -> Optional[ManabaGradePosition]:
        bar_form = gradelist.find("table", {"class": "form"})
        if bar_form is None:
            return None

        bars = bar_form.find_all("td")
        if len(bars) == 1:
            below_percent = None
            my_position_percent = int(bars[0].get("width").replace("%", ""))
            above_percent = None

            return ManabaGradePosition(below_percent, my_position_percent, above_percent)

        if len(bars) == 2:
            if bars[0].get("class") is not None and "gradebar" in bars[0].get("class"):
                # 最低点
                below_percent = None
                my_position_percent = int(bars[0].get("width").replace("%", ""))
                above_percent = int(bars[1].get("width").replace("%", ""))
            elif bars[1].get("class") is not None and "gradebar" in bars[1].get("class"):
                below_percent = int(bars[0].get("width").replace("%", ""))
                my_position_percent = int(bars[1].get("width").replace("%", ""))
                above_percent = None
            else:
                raise ManabaInternalError("_parse_grade_bar not found gradebar")

            return ManabaGradePosition(below_percent, my_position_percent, above_percent)

        if len(bars) == 3:
            below_percent = int(bars[0].get("width").replace("%", ""))
            my_position_percent = int(bars[1].get("width").replace("%", ""))
            above_percent = int(bars[2].get("width").replace("%", ""))

            return ManabaGradePosition(below_percent, my_position_percent, above_percent)

        raise ManabaInternalError("_parse_grade_bar not parseable")


class ManabaNotLoggedIn(Exception):
    """
    manaba にログインしている必要があるがしていない
    """


class ManabaNotFound(Exception):
    """
    manaba のコース等ページにアクセスしたが、そのページが見つからなかった
    """


class ManabaInternalError(Exception):
    """
    処理に失敗した
    """


class ManabaContentDisabled(Exception):
    """
    コンテンツページが無効化（公開期間外などにより）されている
    """
