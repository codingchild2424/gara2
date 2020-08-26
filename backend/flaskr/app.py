from flask import Flask, request

from flaskr import dbclient, minioclient
import json

app = Flask(__name__)
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
    data = json.loads(requests.get_data(as_text=True))

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


@app.route("/picture/<class_code>/<name>")
def get_picture_url(name, class_code):
    object_name = f"{class_code}/{name}.jpg"
    picture_url = minio.presigned_get_object(
        bucket_name="images", object_name=object_name
    )
    return picture_url  # 등록한 학생 사진 URL


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    class_code = db.Column(db.Integer, nullable=False)
    identifier = db.Column(db.Text, unique=True)
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
            "personality_id": self.personality_id,
        }
        return json.dumps(data, ensure_ascii=False)


class Problem(db.Model):

    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.Text)
    options = db.Column(db.Text)

    def __init__(self, context, options):
        self.context = context
        self.options = options

    def jsonify(self):
        data = {"context": self.context, "options": self.options}
        return json.dumps(data, ensure_ascii=False)


class Personality(db.Model):

    __tablename__ = "personalities"

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Text)
    description = db.Column(db.Text)
    linked_personality_jobs = db.relationship(
        "PersonalityJob", backref="personalities", lazy="dynamic"
    )
    linked_students = db.relationship(
        "Student", backref="personalities", lazy="dynamic"
    )

    def __init__(self, group, description):
        self.group = group
        self.description = description

    def jsonify(self):
        data = {"group": self.group, "description": self.description}
        return json.dumps(data, ensure_ascii=False)


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    linked_personality_jobs = db.relationship(
        "PersonalityJob", backref="job", lazy="dynamic"
    )

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def jsonify(self):
        data = {"name": self.name, "description": self.description}
        return json.dumps(data, ensure_ascii=False)


# personailty_jobs = db.Table(
#     "personalityjob",
#     db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
#     db.Column("page_id", db.Integer, db.ForeignKey("page.id"), primary_key=True),
# )


class PersonalityJob(db.Model):
    __tablename__ = "personalityjob"

    id = db.Column(db.Integer, primary_key=True)
    personality_id = db.Column(db.Integer, db.ForeignKey("personalities.id"))
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))

    def __init__(self, personality_id, job_id):
        self.personality_id = personality_id
        self.job_id = job_id
