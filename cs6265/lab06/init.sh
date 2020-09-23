#!/bin/bash
HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
URL=http://www.capstone-engine.org/download/3.0.4/ubuntu-14.04

install_capstone() {  
  if [ $(dpkg-query -W -f='${Status}' libcapstone3 2>/dev/null | \
	grep -c "ok installed") -eq 0 ];
  then

    wget $URL/libcapstone3_3.0.4-0.1ubuntu1_amd64.deb -O libcapstone3.deb
    wget $URL/python-capstone_3.0.4-0.1ubuntu1_amd64.deb -O python-capstone.deb

    sudo dpkg -i libcapstone3.deb
    sudo dpkg -i python-capstone.deb

    rm libcapstone3.deb
    rm python-capstone.deb

  fi
}

install_capstone

# enable randomization
sudo $HERE/bin/setup enable_aslr
sudo $HERE/bin/setenv --dir $HERE

# more setup
sudo chown puzzle:puzzle $HERE/puzzle/vuln
sudo chown rop-sorting:rop-sorting $HERE/rop-sorting/vuln

sudo dpkg --add-architecture i386
sudo apt update
sudo apt install libseccomp2:i386 libc6-dbg:i386 -y

cat <<EOF
- _          _      __           
-| |    __ _| |__  / /_          
-| |   / _\` | '_ \| '_ \\       
-| |__| (_| | |_) | (_) |        
-|_____\__,_|_.__/ \___/
EOF
