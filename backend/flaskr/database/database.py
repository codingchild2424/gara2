import csv
import os

from flaskr import db
from flaskr.models.models import *

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../csv")


def init_celebs():
    # 이름, 성향, 사진 url
    group_id = {
        "ENFJ": "1",
        "ENFP": "2",
        "ENTJ": "3",
        "ENTP": "4",
        "ESFJ": "5",
        "ESFP": "6",
        "ESTJ": "7",
        "ESTP": "8",
        "INFJ": "9",
        "INFP": "10",
        "INTJ": "11",
        "INTP": "12",
        "ISFJ": "13",
        "ISFP": "14",
        "ISTJ": "15",
        "ISTP": "16",
    }
    with open(f"{basedir}/celebs.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in spamreader:
            name, group, picture_url = row

            celebrity = Celebrity(name, group_id[group], picture_url)
            db.session.add(celebrity)

        db.session.commit()


def init_jobs():
    # 직업명, 성향, 설명
    group_id = {
        "ENFJ": "1",
        "ENFP": "2",
        "ENTJ": "3",
        "ENTP": "4",
        "ESFJ": "5",
        "ESFP": "6",
        "ESTJ": "7",
        "ESTP": "8",
        "INFJ": "9",
        "INFP": "10",
        "INTJ": "11",
        "INTP": "12",
        "ISFJ": "13",
        "ISFP": "14",
        "ISTJ": "15",
        "ISTP": "16",
    }
    with open(f"{basedir}/jobs.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in spamreader:
            name, group, description = row
            job = Job(name, description, group_id[group])
            db.session.add(job)

        db.session.commit()


def init_personalities():
    # 성향, 설명
    with open(f"{basedir}/personalities.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in spamreader:
            group, description = row
            personality = Personality(group, description)
            db.session.add(personality)

        db.session.commit()


def init_surveys():
    # 문제, 선택지1, 선택지2, 선택지1 성향, 선택지2 성향
    opt_group = {
        "1": "E",
        "2": "I",
        "3": "S",
        "4": "N",
        "5": "T",
        "6": "F",
        "7": "J",
        "8": "P",
    }
    with open(f"{basedir}/surveys.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for idx, row in enumerate(spamreader):
            survey_context, option_1, option_2, option1_group, option2_group = row
            survey = Survey(survey_context)

            opt1 = opt_group[option1_group]
            opt2 = opt_group[option2_group]

            option1 = Option(idx + 1, option_1, opt1)
            option2 = Option(idx + 1, option_2, opt2)

            db.session.add(survey)
            db.session.add(option1)
            db.session.add(option2)

        db.session.commit()


def init_students():
    # 이름, 학반
    with open(f"{basedir}/students.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in spamreader:
            name, class_code = row
            student = Student(name, class_code)
            db.session.add(student)

        db.session.commit()
