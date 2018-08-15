FROM ubuntu:18.04

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

COPY requirements.txt /tmp/
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends wget git gcc g++ make python3.6-dev default-libmysqlclient-dev python3-pip python3-setuptools python3-wheel libxml2-dev libxslt1-dev zlib1g-dev ruby-sass gettext curl supervisor nginx nodejs npm && \
    npm install -g pleeease-cli && \
    pip3 install -r /tmp/requirements.txt

ENV SITE_BASE=/site
ENV LOGS_DIR=/logs

COPY . /site
WORKDIR /site

RUN npm install qu ws simplesets && \
    sh make_style.sh && \
    chmod +x deploy/entrypoint.sh

CMD ["/site/deploy/entrypoint.sh"]