
FROM mysql:8
EXPOSE 3306

ENV DOCKERIZE_VERSION v0.6.1
ENV DOCKERIZE_FILENAME dockerize-linux-amd64-v0.6.1.tar.gz

FROM ubuntu:18.04
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y gcc locales curl python3-distutils python3-dev \
    && apt-get install -y libmysqlclient-dev mysql-client \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && pip install -U pip \
    && mkdir /src \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
RUN apt-get update && apt-get install -y wget
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
ENV LANG ja_JP.utf8
WORKDIR /src
ADD requirements.txt /src
RUN pip install -r requirements.txt    # requirements.txtからパッケージのインストール
