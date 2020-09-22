#!/bin/bash
HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# enable randomization
sudo $HERE/bin/setup enable_aslr

sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y gcc-multilib
sudo apt-get install -y gcc-arm-linux-gnueabi qemu-user gdb-multiarch moreutils libseccomp2 libssl-dev:i386 libseccomp-dev:i386

sudo mkdir -p /home/seclab/lab07/memo/db
sudo chmod 770 /home/seclab/lab07/memo/db
sudo adduser --no-create-home --disabled-password --disabled-login --force-badname --home /dev/null --shell /bin/false --gecos "" memo_dummy
sudo chown root:memo_dummy /home/seclab/lab07/memo/db
sudo chown root:memo_dummy /home/lab07/memo/target
sudo chmod 2755 /home/lab07/memo/target