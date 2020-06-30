#!/bin/sh
enableProxy=$1
proxyIPOrDIToken=$2
applicationName=$3
flushInterval=$4
python3 ./shopping/manage.py runserver 50050 "$enableProxy" "$proxyIPOrDIToken" "$applicationName"
python3 ./styling/manage.py runserver 50051 "$enableProxy" "$proxyIPOrDIToken" "$applicationName"
python3 ./styling/manage.py runserver 50052 "$enableProxy" "$proxyIPOrDIToken" "$applicationName"
./loadgen.sh "$flushInterval"