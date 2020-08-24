class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    class_code = db.Column(db.Integer)
    picture_url = db.Column(db.Text)
    personality_group = db.Column(db.Text)

    def __init__(self, name, class_code, picture_url, personality_group):
        self.name = name
        self.class_code = class_code
        self.picture_url = picture_url
        self.personality_group = personality_group

    def __repr__(self):
        return f"{self.name} is {self.grade} grade student"


class Problem(db.Model):

    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.Text)
    options = db.Column(db.Text)


class Personality(db.Model):

    __tablename__ = "personality"

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Text)
    describtion = db.Column(db.Text)
    personalityjobs = [PersonalityJob]
    students = [Student]


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    personalityjobs = [PersonalityJob]


class PersonalityJob(db.Model):
    __tablename__ = "personalityjob"

    id = db.Column(db.Integer, primary_key=True)
    personaility = Personality
    job = Job
