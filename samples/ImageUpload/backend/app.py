import os

from flask import Flask, request
from flask_cors import CORS

UPLOAD_FOLDER = "./"


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    CORS(app)

    return app


app = create_app()


@app.route("/api/upload", methods=(["POST"]))
def post_image():
    file = request.files["file"]

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    return "Success"


if __name__ == "__main__":
    app.run(port=5000)
