from minio import Minio


def connect(endpoint="localhost"):
    minio_client = Minio(
        endpoint=f"{endpoint}:9000",
        access_key="garaproj",
        secret_key="garaproj",
        secure=False,
    )

    return minio_client
