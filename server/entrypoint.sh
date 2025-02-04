#!/bin/bash
ansible-playbook entrypoint.yml  -c local --tags run 
sed -i 's/ \{2,\}/ /g' /opt/waddleperf/iperf3-server
echo "Starting NGINX and Iperf servers"
nohup /usr/local/bin/iperf3-server &
/usr/sbin/nginx -g 'daemon off;'