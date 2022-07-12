FROM python:3.9.12-bullseye
LABEL Lucas Calegario

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update; apt-get clean

RUN apt-get install -y x11vnc
RUN apt-get install -y xvfb
RUN apt-get install -y fluxbox
RUN apt-get install -y wget
RUN apt-get install -y wmctrl
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /crawler
COPY ./api /api
COPY crawler /crawler
RUN python3 -m pip install -e /api

RUN useradd -ms /bin/bash user
RUN chown -R user .
USER user