#!/bin/bash
ansible-playbook entrypoint.yml  -c local 
/opt/penguinperf3/pyweb.sh &
/opt/manager/bins/server.sh

#echo "Sleepy time!"
#/usr/bin/sleep infinity
