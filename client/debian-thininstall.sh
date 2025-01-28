#! /bin/bash
$PPING_REPO = "wzv5/pping"
$VERSION = curl --silent "https://api.github.com/repos/wzv5/pping/releases/latest" | jq -r .tag_name | cut -d "v" -f 2

echo "Pulling latest version $VERSION"

apt install iperf3 speedtest-cli httping python3-pip -y
pip3 install ansible

if [[ $(uname -m) == "arm64" ]]; then
  echo "This is an ARM-based Mac"
  wget https://github.com/wzv5/pping/releases/download/v${VERSION}/pping_${VERSION}_Linux_arm64.tar.gz
  tar -xvf pping_${VERSION}_Darwin_arm64.tar.gz -C pping
  
else
  echo "This is not an ARM-based Mac, assuming x86_64"
  wget https://github.com/wzv5/pping/releases/download/v${VERSION}/pping_${VERSION}_Linux_x86_64.tar.gz
  tar -xvf pping_${VERSION}_Darwin_x86_64.tar.gz -C pping
fi

mv pping/pping /usr/local/bin/pping
chmod +x /usr/local/bin/pping