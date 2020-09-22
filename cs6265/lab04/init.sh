#!/bin/bash
HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

sudo $HERE/bin/setup disable_aslr
sudo $HERE/bin/setenv --dir $HERE

cat <<EOF
  _          _     _  _
 | |    __ _| |__ | || |
 | |   / _\` | '_ \\| || |_
 | |__| (_| | |_) |__   _|
 |_____\\__,_|_.__/   |_|
                    cs6265
EOF
