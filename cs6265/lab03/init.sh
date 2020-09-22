#!/bin/bash
HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

sudo $HERE/bin/setup disable_aslr
sudo $HERE/bin/setenv --dir $HERE

sudo apt update && sudo apt install -y hexedit

# install pwndbg
pushd $HERE/bin/pwndbg-git
sudo ./setup.sh
popd

# setup tut03-pwntool
if [ -e /home/lab03/tut03-pwntool ]; then
  sudo /usr/sbin/adduser --uid 23000 --no-create-home \
    --disabled-password --disabled-login \
    --force-badname --home /dev/null \
    --shell /bin/false --gecos "" tut03-pwntool
  sudo /bin/chown root:tut03-pwntool /home/lab03/tut03-pwntool/crackme0x00
  sudo /bin/chmod 2755 /home/lab03/tut03-pwntool/crackme0x00
fi

cat <<EOF
 _          _    _____
| |    __ _| |__|___ /
| |   / _\` | '_ \ |_ \
| |__| (_| | |_) |__) |
|_____\__,_|_.__/____/
                    cs6265
EOF
