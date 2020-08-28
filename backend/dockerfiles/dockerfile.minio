FROM minio/minio

ENV MINIO_ACCESS_KEY=
ENV MINIO_SECRET_KEY=

COPY ./pictures/ /data

CMD ["server", "/data"]