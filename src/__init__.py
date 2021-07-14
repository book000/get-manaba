# coding: utf-8
"""
Library for get various information about manaba.

manabaのさまざまな情報を取得するためのライブラリです。
"""

from typing import Union
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
    def __init__(self, name: str, course_id: int, lecture_at: Union[str, None], teacher: Union[str, None], status_lamps: ManabaCourseLamps):
        self._name = name
        self._course_id = course_id
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
    def lecture_at(self) -> Union[str, None]:
        """
        コース年度・時限

        :return: コースの年度および時限 (取得できない場合 None)
        """
        return self._lecture_at

    @property
    def teacher(self) -> Union[str, None]:
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
        soup = BeautifulSoup(response.text, "html.parser")

        login_form_box = soup.find("div", {"id": "login-form-box"})
        sessionValue1 = login_form_box.find("input", {"name": "SessionValue1"}).get("value")
        sessionValue = login_form_box.find("input", {"name": "SessionValue"}).get("value")
        loginValue = login_form_box.find("input", {"name": "login"}).get("value")

        response = self.session.post(urljoin(self.__base_url, "/ct/login"), params={
            "userid": username,
            "password": password,
            "login": loginValue,
            "manaba-form": "1",
            "sessionValue1": sessionValue1,
            "sessionValue": sessionValue
        })

        self.__logged_in = response.status_code == 200

        return self.__logged_in

    def get_courses(self) -> list[ManabaCourse]:
        """
        参加しているコース情報を取得する

        :return: 参加しているコース情報
        """
        print(self.__logged_in)
        if not self.__logged_in:
            raise ManabaNotLoggedIn()

        response = self.session.get(urljoin(self.__base_url, "/ct/home_course"))
        soup = BeautifulSoup(response.text, "html.parser")

        correct_list_format_href: str = soup \
            .find("ul", {"class": "infolist-tab"}) \
            .find("li", {"class": "current"}) \
            .find("a") \
            .get("href")
        correct_list_format = parse_qs(urlparse(correct_list_format_href).query)["chglistformat"][0]

        mycourses = soup.find("div", {"class": "mycourses-body"})

        if correct_list_format == "thumbnail":
            return self._get_courses_from_thumbnail(mycourses)
        elif correct_list_format == "list":
            return self._get_courses_from_list(mycourses)
        elif correct_list_format == "timetable":
            return self._get_courses_from_timetable(mycourses)

    @staticmethod
    def _get_courses_from_thumbnail(mycourses: bs4.element.Tag) -> list[ManabaCourse]:
        course_cards = mycourses.find_all("div", {"class": "coursecard"})

        courses = []
        course_card: bs4.element.Tag
        for course_card in course_cards:
            title_link = course_card.find("div", {"class": "course-card-title"}).find("a")
            course_name = title_link.text
            course_id = title_link.get("href")

            courseitems: bs4.element.Tag = course_card.find("dl", {"class": "courseitems"})
            dts = courseitems.find_all("dt", {"class": "courseitemtext"}, recursive=False)
            dds = courseitems.find_all("dd", {"class": "courseitemdetail"}, recursive=False)

            lecture_at: Union[str, None] = None
            teacher: Union[str, None] = None

            dt: bs4.element.Tag
            dd: bs4.element.Tag
            for dt, dd in zip(dts, dds):
                dt_text = dt.text.strip()
                dd_text = dt.text.strip()

                if dt_text == "時限":
                    lecture_at = dd_text
                elif dt_text == "担当":
                    teacher = dd_text

            card_statuses = course_card \
                .find("div", {"class": "course-card-status"}) \
                .find_all("img")

            status_lamps = ManabaCourseLamps(
                card_statuses[0].get("src").endswith("on.png"),
                card_statuses[1].get("src").endswith("on.png"),
                card_statuses[2].get("src").endswith("on.png"),
                card_statuses[3].get("src").endswith("on.png"),
                card_statuses[4].get("src").endswith("on.png")
            )

            courses.append(ManabaCourse(course_name, course_id, lecture_at, teacher, status_lamps))

        return courses

    def _get_courses_from_list(self, mycourses: bs4.element.Tag) -> list[ManabaCourse]:
        pass

    def _get_courses_from_timetable(self, mycourses: bs4.element.Tag) -> list[ManabaCourse]:
        pass


class ManabaNotLoggedIn(Exception):
    pass
