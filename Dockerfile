#FROM python:3.10-alpine3.16
FROM python:3.10-alpine

WORKDIR /autoworld
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

#RUN apk add postgresql-client build-base postgresql-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc linux-headers postgresql-dev python3-dev libstdc++ g++

RUN pip3 install kiwisolver
COPY requirements.txt /temp/requirements.txt
RUN #pip install --no-cache-dir -r /temp/requirements.txt
RUN pip install --upgrade pip & pip install --upgrade setuptools & pip install --no-cache-dir -r /temp/requirements.txt

COPY autoworld /autoworld
#USER root

RUN adduser --disabled-password autoworld-user

USER autoworld-user