#!/bin/bash
gcc -m64 -c -o readflag.o readflag.S
objcopy -S -O binary -j .text readflag.o readflag.bin
rm -rf readflag.o
