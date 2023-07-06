#bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install git -y

git clone https://github.com/Zerbaib/StatusDiscordBot.git
cd StatusDiscordBot

read -p "Do you want to start the install script now ? [y/n] " choice

if [[ $choice == "y" ]]; then
    ./install.sh
else
    echo "Install script was not executed."
fi