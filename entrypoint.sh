#!/bin/bash
ansible-playbook entrypoint.yml  -c local 
/opt/manager/bins/pyweb.sh &
/opt/manager/bins/server.sh
echo "Sleeping awaiting action!"
/bin/sleep infinity
