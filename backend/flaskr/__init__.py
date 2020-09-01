import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from minio import Minio


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "./sqlite/data.sqlite"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    CORS(app)

    db = SQLAlchemy(app)

    minio = Minio(
        endpoint=f"minio:9000",
        access_key="garaproj",
        secret_key="garaproj",
        secure=False,
    )

    return (app, db, minio)


app, db, minio = create_app()
