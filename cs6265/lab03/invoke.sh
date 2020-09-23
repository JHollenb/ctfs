#!/bin/sh
# https://stackoverflow.com/questions/17775186/buffer-overflow-works-in-gdb-but-not-without-it

while getopts "dte:h?" opt ; do
case "$opt" in
h|\?)
printf "usage: %s -e KEY=VALUE prog [args...]\n" $(basename $0)
exit 0
;;
t)
tty=1
gdb=1
;;
d)
gdb=1
;;
e)
env=$OPTARG
;;
esac
done

shift $(expr $OPTIND - 1)
prog=$(readlink -f $1)
shift
if [ -n "$gdb" ] ; then
if [ -n "$tty" ]; then
touch /tmp/gdb-debug-pty
exec env - $env LANG=$LANG COLUMNS=$(tput cols) LINES=$(tput lines) PATH=$PATH TERM=$TERM HOME=$HOME PWD=$PWD gdb -tty /tmp/gdb-debug-pty --args $prog "$@"
else
exec env - $env LANG=$LANG COLUMNS=$(tput cols) LINES=$(tput lines) PATH=$PATH TERM=$TERM HOME=$HOME PWD=$PWD gdb --args $prog "$@"
fi
else
exec env - $env LANG=$LANG COLUMNS=$(tput cols) LINES=$(tput lines) PATH=$PATH TERM=$TERM HOME=$HOME PWD=$PWD $prog "$@"
fi
