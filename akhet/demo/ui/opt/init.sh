#!/bin/bash
service apache2 start
cron
echo "Waiting..."
while test ! -f /var/log/apache2/error.log
do
  sleep 1
done
while test ! -f /var/log/apache2/access.log
do
  sleep 1
done
tailf /var/log/apache2/access.log
