#!/bin/bash
ansible-playbook entrypoint.yml  -c local --tags run
/opt/waddleperf3/pyweb.sh &
/opt/manager/bins/server.sh

#echo "Sleepy time!"
#/usr/bin/sleep infinity
