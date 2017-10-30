FROM alpine:3.6
MAINTAINER Thomas Phil <thomas@tphil.nl>

RUN apk add --no-cache python2 python2-dev build-base

RUN python2 -m ensurepip && pip install fastr

RUN apk del unzip build-base python2-dev
