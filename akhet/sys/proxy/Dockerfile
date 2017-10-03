FROM akhet/sys/base:latest

RUN apt-get update && apt-get -y install perl               && rm -f /var/cache/apt/archives/*deb && find /var/lib/apt/lists/ -type f -delete && find /var/log/ -type f -delete
RUN apt-get update && apt-get -y install xml-core           && rm -f /var/cache/apt/archives/*deb && find /var/lib/apt/lists/ -type f -delete && find /var/log/ -type f -delete
RUN apt-get update && apt-get -y install nginx-extras       && rm -f /var/cache/apt/archives/*deb && find /var/lib/apt/lists/ -type f -delete && find /var/log/ -type f -delete
RUN apt-get update && apt-get -y install cron               && rm -f /var/cache/apt/archives/*deb && find /var/lib/apt/lists/ -type f -delete && find /var/log/ -type f -delete
RUN apt-get update && apt-get -y install openssl            && rm -f /var/cache/apt/archives/*deb && find /var/lib/apt/lists/ -type f -delete && find /var/log/ -type f -delete
RUN apt-get update && apt-get -y install dnsmasq            && rm -f /var/cache/apt/archives/*deb && find /var/lib/apt/lists/ -type f -delete && find /var/log/ -type f -delete

RUN rm /var/www/html/* -Rfv && mkdir /etc/akhet/

ENV AKHET_RUN_DIR  /var/run/akhet/
ENV AKHET_CONF_DIR /etc/akhet/

ENTRYPOINT /opt/entrypoint.sh

EXPOSE 8080 8443

ADD ./etc/ /etc/
ADD ./var/www/html/ /var/www/html/
ADD ./opt/ /opt/
