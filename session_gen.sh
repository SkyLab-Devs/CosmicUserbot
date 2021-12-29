#!/bin/bash

clear

# Colors
RED="\033[1;31m" # For errors / warnings
GREEN="\033[1;32m" # For info
YELLOW="\033[1;33m" # For info
BLUE="\033[1;36m" # For info again XD
NC="\033[0m" # reset color

absent=""
echo -e "${GREEN} Checking for requirements${NC}\n"
check(){
	sleep 0.15
	pkg=$1
	command -v $pkg;stat=$?
	if [ "$stat" -ne "0" ]; then
		absent+="$pkg "
	fi

}

instl(){
	sleep 0.2
	if [ -e /data/data/com.termux/files/usr/bin/termux-info ]; then
	        echo -e "${GREEN} Detected Termux! Installing requirements for termux ${NC}"
		apt update
		pkg install python -y
	        echo -e "${YELLOW} \n\nInstalled requirements Successfully ${NC}"
	elif [ -e /usr/bin/apt ]; then
		echo -e "${GREEN} Detected Debian based distro! Trying to install requirements ${NC}"
		sudo apt update
		sudo apt install $1 -y
	else
		echo -e "${YELLOW} \n\nUnknown System Detected... Please install \n $1 \n  for your distro \nA quick google search will help if you don't know how to \n\n ${NC}"
		sleep 3
	fi
	}

check "pip3"
check "python3"


if [ "$absent" == "" ]; then
	echo -e "${BLUE} Requirements Already Installed, Continuing! ${NC}"
else
	instl $absent
fi

sleep 0.5
echo -e "${YELLOW} Installing telethon ${NC}\n"
pip3 install telethon
echo -e "${GREEN} Done! ${NC}\n\n"

sleep 0.3
echo -e "${Blue} Downloading string session generator script ${NC}"
curl https://raw.githubusercontent.com/FrosT2k5/ProjectFizilion/demon/string_session.py > string_session.py
echo -e "${GREEN} Done! ${NC}\n\n"

sleep 2
echo -e "Running string_session.py!\nIn case you have issues in generating string session now,\nYou can run the string_session.py here again to regenrate session.\nThe one-liner command is: \n\n"
$(sleep 1.5)
echo -e "${RED}python3 $(pwd)/string_session.py${NC}\n\n"
$(sleep 0.5)
echo -e "If you feel lazy :p\n"

python3 string_session.py
