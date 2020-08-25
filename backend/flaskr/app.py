from flask_migrate import Migrate
from flask import Flask

from flaskr import dbclient


app = Flask(__name__)
db = dbclient.connect(app)
Migrate(app, db)


@app.route("/<class_code>/student", methods=(["POST"]))
def post_student_info(name, picture, class_code):
    # 사진 등록, 학생 등록
    return


@app.route("/<class_code>/<name>")
def get_student_info(name, class_code):
    student = None
    return student  # 이름, 사진, 학급코드, (성향 그룹)


@app.route("/record", methods=(["POST"]))
def post_record(name, class_code, personality):
    # 설문 결과 등록
    return


@app.route("/job/<jobname>")
def get_job_info(jobname):
    job_info = None
    return job_info  # 분류, 설명


@app.route("/personality/<group>")
def get_personality(group):
    personality = None
    return personality  # 분류, 설명, 직업군, 학생들


def get_group_members(personality):
    group_members = None
    return group_members


@app.route("/groups")
def get_groups():
    groups = None
    return groups  # 16가지 그룹 정보


@app.route("/picture/<class_code>/<name>")
def get_picture_url(name, class_code):
    picture_url = None
    return picture_url  # 등록한 학생 사진 URL
