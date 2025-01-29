#! /bin/bash
$PPING_REPO = "wzv5/pping"
$VERSION = curl --silent "https://api.github.com/repos/wzv5/pping/releases/latest" | jq -r .tag_name | cut -d "v" -f 2

echo "Pulling latest version $VERSION"
if ! command -v brew &> /dev/null
then
  echo "Homebrew is required and it is not installed. Would you like to install it now? (y/n)"
  read -r response
  if [[ "$response" == "y" ]]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  else
    echo "Please install Homebrew first."
    exit 1
  fi
fi
brew install iperf3
brew install speedtest-cli
brew install httping
brew install ansible
brew install json_log_formatter

if [[ $(uname -m) == "arm64" ]]; then
  echo "This is an ARM-based Mac"
  wget https://github.com/wzv5/pping/releases/download/v${VERSION}/pping_${VERSION}_Darwin_arm64.tar.gz
  tar -xvf pping_${VERSION}_Darwin_arm64.tar.gz -C pping
  
else
  echo "This is not an ARM-based Mac, assuming x86_64"
  wget https://github.com/wzv5/pping/releases/download/v${VERSION}/pping_${VERSION}_Darwin_x86_64.tar.gz
  tar -xvf pping_${VERSION}_Darwin_x86_64.tar.gz -C pping
fi

mv pping/pping /usr/local/bin/pping
chmod +x /usr/local/bin/pping
export RUNMODE="thin"