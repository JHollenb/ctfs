#!/usr/bin/python3

from pwn import *

IP = "10.10.183.250"
USER="pingu"
PASS="pinguapingu"
shell = ssh(USER, IP, password=PASS)
p = shell.process('/opt/secret/root')
p.sendline
shell.iteractive()
