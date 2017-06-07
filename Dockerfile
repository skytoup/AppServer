############################################################
# Build a AppServer container images
# 不修改 app/config/config.py:BaseConfig.host , 会导致iOS无法在线下载安装ipa
# 使用: 
#    1. docker build -t app_server ./
#    2. docker run -d -p 8000:8000 -v /path/to/data:/www/AppServer/data -v /path/to/log:/www/AppServer/log --name AppServer app_server
#			or
#		docker run -d -p 8000:8000 --name AppServer app_server
############################################################

FROM centos:latest

MAINTAINER skytoup 875766917@qq.com

RUN yum -y install zlib* sqlite-devel gcc make python-setuptools openssl openssl-devel libpng12

# install python3.6.1
RUN curl -O https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz \
    && tar -zxvf Python-3.6.1.tgz && cd Python-3.6.1 \
    && ./configure --with-ssl --enable-loadable-sqlite-extensions \
    && make \
    && make install \
    && cd .. \
	&& rm -rf Python-3.6.1*

RUN mkdir -p /www/AppServer
COPY ./ /www/AppServer

WORKDIR /www/AppServer
RUN gcc vendors/pngdefry/pngdefry.c -o pngdefry
RUN mkdir data log
RUN python3 -m pip install -i https://pypi.douban.com/simple/ -r requirements.txt

VOLUME ["data", "log"]
EXPOSE 8000

CMD ["python3", "main.py"]
