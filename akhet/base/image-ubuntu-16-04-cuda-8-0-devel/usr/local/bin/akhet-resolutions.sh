#!/bin/bash
if [[ "$1" == "get" ]] ; then
    /usr/bin/xrandr 2> /dev/null | grep -P ' \d{3,4}x\d{3,4} ' | awk '{ print $1 }'
elif [[ "$1" == "set" ]] ; then
    /usr/bin/xrandr --size "$2"
fi
