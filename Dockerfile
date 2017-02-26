FROM ubuntu:14.04
MAINTAINER Dmitriy Apollonin <apollonin@gmail.com>

RUN apt-get update && apt-get install -y python-pip python-dev && apt-get clean

RUN pip install bottle
RUN pip install gevent
RUN pip install gunicorn
RUN pip install gevent-websocket
RUN pip install gevent-socketio
RUN pip install pymongo
RUN easy_install -U gevent==1.1b4

EXPOSE 8080 9999

WORKDIR /app
