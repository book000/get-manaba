# coding: utf-8
import requests
import re
from bs4 import BeautifulSoup
from requests.compat import urljoin


class manaba:
    base_url = None
    session = None

    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username: str, password: str):
        """
        Login to manaba
        :param username: manaba username
        :param password: manaba password
        :return: None
        """

        self.session = requests.Session()
        response = self.session.get(urljoin(self.base_url, "/ct/login"))
        soup = BeautifulSoup(response.text, "html.parser")

        sessionValue1 = soup.find("div", {"id": "login-form-box"}).find("input", {"name": "SessionValue1"}).get("value")
        sessionValue = soup.find("div", {"id": "login-form-box"}).find("input", {"name": "SessionValue"}).get("value")
        loginValue = soup.find("div", {"id": "login-form-box"}).find("input", {"name": "login"}).get("value")

        response = self.session.post(urljoin(self.base_url, "/ct/login"), params={
            "userid": username,
            "password": password,
            "login": loginValue,
            "manaba-form": "1",
            "sessionValue1": sessionValue1,
            "sessionValue": sessionValue
        })
        if response.status_code != 200:
            exit(1)

    def getCourses(self) -> list:
        """
        Return list of courses you are attending
        :return: List of course
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        response = self.session.get(urljoin(self.base_url, "/ct/home"))
        soup = BeautifulSoup(response.text, "html.parser")
        before_course_view = soup.find("ul", {"class": "infolist-tab"}).find("li", {"class": "current"}).find("a").get(
            "href")

        response = self.session.get(urljoin(self.base_url, "/ct/home?chglistformat=list"))
        soup = BeautifulSoup(response.text, "html.parser")
        course_list = soup.find("table", {"class": "courselist"}).findAll("tr", {"class": "courselist-c"})

        courses = []
        for course in course_list:
            course_title = course.find("span", {"class": "courselist-title"}).text.strip()
            course_id = course.find("span", {"class": "courselist-title"}).find("a").get("href")

            course_status_tags = course.find("div", {"class": "course-card-status"}).findAll("img")
            course_status = {
                "news": course_status_tags[0].get("src").endswith("on.png"),
                "task": course_status_tags[1].get("src").endswith("on.png"),
                "grad": course_status_tags[2].get("src").endswith("on.png"),
                "thread": course_status_tags[3].get("src").endswith("on.png"),
                "individual": course_status_tags[4].get("src").endswith("on.png")
            }

            course_td_tags = course.findAll("td")
            course_year = course_td_tags[1].text.strip()
            course_time = course_td_tags[2].text.strip()
            course_teacher = course_td_tags[3].text.strip()

            courses.append({
                "title": course_title,
                "id": course_id,
                "status": course_status,
                "year": course_year,
                "time": course_time,
                "teacher": course_teacher
            })

        self.session.get(urljoin(self.base_url, "/ct/" + before_course_view))
        return courses

    def getCourseQuerys(self, course_id) -> list:
        """
        Return list of course query (mini test)
        :param course_id: Course Id (ex. course_000000)
        :return: List of course query
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+", course_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + course_id + "_query"))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("table", {"class": "stdlist"}) is None:
            return []

        query_tags = soup.find("table", {"class": "stdlist"}).findAll("tr", class_=["row0", "row1"])
        querys = []
        for query_tag in query_tags:
            query_td_tags = query_tag.findAll("td")
            query_title = query_tag.find("h3").text.strip()
            query_status_lamp = query_tag.find("h3").find("img").get("src").endswith("on.png")
            query_id = query_tag.find("h3").find("a").get("href")

            query_status = query_td_tags[1].text.strip().split("\n")[0].strip()
            query_your_status = query_td_tags[1].text.strip().split("\n")[1].strip()
            query_start_time = query_td_tags[2].text.strip()
            query_end_time = query_td_tags[3].text.strip()

            querys.append({
                "title": query_title,
                "id": query_id,
                "status": query_status,
                "status_lamp": query_status_lamp,
                "your_status": query_your_status,
                "start_time": query_start_time,
                "end_time": query_end_time
            })

        return querys

    def getCourseSurveys(self, course_id) -> list:
        """
        Return list of course survey
        :param course_id: Course Id (ex. course_000000)
        :return: List of course survey
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+", course_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + course_id + "_survey"))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("table", {"class": "stdlist"}) is None:
            return []

        survey_tags = soup.find("table", {"class": "stdlist"}).findAll("tr", class_=["row0", "row1"])
        surveys = []
        for survey_tag in survey_tags:
            survey_td_tags = survey_tag.findAll("td")
            survey_title = survey_tag.find("h3").text.strip()
            survey_status_lamp = survey_tag.find("h3").find("img").get("src").endswith("on.png")
            survey_id = survey_tag.find("h3").find("a").get("href")

            survey_status = survey_td_tags[1].text.strip().split("\n")[0].strip()
            survey_your_status = survey_td_tags[1].text.strip().split("\n")[1].strip()
            survey_start_time = survey_td_tags[2].text.strip()
            survey_end_time = survey_td_tags[3].text.strip()

            surveys.append({
                "title": survey_title,
                "id": survey_id,
                "status": survey_status,
                "status_lamp": survey_status_lamp,
                "your_status": survey_your_status,
                "start_time": survey_start_time,
                "end_time": survey_end_time
            })

        return surveys

    def getCourseReports(self, course_id) -> list:
        """
        Return list of course report
        :param course_id: Course Id (ex. course_000000)
        :return: List of course report
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+", course_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + course_id + "_report"))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("table", {"class": "stdlist"}) is None:
            return []

        report_tags = soup.find("table", {"class": "stdlist"}).findAll("tr", class_=["row0", "row1"])
        reports = []
        for report_tag in report_tags:
            report_td_tags = report_tag.findAll("td")
            report_title = report_tag.find("h3").text.strip()
            report_status_lamp = report_tag.find("h3").find("img").get("src").endswith("on.png")
            report_id = report_tag.find("h3").find("a").get("href")

            report_status = report_td_tags[1].text.strip().split("\n")[0].strip()
            report_your_status = report_td_tags[1].text.strip().split("\n")[1].strip()
            report_start_time = report_td_tags[2].text.strip()
            report_end_time = report_td_tags[3].text.strip()

            reports.append({
                "title": report_title,
                "id": report_id,
                "status": report_status,
                "status_lamp": report_status_lamp,
                "your_status": report_your_status,
                "start_time": report_start_time,
                "end_time": report_end_time
            })

        return reports

    def getCourseProjects(self, course_id) -> list:
        """
        Return list of course project
        :param course_id: Course Id (ex. course_000000)
        :return: List of course project
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+", course_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + course_id + "_project"))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("table", {"class": "stdlist"}) is None:
            return []

        project_tags = soup.find("table", {"class": "stdlist"}).findAll("tr", class_=["row0", "row1"])
        projects = []
        for project_tag in project_tags:
            project_td_tags = project_tag.findAll("td")
            project_title = project_tag.find("h3").text.strip()
            project_id = project_tag.find("h3").find("a").get("href")

            project_method = project_td_tags[1].text.strip()
            project_status = project_td_tags[2].text.strip().split("\n")[0].strip()
            project_your_status = project_td_tags[2].text.strip().split("\n")[1].strip()
            project_start_time = project_td_tags[3].text.strip()
            project_end_time = project_td_tags[4].text.strip()
            project_team_count = project_td_tags[5].text.strip()

            projects.append({
                "title": project_title,
                "id": project_id,
                "method": project_method,
                "status": project_status,
                "your_status": project_your_status,
                "start_time": project_start_time,
                "end_time": project_end_time,
                "team_count": project_team_count
            })

        return projects

    def getCourseNews(self, course_id) -> list:
        """
        Return list of course news
        :param course_id: Course Id (ex. course_000000)
        :return: List of course news
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+", course_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + course_id + "_news"))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("table", {"class": "stdlist"}) is None:
            return []

        news_tags = soup.find("table", {"class": "stdlist"}).findAll("tr", class_=["row0", "row1"])
        news_list = []
        for news_tag in news_tags:
            news_td_tags = news_tag.findAll("td")
            news_title = news_td_tags[0].text.strip()
            news_id = news_td_tags[0].find("a").get("href")
            news_author = news_td_tags[1].text.strip()
            news_date = news_td_tags[2].text.strip()

            news_list.append({
                "title": news_title,
                "id": news_id,
                "author": news_author,
                "date": news_date
            })

        return news_list

    def getCourseNewsDetails(self, news_id) -> dict:
        """
        Return details of news
        :param news_id: News Id (ex. course_000000_news_000000)
        :return: Details of News
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+_news_[0-9]+", news_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + news_id))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        news_title = soup.find("h2", {"class": "msg-subject"}).text.strip()
        news_date = soup.find("span", {"class": "msg-date"}).text.strip()
        news_author = soup.find("div", {"class": "msg-info"}).text.replace("投稿者", "").strip()
        news_text = soup.find("div", {"class": "msg-text"}).text.strip()
        news_html = str(soup.find("div", {"class": "msg-text"}))

        return {
            "title": news_title,
            "date": news_date,
            "author": news_author,
            "text": news_text,
            "html": news_html
        }

    def getCourseThreads(self, course_id) -> list:
        """
        Return list of course thread
        :param course_id: Course Id (ex. course_000000)
        :return: List of course thread
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+", course_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + course_id + "_topics"))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html5lib")  # Because the HTML is corrupted

        if soup.find("table", {"class": "stdlist"}) is None:
            return []

        thread_tags = soup.find("table", {"class": "stdlist"}).findAll("tr", class_=["row", "row1"])
        threads = []
        for thread_tag in thread_tags:
            thread_td_tags = thread_tag.findAll("td")
            thread_title = thread_tag.find("span", {"class": "thread-title"}).text.strip()
            thread_id = thread_tag.find("span", {"class": "thread-title"}).find("a").get("href")

            thread_unread = thread_tag.find("td", {"class": "tunread"}).text.strip()
            thread_comment_count = thread_td_tags[2].text.strip()
            thread_lastedit_date = thread_td_tags[3].text.strip()

            threads.append({
                "title": thread_title,
                "id": thread_id,
                "unread": thread_unread,
                "comment_count": thread_comment_count,
                "lastedit_date": thread_lastedit_date
            })

        return threads

    def getCourseThreadDetails(self, thread_id) -> dict:
        """
        Return details of thread
        :param thread_id: Thread Id (ex. course_000000_topics_00_tflat)
        :return: Details of thread
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+_topics_[0-9]+_tflat", thread_id):
            raise ValueError("Invalid thread_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + thread_id))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for i in soup.select("br"):
            i.replace_with("\n")

        thread_tags = soup.findAll("div", {"class": "thread"})

        thread_title = thread_tags[0].find("div", {"class": "articlesubject"}).text.strip()
        thread_text = thread_tags[0].find("div", {"class": "articlebody-msgbody"}).text.strip()
        thread_html = str(thread_tags[0].find("div", {"class": "articlebody-msgbody"}))
        thread_author = str(thread_tags[0].find("span", {"class": "posted-time"}).previous_sibling.string).strip()
        thread_date = thread_tags[0].find("span", {"class": "posted-time"}).text.strip()

        # comments
        comments = []

        comment_tags = thread_tags[1].findAll("div", {"class": "articlecontainer"})
        for comment_tag in comment_tags:
            comment_num = comment_tag.find("h3", {"class": "articlenumber"}).text.strip()
            comment_title = comment_tag.find("div", {"class": "articlesubject"}).text.strip()
            comment_text = comment_tag.find("div", {"class": "articlebody-msgbody"}).text.strip()

            comment_author = None
            comment_date = None
            if comment_tag.find("span", {"class": "posted-time"}) is not None:
                comment_author = str(comment_tag.find("span", {"class": "posted-time"}).previous_sibling.string).strip()
                comment_date = comment_tag.find("span", {"class": "posted-time"}).text.strip()

            comments.append({
                "num": comment_num,
                "title": comment_title,
                "comment_text": comment_text,
                "author": comment_author,
                "date": comment_date
            })

        return {
            "title": thread_title,
            "date": thread_date,
            "author": thread_author,
            "text": thread_text,
            "html": thread_html,
            "comments": comments
        }

    def getCourseContents(self, course_id) -> list:
        """
        Return list of course contents
        :param course_id: Course Id (ex. course_000000)
        :return: List of course contents
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"course_[0-9]+", course_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + course_id + "_page"))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("table", {"class": "contentslist"}) is None:
            return []

        contents_tags = soup.find("table", {"class": "contentslist"}).findAll("tr", recursive=False)
        contents = []
        for contents_tag in contents_tags:
            contents_title = contents_tag.find("td", {"class": "about-contents"}).text.strip()
            contents_id = contents_tag.find("td", {"class": "about-contents"}).find("a").get("href")
            contents_page_count = contents_tag.find("td", {"class": "info-contents"}).text.strip().split("\n")[
                0].strip()
            contents_date = contents_tag.find("td", {"class": "info-contents"}).text.strip().split("\n")[1].strip()

            contents.append({
                "title": contents_title,
                "id": contents_id,
                "page_count": contents_page_count,
                "date": contents_date
            })

        return contents

    def getCourseContentsDetails(self, contents_id) -> dict:
        """
        Return details of Course contents texts
        :param contents_id: Content Id (ex. page_XXXXXXXXXXXXX)
        :return: Details of ourse contents texts
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"page_[a-z0-9]+", contents_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + contents_id))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        contents_title = soup.find("h1", {"class": "contents"}).text.strip()
        contents_modtime = soup.find("div", {"class": "contents-modtime"}).text
        contents_modtime = contents_modtime[contents_modtime.find(":")+1:].strip()

        if soup.find("ul", {"class": "contentslist"}) is None:
            return {
                "title": contents_title,
                "modified": contents_modtime,
                "texts": []
            }

        contents_tags = soup.find("ul", {"class": "contentslist"}).findAll("li", recursive=False)
        texts = []
        for contents_tag in contents_tags:
            contents_title = contents_tag.text.strip()
            contents_id = contents_tag.find("a").get("href")

            texts.append({
                "title": contents_title,
                "id": contents_id
            })

        return {
            "title": contents_title,
            "modified": contents_modtime,
            "texts": texts
        }

    def getCourseContentsText(self, text_id):
        """
        Return details of course contents text
        :param text_id: Content Text Id (ex. page_XXXXXXXXXXXXX_000000000)
        :return: Details of contents text
        """

        if self.session is None:
            raise RuntimeError("Login is required for this operation.")
        if not re.match(r"page_[a-z0-9]+_[0-9]+", text_id):
            raise ValueError("Invalid course_id")

        response = self.session.get(urljoin(self.base_url, "/ct/" + text_id))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        text_title = soup.find("div", {"class": "articlebody"}).find("h1", {"class": "pagetitle"}).text.strip()
        text_text = soup.find("div", {"class": "articlebody"}).find("div", {"class": "articletext"}).text.strip()
        text_html = str(soup.find("div", {"class": "articlebody"}).find("div", {"class": "articletext"}))
        author_tags = soup.findAll("div", {"class": "articleauthor"})
        for author_tag in author_tags:
            if "- " not in author_tag.text:
                continue
            text_date = author_tag.text.split("- ")[0].strip()
            text_author = author_tag.text.split("- ")[1].strip()
            text_version = author_tag.text.split("- ")[2].strip()

        text_files = soup.find("div", {"class": "articlebody"}).findAll("div", {"class": "inlineattachment"})
        files = []
        for text_file in text_files:
            file_date = None
            if len(text_file.text.split(" - ")) == 2:
                file_date = text_file.text.split(" - ")[1].strip()
            files.append({
                "filename": text_file.text.split(" - ")[0].strip(),
                "date": file_date,
                "link": text_file.find("a").get("href")
            })

        return {
            "title": text_title,
            "text": text_text,
            "html": text_html,
            "date": text_date,
            "author": text_author,
            "version": text_version,
            "files": files
        }

