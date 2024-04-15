FROM python:3.9.9

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/app/
