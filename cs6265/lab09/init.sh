#!/bin/bash
HERE=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# enable randomization
sudo $HERE/bin/setup enable_aslr
sudo $HERE/bin/setenv --dir $HERE

cat <<EOF
 _          _      __
| |    __ _| |__  / /_
| |   / _\` | '_ \| '_ \\
| |__| (_| | |_) | (_) |
|_____\__,_|_.__/ \___/
                  cs6265
EOF
