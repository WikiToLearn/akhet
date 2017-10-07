FROM debian:9

ADD ./etc/apt/sources.list /etc/apt/sources.list

RUN apt-get update && apt-get dist-upgrade -y

RUN apt-get install -y python3 && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y python3-setuptools && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y python3-dev && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y build-essential && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y libssl-dev && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get install -y ca-certificates && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete

RUN easy_install3 pip
RUN pip3 install requests
RUN pip3 install pyopenssl
RUN pip3 install pyee
RUN pip3 install pika
RUN pip3 install pymongo
RUN pip3 install flask
RUN pip3 install eve
RUN pip3 install pyyaml

ENV PYTHONUNBUFFERED=0

STOPSIGNAL 9

ADD ./srv/akhet-libs/ /srv/akhet-libs/
RUN pip install /srv/akhet-libs/AkhetInstance/ && rm -Rf /srv/akhet-libs/AkhetInstance/
RUN pip install /srv/akhet-libs/AkhetInstanceManager/ && rm -Rf /srv/akhet-libs/AkhetInstanceManager/
