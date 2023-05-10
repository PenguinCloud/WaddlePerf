#! /bin/bash
export URL="https://github.com/esnet/iperf/archive/refs/tags/3.13.tar.gz"
apt update && apt install gcc build-essential checkinstall wget -y
echo "Downloading: $URL"
wget $URL -O /opt/iperf3.tar.gz
cd /opt/
rm -rf /opt/iperf3
mkdir /opt/iperf3 
tar -xvzf iperf3.tar.gz -C /opt/iperf3 --strip-components=1
cd /opt/iperf3
./configure && checkinstall make --install=no --pkgname="iperf3" --pkgversion="3" --pkgrelease="1" --nodoc -y -j4
