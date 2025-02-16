if [ ! -d "bin" ]; then
    sudo apt update && sudo apt upgrade
    sudo apt install python3-venv
    python3 -m venv .
fi

sudo apt update && sudo apt upgrade
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

source bin/activate
pip3 install buildozer kivy[full] https://github.com/kivymd/KivyMD/archive/master.zip