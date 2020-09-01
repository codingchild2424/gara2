import csv
import json
import os

from flask import Flask, request

from database import database
from flaskr import app, db, minio
from models.models import *

db.create_all()
database.init_students()
database.init_surveys()
database.init_personalities()
database.init_celebs()
database.init_jobs()


@app.route("/student", methods=(["POST"]))
def post_student_info():
    data = json.loads(request.get_data(as_text=True))

    student = _post_student_info(data["name"], data["class_code"])
    return student.jsonify()


def _post_student_info(name, class_code):  # 사진 등록, 학생 등록
    data = json.loads(request.get_data(as_text=True))

    student = Student(data["name"], data["class_code"])
    db.session.add(student)
    db.session.commit()
    return student


@app.route("/student/<class_code>/<name>")
def get_student_info(name, class_code):  # 이름, 사진, 학급코드, (성향 그룹)
    student = Student.query.filter_by(identifier=f"{class_code}-{name}").first()
    return student.jsonify()


@app.route("/record", methods=(["POST"]))
def post_record():  # 설문 결과 등록
    data = json.loads(request.get_data(as_text=True))

    student = _post_record(data["name"], data["class_code"], data["personality"])
    return student.jsonify()


def _post_record(name, class_code, personality):
    student = db.Query.filter_by(identifier=f"{class_code}-{name}").first()
    personality = db.Query.filter_by(group=personality).first()
    student.personality_id = personality.id
    db.session.add(student)
    db.session.commit()
    return student


@app.route("/job/<name>")
def get_job_info(name):
    job = Job.query.filter_by(name=f"{name}").first()
    return job.jsonify()  # 분류, 설명


@app.route("/personality/<group>")
def get_personality(group):
    personality = Personality.query.filter_by(group=f"{group}").first()
    return personality.jsonify()  # 분류, 설명, 직업군, 학생들


def get_group_members(personality):
    group_members = None
    return group_members


@app.route("/groups")
def get_groups():
    groups = None
    return groups  # 16가지 그룹 정보


@app.route("/survey/<survey_id>")
def get_survey(survey_id):
    survey = Survey.query.get(survey_id)
    return survey.jsonify()


@app.route("/picture/<class_code>/<name>")
def get_picture_url(name, class_code):
    object_name = f"{class_code}/{name}.jpg"
    picture_url = minio.presigned_get_object(
        bucket_name="images", object_name=object_name
    )
    return picture_url  # 등록한 학생 사진 URL
