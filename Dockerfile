FROM python:3.8.5

COPY . /root/flask-app
WORKDIR /root/flask-app

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]