# syntax=docker/dockerfile:1
FROM python:3.10.5-slim-bullseye

#docker build -t flask_app .
#docker image ls
#docker run -e AUTHOR='Johan' -e PORT=80 -p 80:80 flask_app

RUN mkdir wd
WORKDIR /wd

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./

CMD exec gunicorn --workers=1 --threads=8 -b :$PORT main:app