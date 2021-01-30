# coding: utf-8
import os
import json
import time

from urllib.parse import urlparse
from src import manaba
from pprint import pprint

# Crawl the news thread content and download new items.
# config.json:
#   base_url (ex. *****.ac.jp)
#   username
#   password


if __name__ == "__main__":
    if not os.path.exists("config.json"):
        print("[ERROR] config.json not found.")
        exit(1)

    with open("config.json", "r") as f:
        config = json.load(f)

    manaba = manaba(config["base_url"])
    manaba.login(config["username"], config["password"])

    if not os.path.exists("data"):
        os.mkdir("data")

    courses = manaba.getCourses()
    with open(os.path.join("data", "courses.json"), "w") as f:
        f.write(json.dumps(courses))
    pprint(courses)

    for course in courses:
        print("[INFO] Title: %s %s" % (course["title"], course["time"]))
        course_id = course["id"]

        if not os.path.exists(os.path.join("data", course_id)):
            os.mkdir(os.path.join("data", course_id))

        with open(os.path.join("data", course_id, "details.json"), "w") as f:
            f.write(json.dumps(course))

        if not os.path.exists(os.path.join("data", course_id, "news")):
            os.mkdir(os.path.join("data", course_id, "news"))

        if not os.path.exists(os.path.join("data", course_id, "threads")):
            os.mkdir(os.path.join("data", course_id, "threads"))

        if not os.path.exists(os.path.join("data", course_id, "contents")):
            os.mkdir(os.path.join("data", course_id, "contents"))

        news_list = manaba.getCourseNews(course_id)
        for news in news_list:
            news_title = news["title"]
            news_id = news["id"]
            print("[INFO] %s | News: %s (%s)" % (course["title"], news_title, news_id))

            if os.path.exists(os.path.join("data", course_id, "news", news_id + ".json")):
                continue

            news_detail = manaba.getCourseNewsDetails(news_id)

            with open(os.path.join("data", course_id, "news", news_id + ".json"), "w") as f:
                f.write(json.dumps(news_detail))
            time.sleep(1)

        threads = manaba.getCourseThreads(course_id)
        for thread in threads:
            thread_title = thread["title"]
            thread_id = thread["id"]
            print("[INFO] %s | Thread: %s (%s)" % (course["title"], thread_title, thread_id))

            thread_detail = manaba.getCourseThreadDetails(thread_id)

            if not os.path.exists(os.path.join("data", course_id, "threads", thread_id)):
                os.mkdir(os.path.join("data", course_id, "threads", thread_id))

            with open(os.path.join("data", course_id, "threads", thread_id, "details.json"), "w") as f:
                f.write(json.dumps(thread_detail))

            for comment in thread_detail["comments"]:
                comment_num = comment["num"]
                if os.path.exists(os.path.join("data", course_id, "threads", thread_id, comment_num + ".json")):
                    continue

                with open(os.path.join("data", course_id, "threads", thread_id, comment_num + ".json"), "w") as f:
                    f.write(json.dumps(comment))

            time.sleep(1)

        contents = manaba.getCourseContents(course_id)
        for content in contents:
            content_title = content["title"]
            content_id = content["id"]
            print("[INFO] %s | Contents: %s (%s)" % (course["title"], content_title, content_id))

            if not os.path.exists(os.path.join("data", course_id, "contents", content_id)):
                os.mkdir(os.path.join("data", course_id, "contents", content_id))

            content_detail = manaba.getCourseContentsDetails(content_id)

            with open(os.path.join("data", course_id, "contents", content_id, "details.json"), "w") as f:
                f.write(json.dumps(content_detail))

            for text in content_detail["texts"]:
                text_title = text["title"]
                text_id = text["id"]
                print("[INFO] %s | Contents: %s | Text: %s (%s)" % (course["title"], content_title, text_title, text_id))

                text_detail = manaba.getCourseContentsText(text_id)

                text_version = text_detail["version"]
                if not os.path.exists(os.path.join("data", course_id, "contents", content_id, text_id)):
                    os.mkdir(os.path.join("data", course_id, "contents", content_id, text_id))

                if os.path.exists(os.path.join("data", course_id, "contents", content_id, text_id, text_version + ".json")):
                    continue

                with open(os.path.join("data", course_id, "contents", content_id, text_id, text_version + ".json"), "w") as f:
                    f.write(json.dumps(text_detail))

                time.sleep(1)

                for file in text_detail["files"]:
                    filename = file["filename"]
                    file_link = file["link"]
                    file_url = config["base_url"] + "/ct/" + file_link
                    file_ext = os.path.splitext(urlparse(file_url).path)
                    if "/" in file_link:
                        file_id = file_link[:file_link.find("/")]
                    else:
                        file_id = urlparse(file_url).path[urlparse(file_url).path.rfind("/") + 1:]

                    if not os.path.exists(os.path.join("data", course_id, "contents", content_id, text_id, "attachments")):
                        os.mkdir(os.path.join("data", course_id, "contents", content_id, text_id, "attachments"))

                    if os.path.exists(os.path.join("data", course_id, "contents", content_id, text_id, "attachments", file_id + file_ext[1])):
                        continue

                    response = manaba.session.get(file_url)
                    with open(os.path.join("data", course_id, "contents", content_id, text_id, "attachments", file_id + file_ext[1]), "wb") as f:
                        f.write(response.content)

                    time.sleep(1)
