FROM python:3.8.5

COPY . /root/
WORKDIR /root/

RUN pip install -r requirements.txt

ENV FLASK_APP flaskr/app.py

ENTRYPOINT [ "flask", "run", "-h", "0.0.0.0", "-p", "5000" ]