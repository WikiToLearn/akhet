#!/bin/bash
# set -x
# set -e
if [[ ! -z $whitelist ]] || [[ ! -z $blacklist ]]
then
  iptables -t filter -A OUTPUT -m state ! --state NEW -j ACCEPT
  iptables -t filter -A OUTPUT -o lo -j ACCEPT
  iptables -t filter -A OUTPUT -m owner --uid-owner root -j ACCEPT
  iptables -t filter -A OUTPUT -m owner --gid-owner root -j ACCEPT

  rules=""
  rule_P=""
  rule_D=""
  if [[ ! -z $whitelist ]]
  then
    rules=$whitelist
    rule_P="ACCEPT"
    rule_D="DROP"
  elif [[ ! -z $blacklist ]]; then
    rules=$blacklist
    rule_P="DROP"
    rule_D="ACCEPT"
  fi

  for rule in $rules ; do
    if [[ "${rule:0:5}" == "HOST:" ]]
    then
      iptables -t filter -A OUTPUT -d ${rule:5} -j $rule_P
    fi
  done
  iptables -t filter -P OUTPUT $rule_D
fi

echo "Wait...wait...wait..."
sleep infinity
