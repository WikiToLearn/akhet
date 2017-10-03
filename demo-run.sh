#!/bin/bash
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
if test ! -f $SCRIPTPATH/demo-run.sh
then
  echo "Error detecting the workdir"
  exit
fi

CONFIG_AGENT=`pwd`/config/akhet-agent.yml
if test -f /etc/akhet/agent.yml
then
  CONFIG_AGENT=/etc/akhet/agent.yml
fi

CONFIG_PROXY=`pwd`/config/akhet-proxy.yml
if test -f /etc/akhet/proxy.yml
then
  CONFIG_PROXY=/etc/akhet/proxy.yml
fi

CONFIG_DEMO_UI=`pwd`/config/akhet-demo-ui.yml
if test -f /etc/akhet/demo-ui.yml
then
  CONFIG_DEMO_UI=/etc/akhet/demo-ui.yml
fi

CONFIG_API=`pwd`/config/akhet-api.yml
if test -f /etc/akhet/api.yml
then
  CONFIG_API=/etc/akhet/api.yml
fi

for f in \
  $CONFIG_AGENT \
  $CONFIG_PROXY \
  $CONFIG_DEMO_UI \
  $CONFIG_API
do
  if test ! -f "$f"
  then
    echo "Missing $f file"
    exit 1
  fi
  echo "Using $f"
done

if [[ $(docker container ps --filter name=^/akhet -q   | wc -l) -gt 0 ]]
then
  docker container kill $(docker container ps --filter name=^/akhet -q)
fi

if [[ $(docker container ps --filter name=^/akhet -aq  | wc -l) -gt 0 ]]
then
  docker container rm   $(docker container ps --filter name=^/akhet -aq)
fi

if [[ $(docker volume ls --filter name=^akhet -q       | wc -l) -gt 0 ]]
then
  docker volume    rm   $(docker volume ls --filter name=^akhet -q)
fi

if ! docker image inspect mongo:3 &> /dev/null
then
  if ! docker image pull mongo:3
  then
    echo "Missing mongo:3"
    exit 1
  fi
fi
for img in \
  akhet/sys/api:latest \
  akhet/sys/agent:latest \
  akhet/sys/proxy:latest \
  akhet/demo/ui:latest
do
  if ! docker image inspect $img &> /dev/null
  then
    echo "Missing $img"
    exit 1
  fi
done

docker container run \
  -tid \
  --hostname api-mongodb.akhet.tdl \
  --name akhet-api-mongodb \
  -v akhet-api-mongodb-configdb:/data/configdb \
  -v akhet-api-mongodb-db:/data/db \
  mongo:3
docker container run \
  -tid \
  --hostname api.akhet.tdl \
  --name akhet-api \
  --link akhet-api-mongodb:db \
  -v $CONFIG_API:/etc/akhet-api.yml \
  akhet/sys/api:latest

docker container run \
  -tid \
  --hostname `hostname -f` \
  --name akhet-agent \
  --link akhet-api:api \
  --add-host `hostname -f`:`ip route get 8.8.8.8 | awk '/8.8.8.8/ {print $NF}'` \
  -v $CONFIG_AGENT:/etc/akhet-agent.yml \
  -v /var/run/docker.sock:/var/run/docker.sock \
  akhet/sys/agent:latest

docker container run \
  -tid \
  --hostname proxy.akhet.tdl \
  --name akhet-proxy \
  --link akhet-api:api \
  --link akhet-agent:agent \
  --add-host `hostname -f`:`ip route get 8.8.8.8 | awk '/8.8.8.8/ {print $NF}'` \
  -v $CONFIG_PROXY:/etc/akhet-proxy.yml \
  akhet/sys/proxy:latest

docker container run \
  -tid \
  --hostname demo-ui.akhet.tdl \
  --name akhet-demo-ui \
  --link akhet-proxy:proxy \
  -p 8080:80 \
  -p 8433:433 \
  -v $CONFIG_DEMO_UI:/etc/akhet-demo-ui.yml \
akhet/demo/ui:latest
