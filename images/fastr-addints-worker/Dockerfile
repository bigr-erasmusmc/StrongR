FROM bigr/fastr_worker

MAINTAINER T. Phil <thomas@tphil.nl>

RUN mkdir /opt/fastr-conf && mkdir /opt/strongr && touch /opt/strongr/init.sh
ENV FASTRHOME /opt/fastr-conf
ADD config.py /opt/fastr-conf/config.py
