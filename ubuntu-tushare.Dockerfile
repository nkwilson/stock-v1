FROM ubuntu

RUN  echo 'Asia/ShangHai' > /etc/timezone  &&
 echo 'mirrors.aliyun.com archive.ubuntu.com' >> /etc/hosts &&
 apt-get update && 
 apt-get -y install python-pip git command-not-found &&
 apt-get autoclean && 
 apt-get autoremove &&
 pip install lxml &&
 pip install pandas &&
 pip install requests &&
 pip install astropy &&
 pip install tushare &&
 pip install pp &&
 pip install --upgrade pip 

