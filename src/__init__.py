# coding: utf-8
"""
Library for get various information about manaba.

manabaのさまざまな情報を取得するためのライブラリです。
"""
import datetime
import re
from enum import Enum, auto
from typing import Optional, ValuesView
from urllib.parse import parse_qs, urljoin, urlparse

import bs4.element
import requests
from bs4 import BeautifulSoup

from src.models.ManabaCourse import ManabaCourse
from src.models.ManabaCourseLamps import ManabaCourseLamps
from src.models.ManabaQuery import ManabaQuery
from src.models.ManabaTaskStatus import ManabaTaskStatus
from src.models.ManabaTaskStatusFlag import ManabaTaskStatusFlag, get_task_status
from src.models.ManabaTaskYourStatusFlag import get_your_status

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


class Manaba:
    """
    manaba 基本ライブラリ
    """

    def __init__(self, base_url: str) -> None:
        self.session = requests.Session()
        self.__base_url = base_url
        self.__logged_in = False

    def login(self, username: str, password: str) -> bool:
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

    def get_course(self, course_id: int) -> ManabaCourse:
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

    def _get_courses_from_thumbnail(self, my_courses: bs4.element.Tag) -> list[ManabaCourse]:
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

    def _get_courses_from_list(self, my_courses: bs4.element.Tag) -> list[ManabaCourse]:
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

    def _get_courses_from_timetable(self, my_courses: bs4.element.Tag, course_list: bs4.element.Tag) \
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

    def get_query(self, course_id: int) -> list[ManabaQuery]:
        """
        指定したコースの小テストを取得します。

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

        query_tags = std_list.find_all("tr", class_=["row0", "row1"])
        querys = []
        for query_tag in query_tags:
            query_td_tags = query_tag.findAll("td")
            query_title = query_tag.find("h3").text.strip()
            query_status_lamp = query_tag.find("h3").find("img").get("src").endswith("on.png")
            query_id = query_tag.find("h3").find("a").get("href")

            if len(query_td_tags[1].text.strip().split("\n")) == 1:
                # 受付開始待ちなど1行しか状態がない
                task_status = get_task_status(query_td_tags[1].text.strip().split("\n")[0])
                if task_status is None:
                    raise ManabaInternalError(
                        "get_task_status return None (" + query_td_tags[1].text.strip().split("\n")[0] + ")")
                query_status = ManabaTaskStatus(task_status, None)
            elif len(query_td_tags[1].text.strip().split("\n")) == 2:
                task_status = get_task_status(query_td_tags[1].text.strip().split("\n")[0])
                if task_status is None:
                    raise ManabaInternalError(
                        "get_task_status return None (" + query_td_tags[1].text.strip().split("\n")[0] + ")")

                your_status = get_your_status(query_td_tags[1].text.strip().split("\n")[1])
                if your_status is None:
                    raise ManabaInternalError(
                        "your_status return None (" + query_td_tags[1].text.strip().split("\n")[1] + ")")

                query_status = ManabaTaskStatus(task_status, your_status)
            else:
                raise ManabaInternalError("query_td_tags length not matched")

            query_start_time = None if query_td_tags[2].text.strip() == "" else \
                datetime.datetime.strptime(query_td_tags[2].text.strip() + " +0900", "%Y-%m-%d %H:%M %z").astimezone(
                    JST)
            query_end_time = None if query_td_tags[3].text.strip() == "" else \
                datetime.datetime.strptime(query_td_tags[3].text.strip() + " +0900", "%Y-%m-%d %H:%M %z").astimezone(
                    JST)

            querys.append(ManabaQuery(
                query_title,
                query_status,
                query_status_lamp,
                query_start_time,
                query_end_time
            ))

        return querys

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
