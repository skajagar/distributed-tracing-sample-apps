#!/bin/sh
enableProxy=$1
proxyIPOrWFClustter=$2
ProxyPortorWFToken$3
applicationName=$4
flushInterval=$5
python3 ./shopping/manage.py runserver 50050 "$enableProxyEnv" "$proxyIPOrWFClustterEnv" "$ProxyPortorWFTokenEnv" "$applicationNameEnv" &
python3 ./styling/manage.py runserver 50051 "$enableProxyEnv" "$proxyIPOrWFClustterEnv" "$ProxyPortorWFTokenEnv" "$applicationNameEnv" &
python3 ./delivery/manage.py runserver 50052 "$enableProxyEnv" "$proxyIPOrWFClustterEnv" "$ProxyPortorWFTokenEnv" "$applicationNameEnv" &
./loadgen.sh "$flushInterval"
