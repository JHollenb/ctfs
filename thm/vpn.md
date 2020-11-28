#!/bin/bash

# install
function install-openvpn(){
apt install apt-transport-https

# Install the OpenVPN repository key used by the OpenVPN 3 Linux packages

wget https://swupdate.openvpn.net/repos/openvpn-repo-pkg-key.pub
apt-key add openvpn-repo-pkg-key.pub

# Then you need to install the proper repository. Replace $DISTRO with the release name depending on your Debian/Ubuntu distribution.
DISTRO="bionic"
wget -O /etc/apt/sources.list.d/openvpn3.list https://swupdate.openvpn.net/community/openvpn3/repos/openvpn3-$DISTRO.list
apt update
apt-get install openvpn3
}


function run-openvpn(){
CONFIG_FILE=jhollctf.ovpn
openvpn3 config-import --config ${CONFIG_FILE}
openvpn3 session-start --config ${CONFIG_FILE}
}
