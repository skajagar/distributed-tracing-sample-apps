#!/bin/sh
enableProxy=$1
proxyIPOrDIToken=$2
applicationName=$3
flushInterval=$4
python3 ./shopping/manage.py runserver 50050 "$enableProxyEnv" "$proxyIPOrWFClustterEnv" "$ProxyPortorWFTokenEnv" "$applicationNameEnv"
python3 ./styling/manage.py runserver 50051 "$enableProxyEnv" "$proxyIPOrWFClustterEnv" "$ProxyPortorWFTokenEnv" "$applicationNameEnv"
python3 ./delivery/manage.py runserver 50052 "$enableProxyEnv" "$proxyIPOrWFClustterEnv" "$ProxyPortorWFTokenEnv" "$applicationNameEnv"
./loadgen.sh "$flushInterval"
