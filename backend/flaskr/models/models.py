import json

from flaskr import db


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
            "options": [
                (option.personality, option.context) for option in self.options
            ],
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
