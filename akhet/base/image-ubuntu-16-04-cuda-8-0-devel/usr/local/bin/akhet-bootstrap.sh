#!/bin/bash
#
#
set -e
set -x
if [[ "$AKHETBASE_VNCPASS" == "" ]] ; then
   echo "Missing AKHETBASE_VNCPASS"
   exit 1
fi

if test ! -d /var/run/akhet
then
   echo "Missing /var/run/akhet directory"
   exit 1
fi
if test ! -d /root/.vnc
then
   echo "Missing /root/.vnc directory"
   exit 1
fi

if test ! -d /var/run/akhet/status/
then
  mkdir /var/run/akhet/status/
fi

/usr/bin/openssl req -new -x509 -days 365 -nodes -out /self.pem -keyout /self.pem -batch &
touch /var/run/akhet/status/certs

websockify 6080 127.0.0.1:5900 -v --cert=/self.pem --key=/self.pem -D
touch /var/run/akhet/status/websockify

x11vnc -storepasswd $AKHETBASE_VNCPASS /root/.vnc/passwd
touch /var/run/akhet/status/vnc-pass

Xorg +extension GLX +extension RANDR +extension RENDER  -config /etc/X11/xorg.conf :0 &
touch /var/run/akhet/status/x11-host

if [[ "$AKHETBASE_USER_LABEL" != "" ]] ; then
    usermod -c "$AKHETBASE_USER_LABEL" user
fi

if [[ ! -z $AKHETBASE_GIDs ]]
then
    for gid in $AKHETBASE_GIDs ; do
        getent group $gid || groupadd -g $gid g$gid
        adduser user $(getent group $gid | awk -F":" '{ print $1 }')
    done
fi

if [ ! -z $AKHETBASE_UID ]
then
  usermod -u $AKHETBASE_UID user
else
  export AKHETBASE_UID=$(id -u user)
fi
chown user:user /home/user

if [ ! -z $AKHETBASE_USER ]
then
  usermod -l $AKHETBASE_USER user
else
  export AKHETBASE_USER=user
fi
touch /var/run/akhet/status/user-setup

service dbus start
touch /var/run/akhet/status/dbus

/usr/local/bin/supervisord \
  -c /etc/supervisor/supervisord.conf
touch /var/run/akhet/status/supervisor

if [[ "$AKHETBASE_SHARED" == "1" ]] ; then
 SHARED="-shared"
else
 SHARED="-nevershared -dontdisconnect"
fi

if [[ "$AKHETBASE_PERSISTENT" != "1" ]] ; then
    for i in $(seq 1 3) ; do
        x11vnc \
          -ncache 0 \
          -flag /var/run/akhet/status/vnc-server \
          -rfbport 5900 \
          -usepw \
          -display :0 \
          -noxdamage \
          -xrandr \
          $SHARED \
          -timeout 60 \
          -ping 1 \
          -repeat
        echo $?
    done
else
    x11vnc \
      -ncache 0 \
      -flag /var/run/akhet/status/vnc-server \
      -rfbport 5900 \
      -usepw \
      -display :0 \
      -noxdamage \
      -xrandr \
      $SHARED \
      -forever \
      -ping 1 \
      -repeat
    echo $?
fi
