FROM ubuntu:16.04
MAINTAINER Thomas Phil <thomas@tphil.nl>

ADD https://gitlab.com/bbmri/infra/strongr/repository/rel-1.1/archive.zip /tmp/strongr.zip

RUN apt-get update && apt-get install -y unzip python2 python2-dev build-base mercurial

RUN python2 -m ensurepip && mkdir -p /opt/strongr && mkdir -p /opt/fastr && unzip -o /tmp/strongr.zip -d  /tmp && mv /tmp/strongr-rel*/* /opt/strongr/ && rm -rf /tmp/strongr* && pip install setuptools && pip install -r /opt/strongr/requirements.txt && hg clone https://bitbucket.org/bigr_erasmusmc/fastr /opt/fastr && cd /opt/fastr && hg checkout develop && pip install -e .


WORKDIR /opt/fastr
