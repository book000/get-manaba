# coding: utf-8
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


class Manaba:
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url

    def login(self, username, password) -> bool:
        """
        Login to manaba

        :param username: manaba UserName
        :param password: manaba Password
        :return: Whether it was successful
        """

        response = self.session.get(urljoin(self.base_url, "/ct/login"))
        soup = BeautifulSoup(response.text, "html.parser")

        login_form_box = soup.find("div", {"id": "login-form-box"})
        sessionValue1 = login_form_box.find("input", {"name": "SessionValue1"}).get("value")
        sessionValue = login_form_box.find("input", {"name": "SessionValue"}).get("value")
        loginValue = login_form_box.find("input", {"name": "login"}).get("value")

        response = self.session.post(urljoin(self.base_url, "/ct/login"), params={
            "userid": username,
            "password": password,
            "login": loginValue,
            "manaba-form": "1",
            "sessionValue1": sessionValue1,
            "sessionValue": sessionValue
        })

        return response.status_code == 200
