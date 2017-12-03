#!/bin/bash

# if Docker.keep exist, then run immediately
test -f Docker.keep && docker run --rm ubuntu:tushare-16.04

# if Docker.update not exist, exit now
test ! -f Docker.update && exit

# update Docker image

mkdir xxx
pushd xxx


cat - > Dockerfile <<EOF
#FROM ubuntu:latest
#FROM ubuntu:17.04
FROM ubuntu:16.04

WORKDIR /root

RUN  echo 'Asia/ShangHai' > /etc/timezone  && \
     sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
     sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
     apt-get update && \
     apt-get -y install python-pip python-tk git command-not-found xvfb 

RUN  apt-get -y install s-nail

RUN  apt-get -y install locales

RUN  apt-get autoclean && apt-get autoremove && apt-get clean

RUN  pip install --upgrade pip

RUN  pip install lxml && \
     pip install pandas

RUN  pip install requests && \
     pip install astropy && \
     pip install bs4 && \
     pip install tushare && \
     pip install pp && \
     pip install matplotlib 

RUN  locale-gen zh_CN.UTF-8

ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8

RUN pip uninstall -y numpy pandas
RUN apt-get -y install python-numpy python-pandas
     
CMD git clone -b adx https://github.com/nkwilson/stock-v1.git && cd stock-v1 && bash -x run-in-docker.sh

EOF

#docker build -t ubuntu:tushare-1 .
#docker build -t ubuntu:tushare-17.04 .
docker build -t ubuntu:tushare-16.04 .
popd

docker run --rm ubuntu:tushare-16.04
