FROM ubuntu

WORKDIR /root

RUN  echo 'Asia/ShangHai' > /etc/timezone  && \
     echo 'mirrors.aliyun.com archive.ubuntu.com' >> /etc/hosts && \
     apt-get update && \
     apt-get -y install python-pip python-tk git command-not-found xvfb &&\
     apt-get autoclean && \
     apt-get autoremove && \
     pip install --upgrade pip && \
     pip install lxml && \
     pip install pandas && \
     pip install requests && \
     pip install astropy && \
     pip install bs4 && \
     pip install tushare && \
     pip install pp && \
     pip install matplotlib && \
     git clone https://github.com/nkwilson/stock-v1.git

