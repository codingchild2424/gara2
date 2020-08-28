from flask import Flask, request
from flask_cors import CORS

import dbclient, minioclient, json, csv, os

app = Flask(__name__)
CORS(app)
db = dbclient.connect(app)
minio = minioclient.connect()


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


def get_picture_url(name, class_code):
    object_name = f"{class_code}/{name}.jpg"
    picture_url = minio.presigned_get_object(
        bucket_name="images", object_name=object_name
    )
    return picture_url  # 등록한 학생 사진 URL


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    class_code = db.Column(db.Integer, nullable=False)
    personality_id = db.Column(db.Integer, db.ForeignKey("personalities.id"))

    def __init__(self, name, class_code, personality_id=None):
        self.name = name
        self.class_code = class_code
        self.personality_id = personality_id
        self.identifier = f"{class_code}-{name}"

    def jsonify(self):
        data = {
            "name": self.name,
            "class_code": self.class_code,
            "group": self.personality.group if self.personality != None else "",
            "picture_url": get_picture_url(self.name, self.class_code),
        }
        return json.dumps(data, ensure_ascii=False)


class Survey(db.Model):

    __tablename__ = "surveys"

    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.Text)
    options = db.relationship("Option", backref="survey", lazy="dynamic")

    def __init__(self, context):
        self.context = context

    def jsonify(self):
        data = {
            "context": self.context,
            "options": [option.context for option in self.options],
        }
        return json.dumps(data, ensure_ascii=False)


class Option(db.Model):

    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.id"))
    context = db.Column(db.Text)
    personality = db.Column(db.Text)

    def __init__(self, survey_id, context, personality):
        self.survey_id = survey_id
        self.context = context
        self.personality = personality


class Personality(db.Model):

    __tablename__ = "personalities"

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text)
    students = db.relationship("Student", backref="personality", lazy="dynamic")
    celebrities = db.relationship("Celebrity", backref="personality", lazy="dynamic")
    jobs = db.relationship("Job", backref="personality", lazy="dynamic")

    def __init__(self, group, description):
        self.group = group
        self.description = description

    def jsonify(self):
        data = {
            "group": self.group,
            "description": self.description,
            "students": [student.name for student in self.students],
            "jobs": [job.name for job in self.jobs],
            "celebrities": [celebrity.name for celebrity in self.celebrities],
        }
        return json.dumps(data, ensure_ascii=False)


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text)
    personality_id = db.Column(db.Integer, db.ForeignKey("personalities.id"))

    def __init__(self, name, description, personality_id):
        self.name = name
        self.description = description
        self.personality_id = personality_id

    def jsonify(self):
        data = {
            "name": self.name,
            "description": self.description,
            "group": self.personality.group,
        }
        return json.dumps(data, ensure_ascii=False)


class Celebrity(db.Model):

    __tablename__ = "celebrities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    personality_id = db.Column(db.Integer, db.ForeignKey("personalities.id"))
    picture_url = db.Column(db.Text)

    def __init__(self, name, personality_id, picture_url):
        self.name = name
        self.personality_id = personality_id
        self.picture_url = picture_url


########## INITAILIZE DATABASE ##############

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./csv")


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


# db.create_all()

# init_students()
# init_personalities()
# init_jobs()
# init_celebs()
# init_surveys()