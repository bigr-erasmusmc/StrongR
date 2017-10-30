FROM alpine:3.6
MAINTAINER Thomas Phil <thomas@tphil.nl>

ADD https://gitlab.com/bbmri/infra/strongr/repository/rel-1.0/archive.zip /tmp/strongr.zip

RUN apk add --no-cache unzip python2 python2-dev build-base

ENV ADDITIONAL_REQUIREMENTS flask flask_restplus celery
RUN python2 -m ensurepip && mkdir -p /opt/strongr && unzip -o /tmp/strongr.zip -d  /tmp && mv /tmp/strongr-rel*/* /opt/strongr/ && rm -rf /tmp/strongr* && pip install setuptools && pip install -r /opt/strongr/requirements.txt && pip install $ADDITIONAL_REQUIREMENTS

RUN apk del unzip build-base python2-dev

WORKDIR /opt/strongr
