class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    class_code = db.Column(db.Integer)
    personality_id = db.Column(db.Integer, db.ForeignKey("personality.id"))

    def __init__(self, name, class_code, picture_url, personality_id):
        self.name = name
        self.class_code = class_code
        self.personality_id = personality_id


class Problem(db.Model):

    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.Text)
    options = db.Column(db.Text)

    def __init__(self, context, options):
        self.context = context
        self.options = options


class Personality(db.Model):

    __tablename__ = "personality"

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Text)
    description = db.Column(db.Text)
    linked_personality_jobs = db.relationship(
        "PersonalityJob", backref="personality", lazy="dynamic"
    )
    linked_students = db.relationship("Student", backref="personality", lazy="dynamic")

    def __init__(self, group, description):
        self.group = group
        self.description = description


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    linked_personality_jobs = db.relationship(
        "PersonalityJob", backref="job", lazy="dynamic"
    )

    def __init__(self, description):
        self.description = description


class PersonalityJob(db.Model):
    __tablename__ = "personalityjob"

    id = db.Column(db.Integer, primary_key=True)
    personality_id = db.Column(db.Integer, db.ForeignKey("personality.id"))
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))

    def __init__(self, personality_id, job_id):
        self.personality_id = personality_id
        self.job_id = job_id
