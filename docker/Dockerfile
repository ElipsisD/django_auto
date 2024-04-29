FROM python:3.12
LABEL authors="Dmitry"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y locales gcc musl-dev bash zlib1g-dev libjpeg-dev && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && apt-get clean

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.4.0 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

WORKDIR /autoworld
COPY . /autoworld

EXPOSE 8000
