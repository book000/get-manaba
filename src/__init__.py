# coding: utf-8
"""
Library for get various information about manaba.

manabaのさまざまな情報を取得するためのライブラリです。
"""
import datetime
import re
from typing import Optional, Union
from urllib.parse import parse_qs, urljoin, urlparse

import bs4.element
import requests
from bs4 import BeautifulSoup

from src.models.ManabaCourse import ManabaCourse
from src.models.ManabaCourseLamps import ManabaCourseLamps
from src.models.ManabaGradePosition import ManabaGradePosition
from src.models.ManabaPortfolioType import get_portfolio_type
from src.models.ManabaQuery import ManabaQuery
from src.models.ManabaQueryDetails import ManabaQueryDetails
from src.models.ManabaReport import ManabaReport
from src.models.ManabaResultViewType import get_result_view_type
from src.models.ManabaSurvey import ManabaSurvey
from src.models.ManabaTaskStatus import ManabaTaskStatus
from src.models.ManabaTaskStatusFlag import ManabaTaskStatusFlag, get_task_status
from src.models.ManabaTaskYourStatusFlag import ManabaTaskYourStatusFlag, get_your_status

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


class Manaba:
    """
    manaba 基本ライブラリ
    """

    def __init__(self,
                 base_url: str) -> None:
        self.session = requests.Session()
        self.__base_url = base_url
        self.__logged_in = False

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
        response = self.session.get(urljoin(self.__base_url, "/ct/login"))
        if response.status_code != 200:
            return False
        soup = BeautifulSoup(response.text, "html5lib")

        login_form_box = soup.find("div", {"id": "login-form-box"})
        session_value1 = login_form_box.find("input", {"name": "SessionValue1"}).get("value")
        session_value = login_form_box.find("input", {"name": "SessionValue"}).get("value")
        login_value = login_form_box.find("input", {"name": "login"}).get("value")

        response = self.session.post(urljoin(self.__base_url, "/ct/login"), params={
            "userid": username,
            "password": password,
            "login": login_value,
            "manaba-form": "1",
            "sessionValue1": session_value1,
            "sessionValue": session_value
        })

        self.__logged_in = response.status_code == 200

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

        response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)))
        if response.status_code == 404 or response.status_code == 403:
            raise ManabaNotFound()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html5lib")

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
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        response = self.session.get(urljoin(self.__base_url, "/ct/home_course"))
        if response.status_code == 404 or response.status_code == 403:
            raise ManabaNotFound()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html5lib")

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
            course_name = title_link.text
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
        course_row: bs4.element.Tag
        for course_row in course_rows:
            course_name = course_row.find("span", {"class": "courselist-title"}).text
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
        course_row: bs4.element.Tag
        for course_card in course_cards:
            course_name = course_card.find("a").text
            course_link = course_card.find("a").get("href")
            course_id: int = int(re.sub(r"course_([0-9]+)", r"\1", course_link))

            status_lamps = self._get_lamps_from_card(course_card)

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
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_query")
        if response.status_code == 404 or response.status_code == 403:
            raise ManabaNotFound()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html5lib")
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

            query_start_time = self._process_datetime(query_td_tags[2].text.strip())
            query_end_time = self._process_datetime(query_td_tags[3].text.strip())

            querys.append(ManabaQuery(
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

        response = self.session.get(
            urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_query_" + str(query_id))
        if response.status_code == 404 or response.status_code == 403:
            raise ManabaNotFound()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html5lib")

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
            query_id,
            query_title,
            self._opt_value(details, "課題に関する説明"),
            self._process_datetime(self._opt_value(details, "受付開始日時")),
            self._process_datetime(self._opt_value(details, "受付終了日時")),
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
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_survey")
        if response.status_code == 404 or response.status_code == 403:
            raise ManabaNotFound()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html5lib")
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

            survey_start_time = self._process_datetime(survey_td_tags[2].text.strip())
            survey_end_time = self._process_datetime(survey_td_tags[3].text.strip())

            surveys.append(ManabaSurvey(
                survey_id,
                survey_title,
                survey_status,
                survey_status_lamp,
                survey_start_time,
                survey_end_time
            ))

        return surveys

    def get_reports(self,
                    course_id: int) -> list[ManabaReport]:
        """
        指定したコースのレポート一覧を取得します。

        Args:
            course_id: 取得するコースのコース ID

        Returns:
            list[ManabaReport]: コースのレポート一覧
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        response = self.session.get(urljoin(self.__base_url, "/ct/course_" + str(course_id)) + "_report")
        if response.status_code == 404 or response.status_code == 403:
            raise ManabaNotFound()
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html5lib")
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

            report_start_time = self._process_datetime(report_td_tags[2].text.strip())
            report_end_time = self._process_datetime(report_td_tags[3].text.strip())

            reports.append(ManabaReport(
                report_id,
                report_title,
                report_status,
                report_status_lamp,
                report_start_time,
                report_end_time
            ))

        return reports

    @staticmethod
    def _process_datetime(datetime_str: Optional[str]) -> Optional[datetime.datetime]:
        if datetime_str is None or datetime_str == "":
            return None
        datetime_format = "%Y-%m-%d %H:%M:%S %z" if len(datetime_str) == 19 else "%Y-%m-%d %H:%M %z"
        return datetime.datetime.strptime(datetime_str + " +0900", datetime_format).astimezone(JST)

    @staticmethod
    def _opt_value(items: dict[str, str],
                   key: str) -> Optional[str]:
        if key not in items or items[key] is None:
            return None
        return items[key]

    @staticmethod
    def _parse_status(status_text: str) -> ManabaTaskStatus:
        if len(status_text.split("\n")) == 1:
            # 受付開始待ちなど1行しか状態がない
            task_status = get_task_status(status_text.split("\n")[0].strip())
            if task_status is None:
                raise ManabaInternalError(
                    "get_task_status return None (" + status_text.split("\n")[0].strip() + ")")
            return ManabaTaskStatus(task_status, None)

        if len(status_text.split("\n")) == 2:
            task_status = get_task_status(status_text.split("\n")[0].strip())
            if task_status is None:
                raise ManabaInternalError(
                    "get_task_status return None (" + status_text.split("\n")[0].strip() + ")")

            your_status = get_your_status(status_text.split("\n")[1].strip())
            if your_status is None:
                raise ManabaInternalError(
                    "your_status return None (" + status_text.split("\n")[1].strip() + ")")

            return ManabaTaskStatus(task_status, your_status)

        raise ManabaInternalError("td_tags length not matched (" + str(len(status_text.split("\n"))) + ")")

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
