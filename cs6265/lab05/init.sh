#!/bin/bash
HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

wget http://www.capstone-engine.org/download/3.0.4/ubuntu-14.04/libcapstone3_3.0.4-0.1ubuntu1_amd64.deb -O libcapstone3.deb
wget http://www.capstone-engine.org/download/3.0.4/ubuntu-14.04/python-capstone_3.0.4-0.1ubuntu1_amd64.deb -O python-capstone.deb

sudo dpkg -i libcapstone3.deb
sudo dpkg -i python-capstone.deb
rm libcapstone3.deb
rm python-capstone.deb

sudo apt install gnuplot

# enable randomization
sudo $HERE/bin/setup enable_aslr
sudo $HERE/bin/setenv --dir $HERE

cat <<EOF
 _       _    ____
| | __ _| |__| ___|
| |/ _\` | '_ \\___ \\
| | (_| | |_) |__) |
|_|\\__,_|_.__/____/
                  cs6265
EOF
