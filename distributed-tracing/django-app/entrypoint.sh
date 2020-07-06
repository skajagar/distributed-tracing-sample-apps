#!/bin/sh
enableProxy=$1
proxyIPOrWFClustter=$2
ProxyPortorWFToken=$3
applicationName=$4
flushInterval=$5

python3 ./shopping/manage.py runserver 50050 "$enableProxy" "$proxyIPOrWFClustter" "$ProxyPortorWFToken" "$applicationName" &
python3 ./styling/manage.py runserver 50051 "$enableProxy" "$proxyIPOrWFClustter" "$ProxyPortorWFToken" "$applicationName" &
python3 ./delivery/manage.py runserver 50052 "$enableProxy" "$proxyIPOrWFClustter" "$ProxyPortorWFToken" "$applicationName" &
./loadgen.sh "$flushInterval"
