FROM ubuntu

WORKDIR /root

RUN  echo 'Asia/ShangHai' > /etc/timezone  &&      sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list &&      sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list &&      apt-get update &&      apt-get -y install python-pip python-tk git command-not-found xvfb &&     apt-get autoclean &&      apt-get autoremove &&      pip install --upgrade pip

RUN  pip install lxml &&      pip install pandas

RUN  pip install requests &&      pip install astropy &&      pip install bs4 &&      pip install tushare &&      pip install pp &&      pip install matplotlib &&      git clone -b adx https://github.com/nkwilson/stock-v1.git

RUN  apt-get -y install s-nail && apt-get autoclean && apt-get autoremove && apt-get clean

RUN  locale-gen zh_CN.UTF-8

RUN  touch a && rm -f a && cd stock-v1 && git pull

ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8
	
CMD cd stock-v1 && git pull && bash -x run-in-docker.sh

