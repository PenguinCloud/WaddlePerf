#!/bin/bash
ansible-playbook entrypoint.yml  -c local --tags run 
sed -i 's/ \{2,\}/ /g' /opt/waddleperf/iperf3-server
sed -i 's/ \{2,\}/ /g' /opt/waddleperf/iperf3-client
/usr/sbin/nginx &
if [ "$IPERF_SERVER_ENABLED" == "true" ]
then
    echo "Starting NGINX and Iperf servers"
    /opt/manager/bins/server.sh
else
    echo "Sleepy time in client mode!"
    /usr/bin/sleep infinity
fi