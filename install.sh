#bin/bash

sudo apt install python3
sudo apt install python3-pip
sudo apt install python-is-python3

pip install disnake

clear

read -p "Do you want to start the start script now ? [y/n] " choice

if [[ $choice == "y" ]]; then
    ./start.sh
else
    echo "Start script was not executed."
fi