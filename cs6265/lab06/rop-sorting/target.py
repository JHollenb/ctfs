#!/usr/bin/python2.7 -u

import sys
import subprocess as sp
import os
import random

NUM_NUMBERS = 8
RANGE = 256

PROG = "/home/lab06/rop-sorting/vuln"

def generate_list():
    while True:
        l = []
        for i in xrange(NUM_NUMBERS):
            l.append(random.randrange(RANGE))
        if any(l[i] > l[i+1] for i in xrange(len(l)-1)):
            return l

def sorted_string(l):
    sorted_l = sorted(l)
    return '[' + ', '.join(map(lambda x:"%4d" % x, sorted_l)) + ']'

if __name__ == '__main__':
    print 'Sort by ROP'

    r1, w1 = os.pipe()
    r2, w2 = os.pipe()
    pid = os.fork()

    if not pid:
        # child

        os.close(r1)
        os.close(w2)
        os.dup2(w1, 1)
        os.dup2(r2, 0)
        os.setreuid(os.getuid(), os.getuid())
        os.execve(PROG, [PROG], {})

    else:
        # parent
        os.close(w1)
        os.close(r2)

        r = os.fdopen(r1, 'r', 0)
        w = os.fdopen(w2, 'w', 0)

        # print stack
        while True:
            l = r.readline()
            print l,
            if l == "\n":
                break

        print 'Give me a payload'
        payload = raw_input()

        # generate list
        l = generate_list()
        for value in l:
            w.write("%d\n" % value)

        w.write(payload + "\n")

        expected = sorted_string(l)
        print r.readline(),
        result = r.readline().strip()
        print result
        if (result == expected):
            os.setreuid(os.geteuid(), os.geteuid())
            os.system("/bin/cat /proc/flag")
        else:
            print "Failed.."

        os.waitpid(pid, 0)
        r.close()
        w.close()
