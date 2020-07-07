#!/bin/sh
enableProxy=$1
proxyIP=$2
applicationName=$3
flushInterval=$4
python3 ./shopping/manage.py runserver 50050 "$enableProxy" "$proxyIP"  "$applicationName" &
python3 ./styling/manage.py runserver 50051 "$enableProxy" "$proxyIP"  "$applicationName" &
python3 ./delivery/manage.py runserver 50052 "$enableProxy" "$proxyIP"  "$applicationName" &
./loadgen.sh "$flushInterval"

