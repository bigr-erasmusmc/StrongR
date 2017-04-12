FROM ubuntu:16.04
MAINTAINER t.phil <thomas@tphil.nl>

RUN apt-get update && \
  apt-get install -y wget && \
  wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add - && \
  echo "deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main" > /etc/apt/sources.list.d/saltstack.list && \
  apt-get update && \
  apt-get -y install salt-master salt-ssh salt-syndic salt-cloud salt-api python python-pip bash && \
  mkdir /opt/strongr

VOLUME ["/opt/strongr"]
