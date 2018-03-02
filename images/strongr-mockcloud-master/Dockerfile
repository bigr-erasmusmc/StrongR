FROM ubuntu:16.04
MAINTAINER Thomas Phil <thomas@tphil.nl>

ADD https://gitlab.com/bbmri/infra/strongr/repository/rel-1.1/archive.zip /tmp/strongr.zip
ADD config.json /root/.strongr/config.json
ADD config.py /root/.fastr/config.py
ADD addtask /opt/strongr/addtask
ADD queryqueue /opt/strongr/queryqueue

RUN apt-get update && apt-get install -y unzip python2.7 python2.7-dev build-essential mercurial python-pip ca-certificates docker.io

RUN chmod +x /opt/strongr/queryqueue && chmod +x /opt/strongr/addtask

RUN mkdir -p /opt/strongr && mkdir -p /opt/fastr && unzip -o /tmp/strongr.zip -d  /tmp && mv /tmp/strongr-rel*/* /opt/strongr/ && rm -rf /tmp/strongr* && pip install setuptools && pip install -r /opt/strongr/requirements.txt && hg clone --insecure https://bitbucket.org/bigr_erasmusmc/fastr /opt/fastr && cd /opt/fastr && hg checkout develop && pip install -e .

RUN cd /opt/strongr && python app.py d:create


WORKDIR /opt/strongr
CMD ["python", "app.py", "r:r"]
