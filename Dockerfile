FROM ubuntu:18.04

RUN apt update
RUN apt install -y \
  git \
  build-essential \
  software-properties-common

RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get update

RUN apt-get install -y \
  gdal-bin \
  git \
  libsqlite3-dev \
  zlib1g-dev \
  libstdc++6 \
  libstdc++-5-dev \
  libffi-dev \
  libgdal-dev \
  libsqlite3-dev \
  libstdc++-5-dev \
  libstdc++6 \
  libxml2-dev \
  libxslt1-dev \
  libssl1.0-dev \
  nodejs \
  node-gyp \
  nodejs-dev \
  npm \
  python-dev \
  python-gdal \
  python-pip \
  python3-dev \
  python3-gdal \
  software-properties-common \
  zlib1g-dev

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip3 install flask flask_cors

