FROM alpine:3.4
#FROM ubuntu:14.04
MAINTAINER Dmitriy Apollonin <apollonin@gmail.com>

#RUN apt-get update && apt-get install -y python-pip python-dev && apt-get clean

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && rm -rf /var/cache/apk/*

RUN pip install bottle
RUN pip install gunicorn
RUN pip install gevent
RUN pip install gevent-websocket


EXPOSE 8080

WORKDIR /app
