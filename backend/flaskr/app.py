from flask import Flask


app = Flask(__name__)

# POST
@app.route("/<class_code>/student", methods=(["POST"]))
def post_student_info(name, picture, class_code):
    # 사진 등록, 학생 등록
    return


# GET
@app.route("/<class_code>/<name>")
def get_student_info(name, class_code):
    student = None
    return student  # 이름, 사진, 학급코드, (성향 그룹)


# POST
@app.route("/record", methods=(["POST"]))
def post_record(name, class_code, personality):
    # 설문 결과 등록
    return


# GET
@app.route("/job/<jobname>")
def get_job_info(jobname):
    job_info = None
    return job_info  # 분류, 설명


# GET
@app.route("/personality/<group>")
def get_personality(group):
    personality = None
    return personality  # 분류, 설명, 직업군, 학생들


def get_group_members(personality):
    group_members = None
    return group_members


# GET
@app.route("/groups")
def get_groups():
    groups = None
    return groups  # 16가지 그룹 정보
