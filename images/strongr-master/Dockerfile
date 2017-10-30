FROM strongr:1.0
MAINTAINER Thomas Phil <thomas@tphil.nl>

RUN apk add --no-cache salt-master salt-cloud salt-ssh

EXPOSE 4505 4506
VOLUME ["/etc/salt/pki", "/var/cache/salt", "/var/logs/salt", "/etc/salt/master.d", "/srv/salt"]

CMD "python app.py r:r"
