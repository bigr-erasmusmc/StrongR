FROM ubuntu:16.04
MAINTAINER Thomas Phil <thomas@tphil.nl>

#ARG FASTRBRANCH develop
ARG FASTRBRANCH
RUN export DEBIAN_FRONTED=noninteractive
RUN apt-get update && apt-get install -y python python-pip mercurial && pip install --upgrade pip
RUN hg clone https://sikerdebaard@bitbucket.org/bigr_erasmusmc/fastr && cd fastr && hg checkout $FASTRBRANCH && hg pull && hg up && pip install -e .

ENTRYPOINT '/bin/bash'
