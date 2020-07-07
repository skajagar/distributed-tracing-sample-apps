#!/bin/sh
enableProxy=$1
DICluster=$2
DIToken=$3
batchSize=$4
queueSize=$5
DIflushInteval=$6
applicationName=$7
loadgenFlushInterval=$8
python3 ./shopping/manage.py runserver 50050 "$enableProxy" "$DICluster" "$DIToken" "$batchSize" "$queueSize" "$DIflushInteval" "$applicationName" &
python3 ./styling/manage.py runserver 50051 "$enableProxy" "$DICluster" "$DIToken" "$batchSize" "$queueSize" "$DIflushInteval" "$applicationName" &
python3 ./delivery/manage.py runserver 50052 "$enableProxy" "$DICluster" $DIToken "$batchSize" "$queueSize" "$DIflushInteval" "$applicationName" &
./loadgen.sh "$loadgenFlushInterval"