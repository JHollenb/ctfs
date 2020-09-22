#!/usr/bin/python2.7

import sys
import os

TARGET_STRING = 'ROP_ATTACK_SUCCESS'
# NOTE: Don't modify this file
PROG = "/home/lab06/puzzle/vuln"

if __name__ == '__main__':
    print 'Your mission is to make a ROP chain that prints "%s"' % TARGET_STRING
    payload = raw_input()
    r, w = os.pipe()
    pid = os.fork()

    if pid:
        os.close(w)
        r = os.fdopen(r, 'r', 0)
        print r.readline(),
        line = r.readline().strip()
        print line
        if line == TARGET_STRING:
            os.setreuid(os.geteuid(), os.geteuid())
            os.system("/bin/cat /proc/flag")
        else:
            print "Failed..."
        os.waitpid(pid, 0)
        r.close()
    else:           # Child
        os.close(r)
        os.dup2(w, 1)
        os.setreuid(os.getuid(), os.getuid())
        os.execve(PROG, [PROG, payload], {})
