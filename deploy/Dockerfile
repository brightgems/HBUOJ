FROM ubuntu:latest
COPY requirements.txt /tmp/
RUN apt-get update && \
    apt-get install -y git gcc g++ make python-dev libxml2-dev libxslt1-dev zlib1g-dev ruby-sass gettext curl supervisor nginx && \
    wget -q --no-check-certificate -O- https://bootstrap.pypa.io/get-pip.py | python && \
    wget -O- https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g pleeease-cli && \
    pip install -r /tmp/requirements.txt

ENV SITE_BASE=/site
ENV LOGS_DIR=/logs

ADD . /site
WORKDIR /site

RUN npm install qu ws simplesets && \
    sh make_style.sh && \
    chmod +x deploy/entrypoint.sh

CMD ["/site/deploy/entrypoint.sh"]