from minio import Minio


def connect():
    minio_client = Minio(
        endpoint="localhost:9000",
        access_key="garaproj",
        secret_key="garaproj",
        secure=False,
    )

    return minio_client
