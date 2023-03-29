FROM python:3.10-alpine3.16

COPY requirements.txt /temp/requirements.txt
WORKDIR /autoworld
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

#RUN apk add postgresql-client build-base postgresql-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc linux-headers postgresql-dev


RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY autoworld /autoworld
#USER root

RUN adduser --disabled-password autoworld-user

USER autoworld-user