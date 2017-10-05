FROM        akhet/base/image-ubuntu-16-04:latest

ADD ./etc/apt/sources.list.d/neon.list /etc/apt/sources.list.d/neon.list

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E6D4736255751E5D
RUN apt-get update

RUN apt-get -y --allow-change-held-packages --allow-downgrades --allow-remove-essential install plasma-desktop && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y --allow-change-held-packages --allow-downgrades --allow-remove-essential install konsole && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete
RUN apt-get -y --allow-change-held-packages --allow-downgrades --allow-remove-essential install dolphin && \
  rm -f /var/cache/apt/archives/*deb && \
  find /var/log/ -type f -delete

ADD ./plasma.conf /etc/supervisor/conf.d/
