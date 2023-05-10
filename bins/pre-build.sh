#! /bin/bash
apt update && apt install gcc build-essential checkinstall wget -y
wget $URL -O /opt/iperf3.tar.gz
cd /opt/
mkdir /opt/iperf3
tar -xvzf iperf3.tar.gz -C /opt/iperf3 --strip-components=1
cd /opt/iperf3
./configure && checkinstall --install=no --pkgname="iperf3" --pkgversion="3" --pkgrelease="1" --nodoc -y make
