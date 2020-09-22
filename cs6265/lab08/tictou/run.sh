#!/bin/sh
rm -f /rw/db.sqlite
# php -S 0.0.0.0:$1 -t $(dirname "$0")/html&
# php -S 0.0.0.0:$(expr $1 + 1) -t $(dirname "$0")/html
php -S 0.0.0.0:$1 -t /home/lab08/tictou/html&
php -S 0.0.0.0:$(expr $1 + 1) -t /home/lab08/tictou/html
