# coding: utf-8
import os
import json
import time
import requests

from src import manaba
from pprint import pprint


# Notify Discord when there are new tasks (mini test, surveys, reports).
# config.json:
#   base_url (ex. *****.ac.jp)
#   username
#   password
#   discord_token
#   discord_channel


def sendMessage(channelId: str, message: str = "", embed: dict = None):
    if not os.path.exists("config.json"):
        print("config.json not found.")
        exit(1)

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    print("[INFO] sendMessage: {message}".format(message=message))
    print("[INFO] sendMessage: {embed}".format(embed=embed))
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bot {token}".format(token=config["discord_token"]),
        "User-Agent": "Bot"
    }
    params = {
        "content": message,
        "embed": embed
    }
    response = requests.post(
        "https://discord.com/api/channels/{channelId}/messages".format(channelId=channelId), headers=headers,
        json=params)
    print("[INFO] response: {code}".format(code=response.status_code))
    print("[INFO] response: {message}".format(message=response.text))


if __name__ == "__main__":
    if not os.path.exists("config.json"):
        print("[ERROR] config.json not found.")
        exit(1)

    with open("config.json", "r") as f:
        config = json.load(f)

    manaba = manaba(config["base_url"])
    manaba.login(config["username"], config["password"])

    readed = []
    init = True
    if os.path.exists("readed.json"):
        print("[INFO] Usual mode")
        init = False
        with open("readed.json", "r", encoding="utf-8") as f:
            readed = json.load(f)
    else:
        print("[INFO] Initialize mode")

    courses = manaba.getCourses()
    pprint(courses)

    for course in courses:
        print("[INFO] Title: %s %s" % (course["title"], course["time"]))
        course_id = course["id"]

        if not course["status"]["task"]:
            continue

        querys = manaba.getCourseQuerys(course_id)

        for query in querys:
            query_id = query["id"]
            if query_id in readed:
                continue

            query_title = query["title"]
            query_status = query["status"]
            query_status_lamp = query["status_lamp"]
            query_your_status = query["your_status"]
            query_start_time = query["start_time"]
            query_end_time = query["end_time"]

            if query_start_time == "":
                query_start_time = "未指定"
            if query_end_time == "":
                query_end_time = "未指定"

            if not query_status_lamp:
                continue

            readed.append(query_id)
            if init:
                continue

            embed = {
                "title": "[MINITEST] " + query_title,
                "type": "rich",
                "url": config["base_url"] + "/ct/" + query_id,
                "fields": [
                    {
                        "name": "Status",
                        "value": query_status
                    },
                    {
                        "name": "Your Status",
                        "value": query_your_status,
                        "inline": False
                    },
                    {
                        "name": "Start Time",
                        "value": query_start_time
                    },
                    {
                        "name": "End Time",
                        "value": query_end_time
                    }
                ]
            }
            sendMessage(config["discord_channel"], "", embed)

        time.sleep(1)

        surveys = manaba.getCourseSurveys(course_id)

        for survey in surveys:
            survey_id = survey["id"]
            if survey_id in readed:
                continue

            survey_title = survey["title"]
            survey_status = survey["status"]
            survey_status_lamp = survey["status_lamp"]
            survey_your_status = survey["your_status"]
            survey_start_time = survey["start_time"]
            survey_end_time = survey["end_time"]

            if not survey_status_lamp:
                continue

            readed.append(survey_id)
            if init:
                continue

            embed = {
                "title": "[SURVEY] " + survey_title,
                "type": "rich",
                "url": config["base_url"] + "/ct/" + survey_id,
                "fields": [
                    {
                        "name": "Status",
                        "value": survey_status
                    },
                    {
                        "name": "Your Status",
                        "value": survey_your_status,
                        "inline": False
                    },
                    {
                        "name": "Start Time",
                        "value": survey_start_time
                    },
                    {
                        "name": "End Time",
                        "value": survey_end_time
                    }
                ]
            }
            sendMessage(config["discord_channel"], "", embed)

        time.sleep(1)

        reports = manaba.getCourseReports(course_id)

        for report in reports:
            report_id = report["id"]
            if report_id in readed:
                continue

            report_title = report["title"]
            report_status = report["status"]
            report_status_lamp = report["status_lamp"]
            report_your_status = report["your_status"]
            report_start_time = report["start_time"]
            report_end_time = report["end_time"]

            if not report_status_lamp:
                continue

            readed.append(report_id)
            if init:
                continue

            embed = {
                "title": "[REPORT] " + report_title,
                "type": "rich",
                "url": config["base_url"] + "/ct/" + report_id,
                "fields": [
                    {
                        "name": "Status",
                        "value": report_status
                    },
                    {
                        "name": "Your Status",
                        "value": report_your_status
                    },
                    {
                        "name": "Start Time",
                        "value": report_start_time
                    },
                    {
                        "name": "End Time",
                        "value": report_end_time
                    }
                ]
            }
            sendMessage(config["discord_channel"], "", embed)

        time.sleep(1)

    with open("readed.json", "w") as f:
        f.write(json.dumps(readed))
