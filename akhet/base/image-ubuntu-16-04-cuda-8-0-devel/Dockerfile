FROM        nvidia/cuda:8.0-devel-ubuntu16.04

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

ENV DISPLAY :0

ADD ./etc/apt/sources.list /etc/apt/sources.list

RUN apt-get update && \
  apt-get dist-upgrade --assume-yes --allow-change-held-packages --allow-downgrades --allow-remove-essential && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete

RUN apt-get -y install apt-utils && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install dbus && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install x11-utils && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install x11-xserver-utils && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install xserver-xorg-video-dummy && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install xinit && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install openssl ca-certificates && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install x11vnc && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python3 && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python-numpy && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python3-numpy && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python-dev && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python3-dev && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python-setuptools && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install python3-setuptools && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install rsync && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install wget && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install ssh && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install git && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install htop && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install strace && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y install lsof && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y build-essential && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y cmake && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y mesa-utils && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete

RUN easy_install pip
RUN pip2 install supervisor && mkdir /var/log/supervisor/
RUN pip2 install websockify

RUN mkdir /var/run/akhet /root/.vnc

RUN useradd -m user -u 1000 -s /bin/bash

ADD ./etc/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
ADD ./usr/local/bin/akhet-bootstrap.sh   /usr/local/bin/
ADD ./usr/local/bin/akhet-resolutions.sh /usr/local/bin/
ADD ./etc/X11/xorg.conf /etc/X11/xorg.conf

EXPOSE 5900 6080

ENTRYPOINT ["/usr/local/bin/akhet-bootstrap.sh"]

LABEL akhetimage=true
