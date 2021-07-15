# coding: utf-8
"""
Library for get various information about manaba.

manabaのさまざまな情報を取得するためのライブラリです。
"""

from typing import Optional, Union
from urllib.parse import urljoin, parse_qs, urlparse

import bs4.element
from bs4 import BeautifulSoup
import requests


class ManabaCourseLamps:
    """
    manaba コース一覧ページに表示されるランプ管理クラス
    """
    def __init__(self, news: bool, deadline: bool, grad: bool, thread: bool, individual: bool) -> None:
        self._news = news
        self._deadline = deadline
        self._grad = grad
        self._thread = thread
        self._individual = individual

    @property
    def news(self) -> bool:
        """
        コースニュースランプ

        :return: newsランプが点いているか
        """
        return self._news

    @property
    def deadline(self) -> bool:
        """
        デッドラインランプ (課題ランプ)

        :return: デッドラインランプが点いているか
        """
        return self._deadline

    @property
    def grad(self) -> bool:
        """
        グラッドランプ (成績ランプ)

        :return: 成績ランプが点いているか
        """
        return self._grad

    @property
    def thread(self) -> bool:
        """
        スレッドランプ

        :return: スレッドランプが点いているか
        """
        return self._thread

    @property
    def individual(self) -> bool:
        """
        個人ランプ (コレクション)

        :return: 個人ランプが点いているか
        """
        return self._individual


class ManabaCourse:
    """
    manaba コース情報
    """
    def __init__(self, name: str, course_id: int, year: Optional[int], lecture_at: Optional[str],
                 teacher: Optional[str], status_lamps: ManabaCourseLamps):
        self._name = name
        self._course_id = course_id
        self._year = year
        self._lecture_at = lecture_at
        self._teacher = teacher
        self._status_lamps = status_lamps

    @property
    def name(self) -> str:
        """
        コース名

        :return: コースの名称
        """
        return self._name

    @property
    def course_id(self) -> int:
        """
        コース ID (URLの一部)
        ※コースコードではない

        :return: コース ID
        """
        return self._course_id

    @property
    def year(self) -> Optional[int]:
        """
        コースの年度

        Returns
        -------

        Notes
        -------
        コース一覧にて曜日表示を利用している場合、この項目は None になる可能性があります。

        """
        return self._year

    @property
    def lecture_at(self) -> Optional[str]:
        """
        コース年度・時限

        :return: コースの年度および時限 (取得できない場合 None)
        """
        return self._lecture_at

    @property
    def teacher(self) -> Optional[str]:
        """
        コースの担当教員名

        :return: コースの担当教員名 (取得できない場合 None)
        """
        return self._teacher

    @property
    def status_lamps(self) -> ManabaCourseLamps:
        """
        コースのステータスランプ

        :return: コースのステータスランプ
        """
        return self._status_lamps


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

        :param username: manaba ユーザー名
        :param password: manaba パスワード
        :return: ログインできたか
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

        Parameters
        ----------
        course_id : int
            取得するコースのコース ID
        """
        pass

    def get_courses(self) -> list[ManabaCourse]:
        """
        参加しているコース情報を取得する

        :return: 参加しているコース情報
        """
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        response = self.session.get(urljoin(self.__base_url, "/ct/home_course"))
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
        elif correct_list_format == "list":
            return self._get_courses_from_list(my_courses)
        elif correct_list_format == "timetable":
            return self._get_courses_from_timetable(my_courses, soup.find("table", {"class": "courselist"}))

    def _get_courses_from_thumbnail(self, my_courses: bs4.element.Tag) -> list[ManabaCourse]:
        course_cards = my_courses.find_all("div", {"class": "coursecard"})

        courses = []
        course_card: bs4.element.Tag
        for course_card in course_cards:
            title_link = course_card.find("div", {"class": "course-card-title"}).find("a")
            course_name = title_link.text
            course_id = title_link.get("href")

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
        course_rows = my_courses.find_all("tr", {"class": "courselist-c"})

        courses = []
        course_row: bs4.element.Tag
        for course_row in course_rows:
            course_name = course_row.find("span", {"class": "courselist-title"}).text
            course_id = course_row.find("span", {"class": "courselist-title"}).find("a").get("href")

            status_lamps = self._get_lamps_from_card(course_row.find("div", {"class": "course-card-status"}))
            course_tds = course_row.find_all("td")
            course_year = int(course_tds[1].text.strip()) if len(course_tds) > 1 else None
            course_time = course_tds[2].text.strip() if len(course_tds) > 2 else None
            course_teacher = course_tds[3].text.strip() if len(course_tds) > 3 else None

            courses.append(ManabaCourse(course_name, course_id, course_year, course_time, course_teacher, status_lamps))

        return courses

    def _get_courses_from_timetable(self, my_courses: bs4.element.Tag, course_list: bs4.element.Tag) -> list[ManabaCourse]:
        course_cards = my_courses.find_all("div", {"class": "courselistweekly-c"})

        courses = []
        course_row: bs4.element.Tag
        for course_card in course_cards:
            course_name = course_card.find("a").text
            course_id = course_card.find("a").get("href")

            status_lamps = self._get_lamps_from_card(course_card)

            courses.append(ManabaCourse(course_name, course_id, None, None, None, status_lamps))

        other_courses = self._get_courses_from_list(course_list)
        courses.extend(other_courses)

        return courses

    @staticmethod
    def _get_lamps_from_card(course_status: bs4.element.Tag) -> ManabaCourseLamps:
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
    pass
