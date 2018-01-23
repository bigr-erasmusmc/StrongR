FROM ubuntu:16.04
MAINTAINER Thomas Phil <thomas@tphil.nl>

ARG FASTRVERSION=develop
ENV FASTRVERSION ${FASTRVERSION}
RUN export DEBIAN_FRONTED=noninteractive
RUN apt-get update && apt-get install -y python python-pip && pip install fastr==$FASTRVERSION

ENTRYPOINT '/bin/bash'
