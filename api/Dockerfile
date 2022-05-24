FROM python:3.9.12-bullseye
MAINTAINER Lucas Calegario

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /api
COPY ./crawler /crawler
COPY ./api /api

RUN useradd -ms /bin/bash user
USER user
