#!/bin/bash

HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# enable randomization
sudo $HERE/bin/setup enable_aslr
sudo $HERE/bin/setenv --dir $HERE

sudo apt-get update
sudo apt-get install -y runit xinetd php5 python-pip php5-sqlite sqlite3 g++-multilib libseccomp2:i386
sudo pip install django==1.8
