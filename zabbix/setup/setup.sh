#!/usr/bin/env bash

set -e

net1=$(ip addr list | grep inet | grep eth0 | awk {'print $2'} | cut -d'.' -f1)
net2=$(ip addr list | grep inet | grep eth0 | awk {'print $2'} | cut -d'.' -f2)
net3=$(ip addr list | grep inet | grep eth0 | awk {'print $2'} | cut -d'.' -f3)
sleep 20
until python setup.py "$net1.$net2.$net3"; do
  >&2 echo "Zabbix indisponível - sleeping"
  sleep 10
done

>&2 echo "Monitoramento zabbix iniciado"
